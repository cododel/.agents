# graphify reference: transcribe video and audio

Load this only when `detect` reported one or more `video` files. A corpus with no video never reads this.

### Step 2.5 - Transcribe video / audio files (only if video files detected)

Skip this step entirely if `detect` returned zero `video` files.

Video and audio files cannot be read directly. Transcribe them to text first, then treat the transcripts as doc files in Step 3.

**Strategy:** Read the god nodes from `graphify-out/.graphify_detect.json` (or the analysis file if it exists from a previous run). You are already a language model — write a one-sentence domain hint yourself from those labels. Then pass it to Whisper as the initial prompt. No separate API call needed.

**However**, if the corpus has *only* video files and no other docs/code, use the generic fallback prompt: `"Use proper punctuation and paragraph breaks."`

**Step 1 - Write the Whisper prompt yourself.**

Read the top god node labels from detect output or analysis, then compose a short domain hint sentence, for example:

- Labels: `transformer, attention, encoder, decoder` → `"Machine learning research on transformer architectures and attention mechanisms. Use proper punctuation and paragraph breaks."`
- Labels: `kubernetes, deployment, pod, helm` → `"DevOps discussion about Kubernetes deployments and Helm charts. Use proper punctuation and paragraph breaks."`

**Export** it as `GRAPHIFY_WHISPER_PROMPT` (the exact name the transcriber reads — and it must be `export`ed so the child Python process sees it) for the next command.

**Step 2 - Transcribe:**

```bash
export GRAPHIFY_WHISPER_MODEL=base  # or whatever --whisper-model the user passed (must be exported)
export GRAPHIFY_WHISPER_PROMPT="<the one-sentence domain hint you composed in Step 1>"
$(cat graphify-out/.graphify_python) -c "
import json, os, sys
from pathlib import Path
from graphify.transcribe import transcribe
import hashlib

detect = json.loads(Path('graphify-out/.graphify_detect.json').read_text(encoding=\"utf-8\"))
video_files = detect.get('files', {}).get('video', [])
prompt = os.environ.get('GRAPHIFY_WHISPER_PROMPT', 'Use proper punctuation and paragraph breaks.')
reads = detect.setdefault('read_paths', {})
for original in video_files:
    # A distinct directory avoids collisions between equally named media in different folders.
    token = hashlib.sha256(original.encode()).hexdigest()[:16]
    target = Path('graphify-out/transcripts') / token
    transcript = transcribe(original, output_dir=target, initial_prompt=prompt)
    reads[original] = str(Path(transcript).resolve())
detect['files'].setdefault('document', []).extend(video_files)
detect['files']['video'] = []
Path('graphify-out/.graphify_detect.json').write_text(json.dumps(detect, ensure_ascii=False), encoding=\"utf-8\")
print(f'Transcribed {len(video_files)} files; retained original source identities')

"
```

After transcription, cache lookup and chunk FILE_LIST use original paths. Supply read_paths to the
agent for reading material, and fingerprint both original and derived bytes. Use the original path
for IDs and source_file; source_location refers to the original when meaningful, otherwise null.
If a transcription fails, retry that file once; remaining failures stop the build as incomplete.

**Whisper model:** Default is `base`. If the user passed `--whisper-model <name>`, `export GRAPHIFY_WHISPER_MODEL=<name>` (it must be exported, not just assigned) before running the command above.
