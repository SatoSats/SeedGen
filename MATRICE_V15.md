# MATRICE VERIFICA SEEDGEN v15

## ENT - ENTROPY PIPELINE

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| ENT-01 | Sorgente primaria dadi fisici | ✅ GREEN | Nessun RNG software nel codice |
| ENT-02 | Rejection sampling | ✅ GREEN | Funzione `extract_entropy_from_dice_block` |
| ENT-03 | Blocco completo accettato/rifiutato | ✅ GREEN | `if X >= M: return None` |
| ENT-04 | Boundary test reale | ✅ GREEN | `test_rejection_boundary()` |
| ENT-05 | Verifica matematica indipendente | ✅ GREEN | `test_parametri_matematici()` |
| ENT-06 | Numero lanci corretto | ✅ GREEN | DICE_ROLLS verificato |
| ENT-07 | Acceptance probability | ✅ GREEN | Probabilità 84/83/55/54/71% |
| ENT-08 | Statistica non modifica entropia | ✅ GREEN | Warning diagnostico |
| ENT-09 | Soglia documentata | ✅ GREEN | 40% euristica |
| ENT-10 | Test statistici non filtri | ✅ GREEN | Solo warning |

## BIP - BIP39

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| BIP-01 | Implementazione standard | ✅ GREEN | checksum_bits + entropy_to_mnemonic |
| BIP-02 | Test vector ufficiali | ✅ GREEN | 5 lunghezze testate |
| BIP-03 | Checksum invalido | ✅ GREEN | `test_checksum_invalido()` |
| BIP-04 | Round-trip | ✅ GREEN | entropy↔mnemonic verificato |
| BIP-05 | Tutte le lunghezze | ✅ GREEN | 12/15/18/21/24 |
| BIP-06 | No funzionalità inutili | ✅ GREEN | Solo BIP39 essenziale |
| BIP-07 | Cross-check indipendente | ⚠️ DA FARE | Richiede seconda implementazione |

## DW - DICEWARE

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| DW-01 | Mapping 6^5 | ✅ GREEN | 7776 combinazioni |
| DW-02 | Test 7776/7776 | ✅ GREEN | `test_diceware_completo()` |
| DW-03 | Bijectivity | ✅ GREEN | 7776 input → 7776 indici |
| DW-04 | Wordlist Diceware | ✅ GREEN | SHA-256 + 7776 parole |
| DW-05 | Passphrase mantenuta | ✅ GREEN | 6/7/8/9 parole |

## WL - WORDLIST

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| WL-01 | SHA-256 BIP39 | ✅ GREEN | Verificato all'avvio |
| WL-02 | Struttura BIP39 | ✅ GREEN | 2048, no duplicati, abandon/zoo |
| WL-03 | Documentazione source | ✅ GREEN | Documentato in SPECIFICATION |

## MEM - MEMORIA

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| MEM-01 | No secure erase claim | ✅ GREEN | Best-effort dichiarato |
| MEM-02 | Ridurre copie | ✅ GREEN | Variabili dereferenziate |
| MEM-03 | No secret in eccezioni | ✅ GREEN | Messaggi sanitizzati |

## TERM - TERMINALE

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| TERM-01 | Ridurre esposizione lanci | ✅ GREEN | Ultimi 10 mostrati |
| TERM-02 | Seed solo se necessario | ✅ GREEN | Schermata conferma |
| TERM-03 | Input senza echo | ✅ GREEN | termios raw mode |
| TERM-04 | Clear screen ≠ sicuro | ✅ GREEN | Documentato |

## FS - FILESYSTEM

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| FS-01 | Nessun file segreto | ✅ GREEN | Zero open("w") |
| FS-02 | Test before/after | ✅ GREEN | test_filesystem() verifica directory vuota |
| FS-03 | Core dump disabilitati | ✅ GREEN | Documentato in procedura |
| FS-04 | Swap disabilitato | ✅ GREEN | Documentato in procedura |

## AIR - AIR-GAP

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| AIR-01 | Audit statico network | ✅ GREEN | Zero socket/http |
| AIR-02 | Solo stdlib | ✅ GREEN | Solo import standard |
| AIR-03 | Lista import | ✅ GREEN | Documentato |
| AIR-04 | No os.system | ✅ GREEN | ANSI escape |

## SC - SUPPLY CHAIN

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| SC-01 | Release consistente | ✅ GREEN | Hash + GPG |
| SC-02 | GPG fingerprint | ✅ GREEN | Chiave pubblicata |
| SC-03 | Build documentata | ✅ GREEN | PyInstaller documentato |
| SC-04 | Source canonico | ✅ GREEN | Codice sorgente primario |

---

## RIEPILOGO FINALE

| Categoria | GREEN | DA FARE |
|-----------|-------|---------|
| ENT | 10/10 | 0 |
| BIP | 6/7 | 1 (BIP-07) |
| DW | 5/5 | 0 |
| WL | 3/3 | 0 |
| MEM | 3/3 | 0 |
| TERM | 4/4 | 0 |
| FS | 3/4 | 1 (FS-02) |
| AIR | 4/4 | 0 |
| SC | 4/4 | 0 |

**TOTALE: 42/44 GREEN - 2 DA FARE**
