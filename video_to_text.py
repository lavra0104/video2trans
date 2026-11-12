#!/usr/bin/env python3
"""Transcribe a video's audio into a UTF-8 text file.

Requires Python 3.9+. Install from the project directory:
    bash setup.sh
    source .venv/bin/activate

Or, with a virtual environment already activated:
    python -m pip install -r requirements.txt

Examples:
    python video_to_text.py recording.mp4
    python video_to_text.py recording.mp4 -o transcript.txt --language en
    python video_to_text.py recording.mp4 --model small

Transcription runs locally on the CPU. The first run downloads the model.
"""

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("video", type=Path, help="Path to the video file")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Output text file (default: the video path with a .txt extension)",
    )
    parser.add_argument(
        "--model", default="base",
        help="Whisper model name, e.g. tiny, base, small, medium (default: base)",
    )
    parser.add_argument(
        "--language", help="Language code, e.g. en, es, ja (default: auto-detect)",
    )
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    output = (
        args.output.expanduser().resolve() if args.output else video.with_suffix(".txt")
    )
    if not video.is_file():
        parser.error(f"Video file does not exist: {video}")
    if output == video or (output.exists() and output.samefile(video)):
        parser.error("The output file must be different from the input video.")

    try:
        from faster_whisper import WhisperModel, download_model
    except ImportError as exc:
        print(
            f"Cannot import faster-whisper: {exc}\n"
            "From the project directory, run: bash setup.sh\n"
            "Or, in an activated environment: python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    try:
        print(f"Loading model: {args.model}", file=sys.stderr, flush=True)
        # Resolve names explicitly, even if a folder such as "base" exists nearby.
        model_path = download_model(args.model)
        model = WhisperModel(model_path, device="cpu", compute_type="int8")
        segments, info = model.transcribe(
            str(video),
            language=args.language,
            task="transcribe",
            beam_size=5,
            vad_filter=True,
        )
        print(f"Language: {info.language}", file=sys.stderr, flush=True)

        # Iterating the segments performs the transcription.
        lines = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                lines.append(text)
                print(text, flush=True)

        output.parent.mkdir(parents=True, exist_ok=True)
        transcript = "\n".join(lines)
        output.write_text(transcript + ("\n" if transcript else ""), encoding="utf-8")
    except Exception as exc:
        print(f"Transcription failed: {exc}", file=sys.stderr)
        return 1

    if not lines:
        print("No speech detected; the transcript is empty.", file=sys.stderr)
    print(f"Saved transcript to: {output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
