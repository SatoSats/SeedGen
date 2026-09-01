# CHANGELOG - SeedGen

## v1.0.2

### Modifiche

- Corretto il requisito minimo GLIBC del launcher da 2.14 a 2.38 per il binario Linux x86_64.
- Il requisito è stato verificato analizzando tutti i 20 componenti binari incorporati nella build PyInstaller `--onefile`, non soltanto l'eseguibile ELF esterno.
- `GLIBC_2.38` è il requisito massimo rilevato nella build v1.0.2.
- Il comportamento del launcher con GLIBC 2.35 è stato verificato anche su Linux Mint 21.1: SeedGen non tenta di avviare il binario incompatibile e mostra invece un messaggio chiaro di incompatibilità.
- Nessuna modifica alla generazione BIP39, alla generazione Diceware, alla gestione dell'entropia D6 o ai controlli di distribuzione dei lanci.

## v1.0.1

### Modifiche

- Aggiunto un controllo iniziale della raggiungibilità Internet: se Internet viene rilevato prima del menu principale, SeedGen avvisa l'utente e permette di continuare consapevolmente oppure chiudere il programma.
- Il controllo di raggiungibilità utilizza tentativi di connessione TCP verso endpoint pubblici sulla porta 443 e non trasmette mnemonic, passphrase o altri segreti.
- Aggiunto nel launcher il controllo della versione GLIBC prima dell'avvio del binario.
- Se la GLIBC rilevata è inferiore alla versione minima richiesta, il launcher mostra un messaggio di incompatibilità e non avvia il binario.
- Nella release v1.0.1 il requisito GLIBC era stato erroneamente determinato come GLIBC_2.14 controllando soltanto l’eseguibile ELF esterno. Un successivo audit dei componenti binari incorporati da PyInstaller ha rilevato requisiti fino a GLIBC_2.38; la correzione è introdotta in v1.0.2.

## v1.0.0

Prima release ufficiale della nuova serie SeedGen.

### Caratteristiche

- Generazione BIP39 da entropia fisica D6.
- Rejection sampling per l'estrazione uniforme dell'entropia.
- Generazione opzionale di passphrase Diceware.
- Verifica SHA-256 delle wordlist.
- Self-test all'avvio.
- Verifica obbligatoria della trascrizione.
- Binario Linux x86_64.
- Installer locale.
- Launcher grafico.
- Nessuna connessione di rete.
- Nessun RNG software per la generazione del segreto.

### Identità della release

Versione: `1.0.0`

SHA-256 sorgente:

`db687c2c9a9443f2588d9005e02f9eecb1291676a493f27a43566088455ea43a`

SHA-256 binario:

`43b18f0c53698ed4c16a7dee703a9a6033f379d6a85329a3d9f644476ec4d3c2`
