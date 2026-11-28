# Verifiche del Test del dado

## Test host

Linux, CPython 3.12.14 e Pillow 13.0.0. Verifiche eseguite sul checkout con le modifiche della PR, basato sul commit upstream 8f24cd97e66cf25f2ab59acbc0ad98e7695a70fc.

Dalla cartella raspberry/240x240:

```bash
shasum -a 256 -c SOURCE-SHA256SUMS
bash -n build-v9.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_ui test_passwords test_navigation
```

Manifest e sintassi verificati. La suite ha eseguito 58 test con esito OK. Verifiche mirate aggiuntive su D6, D8 e D16 hanno coperto il movimento fino all’ultima faccia, la conferma, il mantenimento della selezione, l’annullamento di un lancio e la distinzione tra conteggi uniformi ed estremamente sbilanciati.

## Prova hardware

Il manutentore ha confermato il funzionamento dell’ultima immagine con la griglia sul Raspberry Pi. Profilo della build: Pi Zero v1.3 con display Waveshare ST7789 240×240. La build locale su Mac è stata preparata a partire dal commit del fork 994d3a6e55f4e17021c67f164ca91dca01bb5540 applicando seedgen-pi-test-dado-griglia.patch, SHA-256 ca37b333415208db74cba107fb2352e1d972360653a3cd2e8c216c8f802b79b7. I file applicativi modificati (main.py, ui_views.py e i18n.py) coincidono byte per byte tra la patch sul fork e questa PR.

Lo SHA-256 della specifica immagine provata, il manifest firmato e l’eventuale link di release sono da aggiungere dopo aver ricevuto e verificato gli asset della build. La conferma hardware riguarda il funzionamento.
