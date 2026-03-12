#!/bin/bash
die() {
    local exit_code=${2:-1} # Use argument 2 as exit code, default to 1 if not provided
    echo "$0: ERROR: $1" >&2 # Print error message to stderr
    exit "$exit_code" # Exit the script with the specified code
}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FLATCAM_PATH="${SCRIPT_DIR%/*}"
cd $FLATCAM_PATH || die "incorrect path $FLATCAM_PATH"

source $FLATCAM_PATH/.venv/bin/activate
#pyinstaller  -F --onefile --windowed  -y  --clean --name="ReFlatCAM" --icon="$SCRIPT_DIR/resources/flatcam_icon256.icns" ./FlatCAM.py
# help_bin = pkgutil.get_data( 'helpmod', 'help_data.txt' )

pyinstaller  --windowed  --onedir  -y  --clean   --name="ReFlatCAM" \
  --collect-all vispy  --collect-all language_data --collect-all rasterio \
  --add-data $FLATCAM_PATH/tclCommands/*:tclCommands  \
  --add-data $FLATCAM_PATH/translate/*:translate \
  --add-data $FLATCAM_PATH/preprocessors/*:preprocessors \
  --distpath "SCRIPT_DIR/dist" \
  --icon="$SCRIPT_DIR/resources/flatcam_icon256.icns"  "./FlatCAM.py"

#pyinstaller  -y "$SCRIPT_DIR/ReFlatCAM.spec"
#  --collect-submodules vispy.glsl

