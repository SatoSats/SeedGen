#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$DIR/seedgen-v1.0.2-linux-x86_64"

# Controllo architettura
ARCH="$(uname -m)"

if [ "$ARCH" != "x86_64" ]; then
    echo "=================================================="
    echo "SeedGen v1.0.2 richiede Linux x86_64 (64 bit)."
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

# Controllo versione GLIBC richiesta dal binario
REQUIRED_GLIBC_MAJOR=2
REQUIRED_GLIBC_MINOR=38
GLIBC_VERSION=""

if command -v getconf >/dev/null 2>&1; then
    if GLIBC_OUTPUT="$(getconf GNU_LIBC_VERSION 2>/dev/null)"; then
        GLIBC_VERSION="$(printf "%s\n" "$GLIBC_OUTPUT" | awk '{print $2}')"
    fi
fi

if [[ "$GLIBC_VERSION" =~ ^([0-9]+)\.([0-9]+) ]]; then
    GLIBC_MAJOR="${BASH_REMATCH[1]}"
    GLIBC_MINOR="${BASH_REMATCH[2]}"

    if (( GLIBC_MAJOR < REQUIRED_GLIBC_MAJOR ||
          (GLIBC_MAJOR == REQUIRED_GLIBC_MAJOR && GLIBC_MINOR < REQUIRED_GLIBC_MINOR) )); then
        echo "=================================================="
        echo "VERSIONE GLIBC NON COMPATIBILE"
        echo
        echo "SeedGen richiede GLIBC 2.38 o successiva."
        echo "Versione rilevata: GLIBC $GLIBC_VERSION"
        echo
        echo "La distribuzione Linux in uso è troppo vecchia"
        echo "per eseguire questa versione di SeedGen."
        echo "Questo non indica un malfunzionamento di SeedGen."
        echo
        echo "Aggiorna la distribuzione oppure utilizza"
        echo "una distribuzione Linux più recente."
        echo
        echo "Non aggiornare manualmente GLIBC separatamente dal sistema."
        echo "=================================================="
        read -r -p "Premi INVIO per chiudere..."
        exit 1
    fi
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
