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

## Verifica del pacchetto della prova hardware

- Immagine: `seedgen_os.v1.0.2.pi0.v9.img` (128 MiB).
- SHA-256 dell’immagine: `2c5a7b149c56484de70dfe7213f52ba81a9c05fd4dbbda07618636e999b654de`.
- SHA-256 dello ZIP ricevuto: `eb24913bf0d4cf9b076905b11bf87081de39a9c3f7491efda0f3c938c1394852`.
- Firma OpenPGP di `SHA256SUMS` verificata il 28 novembre 2026 con l’impronta `3F4E3C778F5D63EC1B0985F85823FC25A5186930`, già documentata per la release Pi v9.4.

`gpg --verify SHA256SUMS.asc SHA256SUMS` ha confermato la firma. `shasum -a 256 -c SHA256SUMS` ha confermato che l’immagine corrisponde al manifest firmato. La verifica del pacchetto si affianca alla prova funzionale riferita dal manutentore. Il pacchetto è stato consegnato per la verifica e non ha un link pubblico di download.
