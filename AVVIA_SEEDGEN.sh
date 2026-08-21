#!/bin/bash
# Launcher universale SeedGen v15.4

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

DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v gnome-terminal &> /dev/null; then
    gnome-terminal --geometry=${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} --wait --working-directory="$DIR" -- ./seedgen-v15.4-linux-x86_64
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal --geometry=${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} --working-directory="$DIR" --command="./seedgen-v15.4-linux-x86_64" &
elif command -v xterm &> /dev/null; then
    xterm -geometry ${TERM_W}x${TERM_H}+${POS_X}+${POS_Y} -e "$DIR/seedgen-v15.4-linux-x86_64" &
else
    echo "Terminale non trovato"
    echo "Esegui: $DIR/seedgen-v15.4-linux-x86_64"
fi
