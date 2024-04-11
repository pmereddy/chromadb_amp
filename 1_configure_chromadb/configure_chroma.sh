#!/bin/bash
# 1. switch to using pysqlite3
# 2. fix the log level

PYTHON_DIR=python3.10
if [ ${MISSING_SQLITE_DEPENDENCY:-'true'}=='true' ]; then
    FILE="/home/cdsw/.local/lib/${PYTHON_DIR}/site-packages/chromadb/__init__.py"

    TEMP_FILE=$(mktemp)
    rm -f ${TEMP_FILE}

    # Use sed to remove lines containing the specific logger initialization
    sed -i '/logger = logging\.getLogger(__name__)/d' "$FILE"

    # The three lines to be added
    echo "__import__('pysqlite3')" > $TEMP_FILE
    echo "import sys" >> $TEMP_FILE
    echo "sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')" >> $TEMP_FILE

    # Append the original file content to the temp file
    cat "$FILE" >> "$TEMP_FILE"

    # Replace the original file with the new file
    mv "$TEMP_FILE" "$FILE"
    echo "Fixed missing SQLITE dependency successfully."
fi

CHROMA_LOG_LEVEL=${CHROMA_LOG_LEVEL:-'INFO'}
if [ ${CHROMA_LOG_LEVEL}!='INFO' ]; then

    echo "Change log level to ${CHROMA_LOG_LEVEL}."
    # Define the path to the YAML file
    yaml_file="/home/cdsw/.local/lib/${PYTHON_DIR}/site-packages/chromadb/log_config.yml"

    # This command looks for a line containing 'uvicorn:' followed by any number of spaces and 'level: INFO'
    # and replaces it with 'level: DEBUG'
    sed -i "/uvicorn:/{n;s/level: INFO/level: $CHROMA_LOG_LEVEL/;}" "$yaml_file"
fi
