#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "The script is running from: $SCRIPT_DIR"
parent="${SCRIPT_DIR%/*}"
WORK_DIR="${parent%/*}"
cd $WORK_DIR

python3.14 -m venv .venv
source .venv/bin/activate

pip3 install -r setup/macos/requirements.txt
