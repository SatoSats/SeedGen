#!/bin/bash
set -e
echo "=== BUILD SEEDGEN ==="
HASH_SORGENTE=$(sha256sum seedgen_simulazione_sicuro.py | cut -d' ' -f1)
echo "Hash sorgente: $HASH_SORGENTE"
pyinstaller --onefile --name seedgen-v15-linux-x86_64 seedgen_simulazione_sicuro.py
echo "Build completato!"
