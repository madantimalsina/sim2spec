#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/setup.sh"
python3 -m venv "$venv_name"
source "$venv_name/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .
if [[ ! -d larnd-sim/.git ]]; then
    rm -rf larnd-sim
    git clone -b develop https://github.com/DUNE/larnd-sim
fi
cd larnd-sim
python -m pip install -e .
