# AUDIT SEEDGEN v15

## Hash dei File

| File | SHA-256 |
|------|---------|
| seedgen_simulazione_sicuro.py | 582971df61bd4b2accd8b319bd5c93df88cc342472c4ed9824fbfa7cb24a1445 |
| seedgen-v15-linux-x86_64 | b313851d1627c2d1ee1b45c3955ad7d2cc1274ddb0ca710a5045185beda8576c |
| bip39_wordlist.txt | 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda |
| diceware_wordlist.txt | addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e |

## GPG Fingerprint

Fingerprint: EA83 1AF9 D252 F9E4 43EE 6A1D ECD3 0979 3F79 E833

Chiave: chiave_pubblica_gpg.asc

## Verifica Offline

sha256sum -c seedgen-v15-linux-x86_64.sha256
gpg --verify seedgen-v15-linux-x86_64.asc seedgen-v15-linux-x86_64

## Test Vector BIP39

| Bit | Ultima parola |
|-----|---------------|
| 128 | about |
| 160 | address |
| 192 | agent |
| 224 | admit |
| 256 | art |
