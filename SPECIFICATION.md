# SeedGen v15.4 (BETA) - Specifica Tecnica

## Panoramica
SeedGen genera seed Bitcoin BIP39 e passphrase Diceware usando esclusivamente entropia fisica da lanci di dadi a 6 facce (D6).

## Algoritmo di Estrazione Entropia

### Input
- N lanci di un dado a 6 facce (valori 1-6)
- Target: 128, 160, 192, 224 o 256 bit di entropia

### Passo 1: Conversione Base-6
Ogni lancio viene convertito sottraendo 1:
dado 1 = 0, dado 2 = 1, ..., dado 6 = 5

La sequenza completa diventa un numero in base 6:
X = (((d1-1) x 6 + (d2-1)) x 6 + ... + (dn-1))

### Passo 2: Calcolo Capacita
k = floor(log2(6^N))
M = 2^k

### Passo 3: Rejection Sampling
Se X >= M: RIFIUTA il blocco completo
Se X < M: ACCETTA (X uniforme su [0, 2^k - 1])

### Passo 4: Estrazione Bit
mask = (1 << target_bits) - 1
entropy = X & mask

## Parametri BIP39

| Entropia | Lanci | Checksum | Parole |
|----------|-------|----------|--------|
| 128 bit  | 50    | 4 bit    | 12     |
| 160 bit  | 62    | 5 bit    | 15     |
| 192 bit  | 75    | 6 bit    | 18     |
| 224 bit  | 87    | 7 bit    | 21     |
| 256 bit  | 100   | 8 bit    | 24     |

## Probabilita di Accettazione

| Entropia | P(accettazione) |
|----------|-----------------|
| 128 bit  | 84.2%           |
| 160 bit  | 83.1%           |
| 192 bit  | 54.6%           |
| 224 bit  | 53.9%           |
| 256 bit  | 70.9%           |

## Algoritmo Diceware

Formula indice: indice = somma(d_i - 1) x 6^(4-i) + 1
Range: 1-7776
5 lanci per parola
6^5 = 7776 combinazioni
Entropia per parola: log2(7776) = 12.925 bit

| Parole | Entropia |
|--------|----------|
| 6      | 77.55 bit |
| 7      | 90.47 bit |
| 8      | 103.40 bit |
| 9      | 116.32 bit |

## Verifiche Integrita

- SHA-256 wordlist BIP39
- SHA-256 wordlist Diceware
- Test vector BIP39 (5 lunghezze)
- Boundary test rejection sampling
- Mapping Diceware completo
- Warning distribuzione anomala

## Requisiti di Sistema

- Python 3.6+
- Linux/macOS
- Nessuna dipendenza esterna
- Nessun accesso di scrittura
- Nessuna connessione di rete

## Hash di Verifica

Programma: a5d904e2e9300e5288fab66ac94a1fb0fe7803a534582f2883a4c90c0d4a99da
BIP39: 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda
Diceware: addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e

## Limitazioni

1. Il rejection sampling NON elimina il bias fisico dei dadi
2. Python non garantisce cancellazione sicura della RAM
3. Swap/core dump devono essere disabilitati esternamente
4. La passphrase va conservata separatamente dalla seed
