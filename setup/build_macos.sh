#!/bin/bash
set +x
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FLATCAM_PATH="${SCRIPT_DIR%/*}"
cd $FLATCAM_PATH

source   $FLATCAM_PATH/.venv/bin/activate
#pyinstaller  -F --onefile --windowed  -y  --clean --name="ReFlatCAM" --icon="$SCRIPT_DIR/resources/flatcam_icon256.icns" ./FlatCAM.py
# help_bin = pkgutil.get_data( 'helpmod', 'help_data.txt' )

pyinstaller  --onedir --windowed  -y  --clean   --name="ReFlatCAM" \
  --collect-all vispy  --collect-all language_data --collect-all rasterio \
  --add-data $FLATCAM_PATH/tclCommands/*:tclCommands  \
  --add-data $FLATCAM_PATH/translate/*:translate \
  --add-data $FLATCAM_PATH/preprocessors/*:preprocessors \
  --icon="$SCRIPT_DIR/resources/flatcam_icon256.icns"  "./FlatCAM.py"

#pyinstaller  -y "$SCRIPT_DIR/ReFlatCAM.spec"
#  --collect-submodules vispy.glsl

