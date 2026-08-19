# SeedGen v14

Generatore air-gapped di seed Bitcoin BIP39 e passphrase Diceware con entropia fisica da dadi (D6).

## Caratteristiche

- **Zero networking**: nessuna connessione di rete
- **Zero logging**: nessun log su disco
- **Zero RNG di sistema**: entropia solo da dadi fisici
- **Rejection sampling**: estrazione entropia uniforme
- **Verifica SHA-256** delle wordlist
- **Test vector BIP39** completi
- **Documentazione completa**: threat model, audit, procedura operativa

## Generazione supportata

| Tipo | Parole | Entropia |
|------|--------|----------|
| BIP39 | 12/15/18/21/24 | 128-256 bit |
| Diceware | 6/7/8/9 | ~77-116 bit |

## Requisiti

- Python 3.8+
- Sistema air-gapped (es. Raspberry Pi)
- Dadi fisici (D6)

## Utilizzo

python3 seedgen_simulazione_sicuro.py

## Verifica wordlist

Il programma verifica automaticamente l'hash SHA-256 delle wordlist prima dell'uso.

## Documentazione

- THREAT_MODEL.md - Modello delle minacce
- AUDIT_SEEDGEN.md - Guida all'audit
- COLD_STORAGE_PROCEDURE.md - Procedura operativa
- ANALISI_COMPLETA_SEEDGEN_v14.txt - Analisi matematica completa

## Verifica integrità

Hash SHA-256 del programma:
fd2459f18c8115cfcfa30e13617f10afb1be17fc827cfbb29f3b7e79aa124d5e

## Licenza

MIT - vedi file LICENSE

## Contributi

Pull request e audit indipendenti sono benvenuti.
