#!/bin/bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APP_DIR="$HOME/.local/share/seedgen"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

BIN_NAME="seedgen-v1.0.1-linux-x86_64"

echo
echo "========================================"
echo "        INSTALLAZIONE SEEDGEN"
echo "========================================"
echo

echo "Sorgente:"
echo "  $SRC_DIR"
echo

echo "Destinazione:"
echo "  $APP_DIR"
echo

mkdir -p "$APP_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

echo "Copio i file di SeedGen..."

cp "$SRC_DIR/$BIN_NAME" "$APP_DIR/$BIN_NAME"
cp "$SRC_DIR/AVVIA_SEEDGEN.sh" "$APP_DIR/AVVIA_SEEDGEN.sh"
cp "$SRC_DIR/INSTALLA_SEEDGEN.sh" "$APP_DIR/INSTALLA_SEEDGEN.sh"
cp "$SRC_DIR/bip39_wordlist.txt" "$APP_DIR/bip39_wordlist.txt"
cp "$SRC_DIR/diceware_wordlist.txt" "$APP_DIR/diceware_wordlist.txt"
cp "$SRC_DIR/seedgen-icon.svg" "$ICON_DIR/seedgen-icon.svg"

chmod 755 "$APP_DIR/$BIN_NAME"
chmod 755 "$APP_DIR/AVVIA_SEEDGEN.sh"
chmod 755 "$APP_DIR/INSTALLA_SEEDGEN.sh"
chmod 644 "$APP_DIR/bip39_wordlist.txt"
chmod 644 "$APP_DIR/diceware_wordlist.txt"
chmod 644 "$ICON_DIR/seedgen-icon.svg"

cat > "$DESKTOP_DIR/seedgen.desktop" <<DESKTOP
[Desktop Entry]
Name=SeedGen v1.0.1
Comment=Generatore offline BIP39 e passphrase Diceware
Exec=$APP_DIR/AVVIA_SEEDGEN.sh
Icon=$ICON_DIR/seedgen-icon.svg
Type=Application
Terminal=true
Categories=Utility;Security;
DESKTOP

chmod 644 "$DESKTOP_DIR/seedgen.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo
echo "========================================"
echo "     INSTALLAZIONE COMPLETATA"
echo "========================================"
echo
echo "SeedGen installato in:"
echo "  $APP_DIR"
echo
echo "Launcher:"
echo "  $DESKTOP_DIR/seedgen.desktop"
echo
echo "Icona:"
echo "  $ICON_DIR/seedgen-icon.svg"
echo
echo "SeedGen è ora disponibile nel menu Applicazioni."
echo
