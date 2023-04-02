# as9-auto-play

## Setup environment

First clone repo and CD into it.

Install the venv. Must use Python 3.9.

`path/to/python3.9 -m venv .venv`

Activate the venv.

`.\.venv\Scripts\activate`

Install dependencies.

This command is from: https://pytorch.org/get-started/locally/

Install pytorch with CUDA.
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

`pip install -r requirements.txt`

`$env:PYTHONPATH = (Join-Path (Get-Location).Path 'src')`

`cd src/as9/run`

Edit `settings.py`

`python run_hunt.py`
