#!/usr/bin/env bash
# Install the project into a virtual environment beside this script.
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
venv_dir="$project_dir/.venv"
venv_python="$venv_dir/bin/python"
python_bin="${PYTHON_BIN:-python3}"

if [[ -x "$venv_python" ]]; then
    python_bin="$venv_python"
fi

"$python_bin" -c 'import sys; sys.exit("Python 3.9 or newer is required.") if sys.version_info < (3, 9) else None'

if [[ ! -x "$venv_python" ]]; then
    "$python_bin" -m venv "$venv_dir"
fi

# Some virtual environments are created without pip.
if ! "$venv_python" -m pip --version >/dev/null 2>&1; then
    "$venv_python" -m ensurepip --upgrade --default-pip
fi

"$venv_python" -m pip install --upgrade pip
"$venv_python" -m pip install -r "$project_dir/requirements.txt"
"$venv_python" -m pip check
"$venv_python" -c 'import av; from faster_whisper import WhisperModel, download_model; print("Dependency imports passed.")'

printf '\nSetup complete. Activate the environment with:\n  source %q\n' "$venv_dir/bin/activate"
