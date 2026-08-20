# AUDIT SEEDGEN v15

## Hash dei File

| File | SHA-256 |
|------|---------|
| seedgen_simulazione_sicuro.py | 6774d20716a8d653afbcac77abb05246e12c76abd75aae31763a9397abd4de7b |
| seedgen-v15-linux-x86_64 | 932fc6df6f8162f701cf2dcc50264eebc13286a9c360f58898571ed2f205b776 |
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
