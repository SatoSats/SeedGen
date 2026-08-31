#!/bin/bash
set -euo pipefail

VERSION="1.0.1"
NAME="seedgen-v${VERSION}-linux-x86_64"
EXPECTED_SOURCE_SHA256="9e0257cfabdfad75274f8572569d52551aff6e3ecd4906d487ec77bc38001d98"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_ROOT="/tmp/seedgen-v1.0.1-build-scripted"

cd "$ROOT_DIR"

export PYTHONHASHSEED=1

ACTUAL_SOURCE_SHA256="$(sha256sum seedgen.py | cut -d" " -f1)"
echo "Hash sorgente: $ACTUAL_SOURCE_SHA256"

if [ "$ACTUAL_SOURCE_SHA256" != "$EXPECTED_SOURCE_SHA256" ]; then
    echo "ERRORE: hash seedgen.py diverso da quello congelato per v1.0.1" >&2
    exit 1
fi

rm -rf "$BUILD_ROOT"
mkdir -p "$BUILD_ROOT/dist" "$BUILD_ROOT/work" "$BUILD_ROOT/spec"

pyinstaller \
  --clean \
  --noconfirm \
  --onefile \
  --noupx \
  --console \
  --name "$NAME" \
  --distpath "$BUILD_ROOT/dist" \
  --workpath "$BUILD_ROOT/work" \
  --specpath "$BUILD_ROOT/spec" \
  "$ROOT_DIR/seedgen.py"

echo "Build completato: $BUILD_ROOT/dist/$NAME"
sha256sum "$BUILD_ROOT/dist/$NAME"
