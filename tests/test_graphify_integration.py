"""Optional installed-package probes; never install Graphify to run these tests."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/graphify/scripts'


@unittest.skipUnless(importlib.util.find_spec('graphify'), 'Graphify is not installed in this interpreter')
class InstalledGraphifyTests(unittest.TestCase):
    def test_custom_output_is_excluded_from_incremental_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'source.md').write_text('Original source.')
            output = root / 'custom-results'
            output.mkdir()
            (output / 'GRAPH_REPORT.md').write_text('Generated report is not a source.')
            probe = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
root, output = Path(sys.argv[2]), Path(sys.argv[3])
os.environ['GRAPHIFY_OUT'] = str(output / '.runs/test/work/graphify-out')
from run_sources import detect_sources
from graphify.detect import save_manifest
result = detect_sources(root, published_output=output)
assert result['files']['document'] == [str(root / 'source.md')], result['files']
save_manifest(result['files'], root=root)
result = detect_sources(root, published_output=output, incremental=True)
assert result['new_total'] == 0, result
'''
            result = subprocess.run([sys.executable, '-c', probe, str(SCRIPTS), str(root), str(output)],
                                    cwd=root, capture_output=True, text=True, check=False)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
