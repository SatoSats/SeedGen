#!/usr/bin/env bash
set -euo pipefail
SEEDGEN_TAG="${SEEDGEN_TAG:-v1.0.2}"
SS_TAG="${SS_TAG:-0.8.7}"
BOARD_TYPE="${BOARD_TYPE:-pi0}"
BASE="${PWD}"; WORK="${BASE}/work"; SS_OS="${WORK}/seedsigner-os"; SS_APP="${WORK}/seedsigner-app"; SEEDGEN="${WORK}/SeedGen"; OUT="${BASE}/images"
mkdir -p "$WORK" "$OUT"
test "$BOARD_TYPE" = pi0
command -v git >/dev/null; command -v docker >/dev/null

echo "[1/8] Sources"
[ -d "$SEEDGEN/.git" ] || git clone --depth 1 --branch "$SEEDGEN_TAG" https://github.com/SatoSats/SeedGen.git "$SEEDGEN"
[ -d "$SS_OS/.git" ] || git clone --recursive --branch "$SS_TAG" https://github.com/SeedSigner/seedsigner-os.git "$SS_OS"
git -C "$SS_OS" submodule update --init --recursive
[ -d "$SS_APP/.git" ] || git clone --recurse-submodules --depth 1 --branch "$SS_TAG" https://github.com/SeedSigner/seedsigner.git "$SS_APP"

echo "[2/8] Verify bundled upstream"
SEEDGEN="$BASE/vendor"
(cd "$SEEDGEN" && shasum -a 256 -c SHA256SUMS)
# Fix the small boot image without deleting compiled components.
sed -i.bak 's/count=50/count=128/' "$SS_OS/opt/pi0/board/post-image-seedsigner.sh"
grep -q 'count=128' "$SS_OS/opt/pi0/board/post-image-seedsigner.sh"
echo "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda  $SEEDGEN/bip39_wordlist.txt" | shasum -a 256 -c -

echo "[3/8] Prepare overlay"
OVERLAY="$SS_OS/opt/rootfs-overlay"
test -d "$OVERLAY"
rm -rf "$OVERLAY/opt"; mkdir -p "$OVERLAY/opt"
cp -a "$SS_APP/." "$OVERLAY/opt/"

echo "[4/8] Install SeedGen-only entrypoint"
cp "$BASE/main.py" "$OVERLAY/opt/src/main.py"
cp "$BASE/password_tools.py" "$BASE/ui_views.py" "$BASE/i18n.py" "$OVERLAY/opt/src/"
mkdir -p "$OVERLAY/opt/src/fonts"
cp "$BASE/fonts/DejaVuSans.ttf" "$BASE/fonts/DejaVuSans-Bold.ttf" "$BASE/fonts/LICENSE.txt" "$OVERLAY/opt/src/fonts/"
mkdir -p "$OVERLAY/opt/src/seedgen_upstream"
cp "$SEEDGEN/seedgen.py" "$SEEDGEN/bip39_wordlist.txt" "$SEEDGEN/diceware_wordlist.txt" "$SEEDGEN/eff_short_wordlist_1.txt" "$SEEDGEN/LICENSE" "$SEEDGEN/EFF-ATTRIBUTION.txt" "$OVERLAY/opt/src/seedgen_upstream/"
printf "SEEDGEN_PI_V9_MARKER\nSeedGen=%s\nSeedSignerOS=%s\nBoard=%s\n" "$SEEDGEN_TAG" "$SS_TAG" "$BOARD_TYPE" > "$OVERLAY/opt/SEEDGEN_PI_BUILD_INFO.txt"

echo "[5/8] Verify custom entrypoint"
grep -q "SEEDGEN_PI_V9_MARKER" "$OVERLAY/opt/src/main.py"
! grep -q "Controller.get_instance().start()" "$OVERLAY/opt/src/main.py"
echo "SeedGen entrypoint OK"

rm -f "$SS_OS"/images/seedsigner_os.*.pi0.img
echo "[6/8] Build with official --skip-repo"
cd "$SS_OS"
export DOCKER_DEFAULT_PLATFORM=linux/amd64
export SS_ARGS="--${BOARD_TYPE} --skip-repo"
docker compose up --build --force-recreate --abort-on-container-exit --exit-code-from build-images

echo "[7/8] Collect image"
cd "$BASE"
BUILT="$(find "$SS_OS/images" -maxdepth 1 -type f -name 'seedsigner_os.*.pi0.img' | head -n1 || true)"
test -n "$BUILT"
FINAL="$OUT/seedgen_os.v1.0.2.pi0.v9.img"
cp "$BUILT" "$FINAL"
shasum -a 256 "$FINAL" | tee "$OUT/SHA256SUMS-v9"

echo "[8/8] DONE"
echo "$FINAL"
echo "Prototype only: test with throwaway entropy first."
