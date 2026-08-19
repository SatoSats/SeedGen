# THREAT MODEL - SEEDGEN v13

## Minacce e Mitigazioni

| Minaccia | Mitigazione |
|----------|-------------|
| Malware | Procedura (macchina dedicata) |
| Keylogger | Fuori scope |
| OS compromesso | Fuori scope |
| Firmware compromesso | Fuori scope |
| Hardware compromesso | Fuori scope |
| Dado non uniforme | Software (parziale) |
| Osservatore fisico | Procedura |
| Telecamera | Procedura |
| Supporto software | Software (SHA-256) |
| Errore umano | Procedura |
| Perdita seed | Fuori scope |
| Perdita passphrase | Fuori scope |
| Swap file | Procedura (disabilitato) |
| Core dump | Procedura (disabilitati) |
| Hibernation | Procedura (disabilitata) |
| Shell history | Software (nessun segreto) |
| Clipboard | Software (zero uso) |
| Network | Software (zero networking) |
| Screen capture | Procedura |
| Cold boot | Fuori scope |

## Conclusione

SeedGen mitiga direttamente:
- Bias conversione D6-bit (rejection sampling)
- Networking (zero codice)
- Clipboard (zero uso)
- Wordlist compromesse (SHA-256)

La sicurezza finale dipende dalla PROCEDURA.
