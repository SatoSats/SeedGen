# DOCUMENTAZIONE SICUREZZA - SEEDGEN v15.3 (BETA)

## DOC-01: Nessun claim assoluto
SeedGen non è "invulnerabile" o "perfetto". La sicurezza dipende da:
- Hardware
- Sistema operativo
- Dadi fisici
- Procedura operativa
- Ambiente fisico

## DOC-02: Rejection sampling
Il rejection sampling produce output uniforme **rispetto alla distribuzione D6 assunta uniforme**.

## DOC-03: Bias fisico
Il rejection sampling elimina il **modulo bias matematico** ma NON corregge un dado fisicamente non uniforme.

## DOC-04: Tails e RAM
Tails NON "cancella la RAM". È una **mitigazione operativa** contro la persistenza su storage.

## DOC-05: Air-gap reale
Air-gapped NON significa solo Wi-Fi off. Richiede:
- Rete fisicamente disconnessa
- Wi-Fi disabilitato
- Bluetooth disabilitato
- Nessuna interfaccia di rete attiva
- Nessuno swap
- Nessuno storage con segreti

## DOC-06: Macchina online vs air-gapped
- **Macchina online**: per scaricare, verificare hash, preparare
- **Macchina air-gapped**: per generare le seed
- MAI eseguire git clone sulla macchina air-gapped

## DOC-07: Doppia verifica
Verificare hash e firma:
1. Sulla macchina online
2. NUOVAMENTE sulla macchina air-gapped

---

## PROCEDURA OPERATIVA CONSIGLIATA

### Preparazione (macchina online)
1. Scaricare il repository
2. Verificare SHA-256 del codice sorgente
3. Verificare firma GPG
4. Verificare hash wordlist
5. Copiare su USB

### Generazione (macchina air-gapped)
1. Boot da sistema pulito
2. Disabilitare swap: `sudo swapoff -a`
3. Disabilitare core dump: `ulimit -c 0`
4. Scollegare rete fisica
5. Disabilitare Wi-Fi e Bluetooth
6. Verificare hash dalla USB
7. Verificare firma GPG
8. Eseguire SeedGen
9. Eseguire self-test completo
10. Generare la seed
11. Trascrivere su carta
12. Spegnere la macchina

### Dopo la generazione
1. Riavviare la macchina
2. Conservare la seed in luogo sicuro
3. Conservare la passphrase SEPARATAMENTE
4. NON fotografare
5. NON digitalizzare
