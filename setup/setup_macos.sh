#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "The script is running from: $SCRIPT_DIR"
#parent="${SCRIPT_DIR%/*}"
#$FLATCAM_PATH="${parent%/*}"
FLATCAM_PATH="${SCRIPT_DIR%/*}"
cd $FLATCAM_PATH

#python3.14 -m venv .venv
#source .venv/bin/activate
#pip3 install -r $SCRIPT_DIR/requirements.txt

echo "... Prepare QT forms"
pyrcc5 "$SCRIPT_DIR/resources.qrc" -o "$FLATCAM_PATH/resources.py"
pyrcc5 "$SCRIPT_DIR/resources_dark.qrc" -o "$FLATCAM_PATH/resources_dark.py"

echo "... Compile languages dictionary"
find "$FLATCAM_PATH/translate" -name "*.po" -exec sh -c 't={} ; msgfmt "${t%.*}.po" -o  "${t%.*}.mo" ' \;

