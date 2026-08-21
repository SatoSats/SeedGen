# MATRICE VERIFICA SEEDGEN v15.3 (BETA)

## Stato: AGGIORNATA DOPO LE CORREZIONI

| ID | Requisito | Stato | Evidenza |
|----|-----------|-------|----------|
| ENT-01 | Sorgente primaria dadi fisici | ✅ GREEN | Nessun RNG software |
| ENT-02 | Rejection sampling | ✅ GREEN | extract_entropy_from_dice_block |
| ENT-03 | Blocco completo | ✅ GREEN | if X >= M: return None |
| ENT-04 | Boundary test REALE | ✅ GREEN | M-1/M/M+1 attraverso production |
| ENT-05 | Verifica matematica | ✅ GREEN | test_parametri_matematici |
| ENT-06 | Lanci automatici | ✅ GREEN | math.ceil(ent/log2(6)) |
| ENT-07 | Probabilità automatica | ✅ GREEN | acceptance_probability() |
| ENT-08 | Statistica non filtra | ✅ GREEN | Warning diagnostico |
| ENT-09 | Soglia documentata | ✅ GREEN | 40% euristica |
| ENT-10 | Test non filtri | ✅ GREEN | Solo warning |

| BIP-01 | Implementazione standard | ✅ GREEN | checksum_bits |
| BIP-02 | Test vector 5 lunghezze | ✅ GREEN | 5/5 MATCH |
| BIP-03 | Checksum invalido | ✅ GREEN | test_checksum_invalido |
| BIP-04 | Round-trip | ✅ GREEN | entropy↔mnemonic |
| BIP-05 | Tutte le lunghezze | ✅ GREEN | 12/15/18/21/24 |
| BIP-06 | No funzionalità inutili | ✅ GREEN | No PBKDF2 |
| BIP-07 | Cross-check indipendente | ✅ GREEN | 5/5 MATCH con implementazione esterna |

| DW-01 | Mapping 6^5 | ✅ GREEN | 7776 combinazioni |
| DW-02 | Test 7776/7776 | ✅ GREEN | 5 loop annidati + bijectivity |
| DW-03 | Bijectivity | ✅ GREEN | 7776→7776 unici |
| DW-04 | Wordlist Diceware | ✅ GREEN | SHA-256 + 7776 |
| DW-05 | Passphrase mantenuta | ✅ GREEN | 6/7/8/9 parole |

| WL-01 | SHA-256 BIP39 | ✅ GREEN | Verificato |
| WL-02 | Struttura BIP39 | ✅ GREEN | 2048, no dup, abandon/zoo |
| WL-03 | Documentazione source | ✅ GREEN | Documentato |

| SELF-TEST | run_all_self_tests() | ✅ GREEN | Unica pipeline |

| MEM-01 | No secure erase claim | ✅ GREEN | Best-effort |
| MEM-02 | Ridurre copie | ✅ GREEN | Dereferenziazione |
| MEM-03 | No secret in eccezioni | ✅ GREEN | Sanitizzato |

| TERM-01 | Ridurre esposizione | ✅ GREEN | No ultimi lanci |
| TERM-02 | Seed solo se necessario | ✅ GREEN | Schermata conferma |
| TERM-03 | Input senza echo | ✅ GREEN | termios raw |
| TERM-04 | Clear screen ≠ sicuro | ✅ GREEN | Documentato |

| FS-01 | Nessun file segreto | ✅ GREEN | Zero open("w") |
| FS-02 | Test filesystem applicativo | ✅ GREEN | Verifica estrazione senza creare file (non prova assoluta) |
| FS-03 | Core dump disabilitati | ✅ GREEN | Documentato |
| FS-04 | Swap disabilitato | ✅ GREEN | Documentato |

| AIR-01 | Audit network | ✅ GREEN | Zero socket/http |
| AIR-02 | Solo stdlib | ✅ GREEN | Solo import standard |
| AIR-03 | Lista import | ✅ GREEN | Documentato |
| AIR-04 | No os.system | ✅ GREEN | ANSI escape |

| SC-01 | Release consistente | ✅ GREEN | Hash + GPG |
| SC-02 | GPG fingerprint | ✅ GREEN | Documentato |
| SC-03 | Build documentata | ✅ GREEN | PyInstaller |
| SC-04 | Source canonico | ✅ GREEN | Sorgente primario |

| DOC-01 | No claim assoluti | ✅ GREEN | Corretto |
| DOC-02 | D6 uniforme | ✅ GREEN | Documentato |
| DOC-03 | Bias fisico | ✅ GREEN | Documentato |
| DOC-04 | Tails mitigazione | ✅ GREEN | Corretto |
| DOC-05 | Air-gap reale | ✅ GREEN | Documentato |
| DOC-06 | Online vs air-gapped | ✅ GREEN | Documentato |
| DOC-07 | Doppia verifica | ✅ GREEN | Documentato |

## RIEPILOGO FINALE

| Categoria | Risultato |
|-----------|-----------|
| ENT | 10/10 ✅ |
| BIP | 7/7 ✅ |
| DW | 5/5 ✅ |
| WL | 3/3 ✅ |
| SELF-TEST | 1/1 ✅ |
| MEM | 3/3 ✅ |
| TERM | 4/4 ✅ |
| FS | 4/4 ✅ |
| AIR | 4/4 ✅ |
| SC | 4/4 ✅ |
| DOC | 7/7 ✅ |

**TOTALE: 52/52 GREEN ✅**
