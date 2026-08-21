#!/bin/bash
# Launcher universale SeedGen - scrollback disabilitato

if command -v xdpyinfo &> /dev/null; then
    SCREEN_W=$(xdpyinfo | grep dimensions | awk '{print $2}' | cut -d'x' -f1)
    SCREEN_H=$(xdpyinfo | grep dimensions | awk '{print $2}' | cut -d'x' -f2)
else
    SCREEN_W=1920
    SCREEN_H=1080
fi

TERM_W=110
TERM_H=45
POS_X=$(( (SCREEN_W - TERM_W * 8) / 2 ))
POS_Y=$(( (SCREEN_H - TERM_H * 16) / 2 ))
[ $POS_X -lt 0 ] && POS_X=0
[ $POS_Y -lt 0 ] && POS_Y=0

# Usa --working-directory (evita interpolazione shell)
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal --geometry=${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} --wait --working-directory="$PWD" -- python3 seedgen_simulazione_sicuro.py
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal --geometry=${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} --working-directory="$PWD" --command="python3 seedgen_simulazione_sicuro.py" &
elif command -v xterm &> /dev/null; then
    xterm -geometry ${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} -e "cd '$PWD' && python3 seedgen_simulazione_sicuro.py" &
else
    echo "Terminale non trovato"
    echo "Esegui: python3 seedgen_simulazione_sicuro.py"
fi
