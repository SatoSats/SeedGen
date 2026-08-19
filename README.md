# SeedGen v14

Generatore air-gapped di seed Bitcoin BIP39 e passphrase Diceware con entropia fisica da dadi (D6).

## Perché SeedGen?

La sicurezza di un wallet Bitcoin dipende interamente dalla qualità dell'entropia usata per generare il seed. I generatori software usano RNG di sistema che potrebbero essere compromessi, manipolati o semplicemente deboli. SeedGen elimina questo rischio usando **solo entropia fisica da dadi**.

## Principi di progettazione

| Principio | Implementazione |
|-----------|----------------|
| **Zero networking** | Nessuna chiamata di rete, nessuna API, nessun socket |
| **Zero logging** | Nessun file di log, nessun output su disco |
| **Zero RNG di sistema** | Nessun uso di random, os.urandom o simili |
| **Entropia fisica** | Solo lanci di dadi D6 (6 facce) |
| **Rejection sampling** | Estrazione entropia uniforme senza bias |
| **Verifica integrità** | SHA-256 delle wordlist prima dell'uso |

## Come funziona

### 1. Raccolta entropia

L'utente lancia un dado fisico a 6 facce. Ogni lancio produce un valore da 1 a 6, che viene convertito in **2,58 bit di entropia** (log2(6) = 2,585).

### 2. Rejection sampling

Per evitare bias nella conversione, il programma usa il **rejection sampling**:
- I valori del dado vengono raggruppati in blocchi
- I blocchi che eccedono l'intervallo uniforme vengono scartati
- Questo garantisce che ogni possibile output abbia **esattamente la stessa probabilità**

### 3. Generazione seed

L'entropia raccolta viene convertita in:
- **Seed BIP39**: 12, 15, 18, 21 o 24 parole (128-256 bit)
- **Passphrase Diceware**: 6, 7, 8 o 9 parole (~77-116 bit)

### 4. Verifica wordlist

Prima di ogni generazione, il programma verifica l'hash SHA-256 delle wordlist per garantire che non siano state manomesse.

## Entropia richiesta

| Tipo | Parole | Entropia | Lanci di dado (min) |
|------|--------|----------|---------------------|
| BIP39 | 12 | 128 bit | 50 |
| BIP39 | 15 | 160 bit | 62 |
| BIP39 | 18 | 192 bit | 75 |
| BIP39 | 21 | 224 bit | 87 |
| BIP39 | 24 | 256 bit | 100 |
| Diceware | 6 | ~77,5 bit | 30 |
| Diceware | 7 | ~90,4 bit | 35 |
| Diceware | 8 | ~103,3 bit | 40 |
| Diceware | 9 | ~116,2 bit | 45 |

*I numeri di lanci sono arrotondati per eccesso e tengono conto del rejection sampling.*

## Requisiti

- Python 3.8+ (nessuna dipendenza esterna)
- Sistema air-gapped (es. Raspberry Pi)
- Dadi fisici (D6)
- Terminale

## Installazione

git clone https://github.com/SatoSats/SeedGen.git
cd SeedGen

## Utilizzo

python3 seedgen_simulazione_sicuro.py

## Verifica integrità

Hash SHA-256 del programma:

df6595c3b9e71f48361053db60524cbdd6fd17a0d26cb0e87653889698caf311

Per verificare:
sha256sum seedgen_simulazione_sicuro.py

## Struttura del progetto

| File | Contenuto |
|------|-----------|
| seedgen_simulazione_sicuro.py | Programma principale |
| bip39_wordlist.txt | Wordlist BIP39 ufficiale (2048 parole) |
| diceware_wordlist.txt | Wordlist Diceware EFF (7776 parole) |
| THREAT_MODEL.md | Modello delle minacce dettagliato |
| AUDIT_SEEDGEN.md | Guida per l'audit indipendente |
| COLD_STORAGE_PROCEDURE.md | Procedura operativa per cold storage |
| SPECIFICATION.md | Analisi matematica completa |

## Documentazione tecnica

- THREAT_MODEL.md: Analisi delle minacce e contromisure adottate
- AUDIT_SEEDGEN.md: Procedura passo-passo per verificare il codice e le wordlist
- COLD_STORAGE_PROCEDURE.md: Procedura operativa per usare SeedGen in cold storage
- SPECIFICATION.md: Analisi matematica completa con calcolo entropia, dimostrazione uniformità, verifica rejection sampling, test vector BIP39

## Sicurezza operativa

### Cosa fare
- Usare solo su sistema air-gapped
- Verificare sempre gli hash SHA-256
- Trascrivere il seed su supporto fisico
- Distruggere l'ambiente dopo l'uso

### Cosa NON fare
- Non usare su sistemi connessi a rete
- Non salvare il seed su dispositivi elettronici
- Non fotografare il seed
- Non modificare le wordlist senza verifica

## Licenza

MIT - vedi file LICENSE

## Verifica finale

Prima di usare SeedGen per fondi reali:
1. Verifica gli hash SHA-256
2. Fai un audit completo del codice
3. Testa con importi minimi
4. Verifica i test vector BIP39
5. Leggi tutta la documentazione

**Non usare per fondi reali senza aver completato tutti i passaggi di verifica.**


## Verifica con firma GPG

### Chiave pubblica

ID chiave: EA831AF9D252F9E443EE6A1DECD309793F79E833
Impronta: EA83 1AF9 D252 F9E4 43EE 6A1D ECD3 0979 3F79 E833

### Importare la chiave pubblica

gpg --keyserver keys.openpgp.org --recv-keys EA831AF9D252F9E443EE6A1DECD309793F79E833

Oppure scaricare il file chiave_pubblica_gpg.asc e importarlo:

gpg --import chiave_pubblica_gpg.asc

### Verificare la firma del programma

gpg --verify seedgen_simulazione_sicuro.py.asc seedgen_simulazione_sicuro.py

### Verificare hash SHA-256

sha256sum seedgen_simulazione_sicuro.py

L'hash deve corrispondere a:
df6595c3b9e71f48361053db60524cbdd6fd17a0d26cb0e87653889698caf311


## Requisiti di Sicurezza ed Esecuzione

Per annullare i rischi legati alla memoria RAM e ai file di swap del sistema operativo, **SeedGen v14** deve essere eseguito esclusivamente in ambienti isolati (*Air-Gapped*).

### 1. Ambiente Consigliato

- **Tails OS (Live USB):** Avvia il PC tramite Tails in modalità offline. Tails esegue lo script totalmente in RAM e la cancella all'arresto.
- **Zero Swap:** L'assenza di dischi rigidi montati impedisce la scrittura temporanea dell'entropia su disco.

### 2. Prevenzione Bias Fisico

- Il Rejection Sampling elimina il *modulo bias* matematico.
- Utilizza sempre dadi di precisione/casinò per evitare bias meccanici della plastica.

### 3. Roadmap Futura

È in fase di valutazione il porting della logica di Rejection Sampling su microcontrollori dedicati (Rust/C++ su Raspberry Pi Pico) per realizzare un generatore hardware indipendente privo di sistema operativo.

---

## Verifica del Binario (Linux x86_64)

### Download
Scarica il binario e i file di verifica:
- seedgen-v14-linux-x86_64 (7.2 MB)
- seedgen-v14-linux-x86_64.sha256
- seedgen-v14-linux-x86_64.asc

### Verifica SHA-256
sha256sum -c seedgen-v14-linux-x86_64.sha256

### Verifica Firma GPG
gpg --import chiave_pubblica_gpg.asc
gpg --verify seedgen-v14-linux-x86_64.asc seedgen-v14-linux-x86_64

### Esecuzione
chmod +x seedgen-v14-linux-x86_64
./seedgen-v14-linux-x86_64

Nota: eseguire dalla cartella con le wordlist.


## Build Binaria (Linux x86_64)

Per chi preferisce non eseguire lo script Python, è disponibile una build isolata pronta all'uso.

### Download

Scarica dalla release v14:
- seedgen-v14-linux-x86_64.tar.gz
- seedgen-v14-linux-x86_64.tar.gz.asc

### Verifica

Importa la chiave pubblica GPG:
gpg --keyserver keys.openpgp.org --recv-keys EA831AF9D252F9E443EE6A1DECD309793F79E833

Verifica la firma dell'archivio:
gpg --verify seedgen-v14-linux-x86_64.tar.gz.asc seedgen-v14-linux-x86_64.tar.gz

Verifica hash SHA-256:
sha256sum seedgen-v14-linux-x86_64.tar.gz

Hash atteso:
c2b74cc300b84b834d8b70186ce3d815f344ac9052d68c70efbc1d84b74a61aa

### Installazione

tar -xzvf seedgen-v14-linux-x86_64.tar.gz
cd dist
./seedgen-v14-linux-x86_64

Oppure usa il file SeedGen.desktop per avviare il programma con un click.
