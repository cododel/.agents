import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/graphify/scripts'
sys.path.insert(0, str(SCRIPTS))
import run_state as runs
import run_sources
sys.path.pop(0)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.source = self.root / 'doc.md'
        self.source.write_text('source v1')
        self.output = self.root / 'graphify-out'
        self.output.mkdir()
        self.old = {'nodes': [{'id': 'old'}], 'links': []}
        runs.write_json(self.output / 'graph.json', self.old)
        (self.output / 'GRAPH_REPORT.md').write_text('old report')

    def prepared(self, chunks=True):
        run = runs.begin(self.output)
        plan = run / 'plan.json'
        runs.write_json(plan, {'sources': [str(self.source)], 'parameters': {'mode': 'standard'},
                              'chunks': [[str(self.source)]] if chunks else []})
        state = runs.prepare(run, plan)
        return run, state

    def chunk(self, run, state):
        extraction = {'nodes': [{'id': 'new', 'label': 'New', 'file_type': 'document',
                                 'source_file': str(self.source)}], 'edges': [], 'hyperedges': []}
        path = run / 'chunks/chunk-0000.json'
        runs.write_json(path, {'run_id': state['run_id'], 'chunk_id': 0,
                              'fingerprint': state['fingerprint'], 'extraction': extraction})
        return path

    def stage(self, run):
        stage = run / 'work/graphify-out'
        runs.write_json(stage / 'graph.json', {'nodes': [{'id': 'new'}], 'links': []})
        runs.write_json(stage / '.graphify_extract.json', {'nodes': [{'id': 'new'}], 'edges': []})
        (stage / 'GRAPH_REPORT.md').write_text('new report')

    def unchanged(self):
        self.assertEqual(self.old, runs.read_json(self.output / 'graph.json'))
        self.assertEqual('old report', (self.output / 'GRAPH_REPORT.md').read_text())

    def test_success_ignores_unlisted_and_previous_chunks(self):
        previous, state = self.prepared()
        self.chunk(previous, state)
        run, state = self.prepared()
        self.chunk(run, state)
        (run / 'chunks/chunk-0099.json').write_text('invalid stale content')
        result = runs.merge(run)
        self.assertEqual(['new'], [n['id'] for n in result['nodes']])
        self.stage(run)
        runs.publish(run)
        self.assertEqual('new', runs.read_json(self.output / 'graph.json')['nodes'][0]['id'])
        self.assertEqual('new report', (self.output / 'GRAPH_REPORT.md').read_text())
        self.assertTrue((previous / 'chunks/chunk-0000.json').exists())

    def test_missing_chunk_does_not_publish(self):
        run, _ = self.prepared()
        with self.assertRaises(ValueError):
            runs.merge(run)
        self.stage(run)
        with self.assertRaises(ValueError):
            runs.publish(run)
        self.unchanged()

    def test_invalid_json_and_structure_fail(self):
        for content in ('{', '[]', '{"nodes":[]}'):
            with self.subTest(content=content):
                run, _ = self.prepared()
                (run / 'chunks/chunk-0000.json').write_text(content)
                with self.assertRaises(ValueError):
                    runs.merge(run)
        self.unchanged()

    def test_bad_extraction_is_rejected(self):
        run, state = self.prepared()
        path = self.chunk(run, state)
        payload = runs.read_json(path)
        payload['extraction']['nodes'] = ['invalid node']
        runs.write_json(path, payload)
        with self.assertRaises(ValueError):
            runs.merge(run)

    def test_foreign_source_is_rejected(self):
        run, state = self.prepared()
        path = self.chunk(run, state)
        payload = runs.read_json(path)
        payload['extraction']['nodes'][0]['source_file'] = '/foreign/doc.md'
        runs.write_json(path, payload)
        with self.assertRaisesRegex(ValueError, 'foreign'):
            runs.merge(run)

    def test_new_run_rejects_copied_envelope(self):
        old, state = self.prepared()
        payload = self.chunk(old, state).read_bytes()
        run, state = self.prepared()
        (run / 'chunks/chunk-0000.json').write_bytes(payload)
        with self.assertRaisesRegex(ValueError, 'foreign or stale'):
            runs.merge(run)
        self.chunk(run, state)
        runs.merge(run)

    def test_source_change_invalidates_merge_and_publication(self):
        run, state = self.prepared()
        self.chunk(run, state)
        runs.merge(run)
        self.stage(run)
        self.source.write_text('source v2')
        for action in (runs.merge, runs.publish):
            with self.assertRaisesRegex(ValueError, 'source changed'):
                action(run)
        self.unchanged()

    def test_preparation_cannot_be_rewritten(self):
        run, _ = self.prepared()
        with self.assertRaisesRegex(ValueError, 'immutable'):
            runs.prepare(run, run / 'plan.json')

    def test_chunk_change_after_merge_invalidates_publication(self):
        run, state = self.prepared()
        path = self.chunk(run, state)
        runs.merge(run)
        self.stage(run)
        path.write_text(path.read_text() + ' ')
        with self.assertRaisesRegex(ValueError, 'chunk changed'):
            runs.publish(run)
        self.unchanged()

    def test_published_drift_is_preserved(self):
        run, state = self.prepared()
        self.chunk(run, state)
        runs.merge(run)
        self.stage(run)
        (self.output / 'GRAPH_REPORT.md').write_text('operator edit')
        with self.assertRaisesRegex(ValueError, 'published output changed'):
            runs.publish(run)
        self.assertEqual('operator edit', (self.output / 'GRAPH_REPORT.md').read_text())
        self.assertFalse((self.output / '.publish-lock').exists())

    def test_invalid_graph_preserves_outputs(self):
        run, _ = self.prepared(chunks=False)
        runs.merge(run)
        self.stage(run)
        runs.write_json(run / 'work/graphify-out/graph.json', {'nodes': [], 'links': []})
        with self.assertRaises(ValueError):
            runs.publish(run)
        self.unchanged()

    def test_io_failure_rolls_back_sidecars(self):
        run, state = self.prepared()
        self.chunk(run, state)
        runs.merge(run)
        self.stage(run)
        replace = runs.os.replace
        failed = False
        def fail_once(src, dst):
            nonlocal failed
            if Path(dst) == self.output / 'graph.json' and not failed:
                failed = True
                raise OSError('simulated disk error')
            return replace(src, dst)
        with patch.object(runs.os, 'replace', side_effect=fail_once):
            with self.assertRaises(OSError):
                runs.publish(run)
        self.unchanged()
        self.assertFalse((self.output / '.publish-lock').exists())
        runs.publish(run)

    def test_interrupted_publish_leaves_recovery_lock(self):
        run, _ = self.prepared(chunks=False)
        runs.merge(run)
        self.stage(run)
        replace = runs.os.replace
        def interrupt(src, dst):
            if Path(dst) == self.output / 'graph.json':
                raise KeyboardInterrupt()
            return replace(src, dst)
        with patch.object(runs.os, 'replace', side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                runs.publish(run)
        self.assertTrue((self.output / '.publish-lock').exists())
        self.assertEqual(self.old, runs.read_json(self.output / 'graph.json'))
        self.assertEqual('old report', (run / 'backup/GRAPH_REPORT.md').read_text())

    def test_empty_chunk_plan_is_valid_for_code_only(self):
        run, _ = self.prepared(chunks=False)
        self.assertEqual([], runs.merge(run)['nodes'])
        self.stage(run)
        runs.publish(run)

    def test_plan_parameter_change_invalidates_result(self):
        run, state = self.prepared()
        self.chunk(run, state)
        plan = runs.read_json(run / 'plan.json')
        plan['parameters']['mode'] = 'deep'
        runs.write_json(run / 'plan.json', plan)
        with self.assertRaisesRegex(ValueError, 'plan parameters changed'):
            runs.merge(run)

    def test_cache_is_staged_published_and_reused(self):
        cache = self.output / 'cache'
        cache.mkdir()
        (cache / 'old.json').write_text('{}')
        run, _ = self.prepared(chunks=False)
        staged_cache = run / 'work/graphify-out/cache'
        self.assertTrue((staged_cache / 'old.json').exists())
        (staged_cache / 'new.json').write_text('{}')
        self.assertFalse((cache / 'new.json').exists())
        runs.merge(run)
        self.stage(run)
        runs.publish(run)
        self.assertTrue((cache / 'new.json').exists())
        next_run = runs.begin(self.output)
        self.assertTrue((next_run / 'work/graphify-out/cache/new.json').exists())

    def test_original_change_invalidates_unchanged_derived_content(self):
        run = runs.begin(self.output)
        derived = run / 'work/graphify-out/converted.md'
        derived.write_text('derived content')
        plan = run / 'plan.json'
        runs.write_json(plan, {'sources': [str(self.source), str(derived)], 'parameters': {},
                              'read_paths': {str(self.source): str(derived)},
                              'chunks': [[str(self.source)]]})
        state = runs.prepare(run, plan)
        self.chunk(run, state)
        self.source.write_text('original modified after conversion')
        with self.assertRaisesRegex(ValueError, 'source changed'):
            runs.merge(run)

    def test_two_derived_runs_keep_original_identity_after_cleanup(self):
        import shutil
        for attempt in range(2):
            run = runs.begin(self.output)
            derived = run / 'work/graphify-out/transcript.txt'
            derived.write_text('transcript')
            runs.write_json(run / 'plan.json', {'sources': [str(self.source), str(derived)],
                           'parameters': {}, 'read_paths': {str(self.source): str(derived)},
                           'chunks': [[str(self.source)]]})
            state = runs.prepare(run, run / 'plan.json')
            self.chunk(run, state)
            merged = runs.merge(run)
            stage = run / 'work/graphify-out'
            runs.write_json(stage / '.graphify_extract.json', merged)
            runs.write_json(stage / 'graph.json', {'nodes': merged['nodes'], 'links': []})
            (stage / 'GRAPH_REPORT.md').write_text('graph of original')
            runs.publish(run)
            shutil.rmtree(run)
            published = runs.read_json(self.output / 'graph.json')
            self.assertEqual(str(self.source), published['nodes'][0]['source_file'])
            self.assertTrue(Path(published['nodes'][0]['source_file']).exists())

    def test_converted_detection_resolves_original_and_incremental_hash(self):
        import hashlib
        original = self.root / 'report.docx'
        original.write_text('original bytes')
        converted = self.root / 'staged/converted'
        converted.mkdir(parents=True)
        token = hashlib.sha256('report.docx'.encode()).hexdigest()[:8]
        derived = converted / f'report_{token}.md'
        derived.write_text('converted')
        files, reads = run_sources.source_reads({'document': [str(derived)]},
                                                [original], self.root, converted)
        self.assertEqual({'document': [str(original)]}, files)
        self.assertEqual({str(original): str(derived)}, reads)
        manifest = {str(original): {'semantic_hash': hashlib.md5(original.read_bytes()).hexdigest()}}
        self.assertEqual(0, run_sources.incremental_files(files, manifest, self.root)['new_total'])
        original.write_text('changed original')
        self.assertEqual(1, run_sources.incremental_files(files, manifest, self.root)['new_total'])


if __name__ == '__main__':
    unittest.main()
