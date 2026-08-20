#!/bin/bash
# ============================================================
# LAUNCHER UNIVERSALE SEEDGEN
# Compatibile: Ubuntu, Debian, Linux Mint, Tails, Fedora, Arch
# Centratura automatica su qualsiasi risoluzione
# ============================================================

# Rileva dimensioni schermo con multipli fallback
if command -v xdpyinfo &> /dev/null; then
    SCREEN_W=$(xdpyinfo | grep dimensions | awk '{print $2}' | cut -d'x' -f1)
    SCREEN_H=$(xdpyinfo | grep dimensions | awk '{print $2}' | cut -d'x' -f2)
elif command -v xrandr &> /dev/null; then
    SCREEN_W=$(xrandr --current | grep '*' | awk '{print $1}' | cut -d'x' -f1 | head -1)
    SCREEN_H=$(xrandr --current | grep '*' | awk '{print $1}' | cut -d'x' -f2 | head -1)
elif command -v wmctrl &> /dev/null; then
    SCREEN_W=$(wmctrl -d | awk '{print $4}' | cut -d'x' -f1 | head -1)
    SCREEN_H=$(wmctrl -d | awk '{print $4}' | cut -d'x' -f2 | head -1)
else
    SCREEN_W=1920
    SCREEN_H=1080
fi

# Dimensione terminale FISSA
TERM_W=110
TERM_H=45

# Calcola posizione centrata
POS_X=$(( (SCREEN_W - TERM_W * 8) / 2 ))
POS_Y=$(( (SCREEN_H - TERM_H * 16) / 2 ))

# Assicura posizioni positive
[ $POS_X -lt 0 ] && POS_X=0
[ $POS_Y -lt 0 ] && POS_Y=0

# Directory del programma
DIR="$(cd "$(dirname "$0")" && pwd)"

# Apri il terminale con supporto per TUTTI i terminali Linux
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal --geometry=${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} -- bash -c "cd '$DIR' && python3 seedgen_simulazione_sicuro.py; exec bash"
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal --geometry=${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} --command="cd '$DIR' && python3 seedgen_simulazione_sicuro.py" &
elif command -v konsole &> /dev/null; then
    konsole --geometry ${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} -e bash -c "cd '$DIR' && python3 seedgen_simulazione_sicuro.py" &
elif command -v lxterminal &> /dev/null; then
    lxterminal --geometry=${TERM_W}x${TERM_H} --working-directory="$DIR" -e "python3 seedgen_simulazione_sicuro.py" &
elif command -v xterm &> /dev/null; then
    xterm -geometry ${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} -e "cd '$DIR' && python3 seedgen_simulazione_sicuro.py" &
else
    echo "Nessun terminale grafico trovato"
    echo "Esegui manualmente:"
    echo "  cd $DIR"
    echo "  python3 seedgen_simulazione_sicuro.py"
    exit 1
fi
