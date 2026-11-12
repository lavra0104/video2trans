# Video to text

Transcribe speech from a local video into a UTF-8 text file. The script also prints
the transcript as it is generated. It uses the CPU, detects the language by
default, and keeps the original language of the speech.

## Requirements

- Python 3.9 or newer with the `venv` and `ensurepip` modules.
- Bash for the setup script on Linux or macOS.
- Internet access to install packages and download a speech model on its first use.

No API key or separate FFmpeg command-line installation is required. Audio decoding
uses the FFmpeg libraries bundled with PyAV. Transcription runs on your machine.

## Install

From this project directory:

```bash
bash setup.sh
source .venv/bin/activate
```

The setup script creates `.venv` beside itself, installs pip if it is missing,
installs the packages from `requirements.txt`, and checks the dependencies. It can
also be rerun against an existing environment. To select a Python interpreter
when creating a new environment:

```bash
PYTHON_BIN=python3.11 bash setup.sh
```

To install manually:

```bash
python3 -m venv .venv
.venv/bin/python -m ensurepip --upgrade --default-pip
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
source .venv/bin/activate
```

On Debian or Ubuntu, if virtual environment creation reports that `ensurepip` is
unavailable, install the venv package for your chosen Python version. For the
system Python this is usually:

```bash
sudo apt-get update
sudo apt-get install python3-venv
```

## Transcribe a video

```bash
python video_to_text.py recording.webm -o transcript.txt
```

For the recording already downloaded into this directory:

```bash
python video_to_text.py applicant-6ad6772de6e2af5f47639290-1792440795691.webm -o transcript.txt
```

An existing output file is replaced after transcription completes. When `-o` is
omitted, the output uses the video's filename with a `.txt` extension beside the
video.

To specify the language or select a larger model:

```bash
python video_to_text.py recording.webm --language en --model small -o transcript.txt
```

You can also run without activating the environment:

```bash
.venv/bin/python video_to_text.py recording.webm -o transcript.txt
```

| Option | Default | Description |
| --- | --- | --- |
| `video` | Required | Path to the input video or audio file. |
| `-o`, `--output` | Input path with `.txt` extension | Path to the output text file. |
| `--model` | `base` | Model name, such as `tiny`, `base`, `small`, or `medium`. |
| `--language` | Auto-detect | Language code, such as `en`, `es`, or `ja`. |
| `-h`, `--help` | — | Show command-line help. |

Model files are downloaded from Hugging Face and cached for subsequent runs. The
script processes the first audio stream in the video. It transcribes speech;
on-screen text and speaker labels are not included. Long recordings require more
processing time and memory because the decoder loads the audio into memory.

## Dependencies

`requirements.txt` pins the direct runtime dependencies:

- `faster-whisper==1.2.1`: speech recognition, model downloading, and voice activity detection.
- `av==16.1.0`: video/audio decoding. This version avoids the `metadata_errors`
  incompatibility between faster-whisper 1.2.1 and PyAV 19.

Pip installs the remaining dependencies automatically, including CTranslate2,
Hugging Face Hub, tokenizers, ONNX Runtime, NumPy, and tqdm. `argparse`, `sys`, and
`pathlib` are part of Python's standard library.

To verify an installation:

```bash
python -m pip check
python -c 'import av; from faster_whisper import WhisperModel; print("Ready")'
```

If `python -m pip` reports `No module named pip`, run `bash setup.sh` again, or run
`.venv/bin/python -m ensurepip --upgrade --default-pip` before the manual install.

Upstream documentation: [faster-whisper](https://github.com/SYSTRAN/faster-whisper).
