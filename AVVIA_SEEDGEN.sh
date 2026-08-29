#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$DIR/seedgen-v1.0.0-linux-x86_64"

# Controllo architettura
ARCH="$(uname -m)"

if [ "$ARCH" != "x86_64" ]; then
    echo "=================================================="
    echo "SeedGen v1.0.0 richiede Linux x86_64 (64 bit)."
    echo
    echo "Architettura rilevata: $ARCH"
    echo "=================================================="
    read -r -p "Premi INVIO per chiudere..."
    exit 1
fi

# Controllo presenza binario
if [ ! -f "$BIN" ]; then
    echo "Errore: binario SeedGen non trovato:"
    echo "$BIN"
    read -r -p "Premi INVIO per chiudere..."
    exit 1
fi

chmod 755 "$BIN"

TERM_W=110
TERM_H=45

if command -v xdpyinfo >/dev/null 2>&1; then
    SCREEN_W="$(xdpyinfo | awk '/dimensions:/{print $2}' | cut -d'x' -f1)"
    SCREEN_H="$(xdpyinfo | awk '/dimensions:/{print $2}' | cut -d'x' -f2)"
else
    SCREEN_W=1920
    SCREEN_H=1080
fi

POS_X=$(( (SCREEN_W - TERM_W * 8) / 2 ))
POS_Y=$(( (SCREEN_H - TERM_H * 16) / 2 ))

[ "$POS_X" -lt 0 ] && POS_X=0
[ "$POS_Y" -lt 0 ] && POS_Y=0

if command -v gnome-terminal >/dev/null 2>&1; then
    exec gnome-terminal \
        --geometry="${TERM_W}x${TERM_H}+${POS_X}+${POS_Y}" \
        --working-directory="$DIR" \
        -- "$BIN"
elif command -v kgx >/dev/null 2>&1; then
    exec kgx \
        --working-directory="$DIR" \
        -e "$BIN"
elif command -v xfce4-terminal >/dev/null 2>&1; then
    exec xfce4-terminal \
        --geometry="${TERM_W}x${TERM_H}+${POS_X}+${POS_Y}" \
        --working-directory="$DIR" \
        -e "$BIN"
elif command -v xterm >/dev/null 2>&1; then
    exec xterm \
        -geometry "${TERM_W}x${TERM_H}+${POS_X}+${POS_Y}" \
        -e "cd \"$DIR\" && exec \"$BIN\""
else
    echo "Terminale grafico non trovato."
    echo
    echo "Avvia manualmente:"
    echo "$BIN"
    read -r -p "Premi INVIO per chiudere..."
    exit 1
fi
