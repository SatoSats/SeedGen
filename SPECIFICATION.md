# SPECIFICHE TECNICHE - SEEDGEN v1.0.0

## 1. Scopo

SeedGen è un generatore offline di mnemonic BIP39 ottenute da entropia fisica generata tramite dadi D6.

Il programma può inoltre generare passphrase basate su Diceware.

SeedGen non è un wallet e non gestisce fondi o transazioni.

## 2. Entropia

L'entropia primaria viene fornita esclusivamente dai lanci fisici di dadi D6.

La conversione dei risultati utilizza rejection sampling.

Questo evita di introdurre bias dovuto alla diversa rappresentazione delle potenze di due rispetto alle sei facce del dado.

## 3. BIP39

SeedGen supporta le lunghezze standard di entropia BIP39:

- 128 bit;
- 160 bit;
- 192 bit;
- 224 bit;
- 256 bit.

Per ogni lunghezza viene calcolato il checksum SHA-256 previsto da BIP39 e l'entropia viene convertita nella mnemonic corrispondente utilizzando la wordlist BIP39 inglese.

## 4. Verifica BIP39

Il programma include test vettoriali BIP39 e verifica:

- conversione entropia → mnemonic;
- conversione mnemonic → entropia;
- correttezza del checksum;
- rifiuto di mnemonic con checksum non valido.

## 5. Diceware

SeedGen può generare passphrase utilizzando una wordlist Diceware.

La wordlist viene verificata prima dell'utilizzo.

Sono controllati formato, codici, sequenza, numero di parole e assenza di duplicati.

## 6. Integrità delle wordlist

Le wordlist vengono sottoposte a verifica SHA-256 prima dell'utilizzo.

Una wordlist modificata o non valida provoca l'interruzione del programma.

## 7. Self-test

SeedGen esegue controlli automatici prima della generazione.

I test verificano le funzioni critiche di conversione dell'entropia, BIP39, checksum, wordlist e rejection sampling.

Se un test fallisce, la generazione non viene avviata.

## 8. Verifica della trascrizione

La procedura di generazione richiede una verifica esplicita della trascrizione del segreto.

La generazione non deve essere considerata completata semplicemente perché il segreto è stato visualizzato.

## 9. RNG software

Il software non utilizza un RNG software per generare il segreto principale.

L'entropia utilizzata per la mnemonic deriva dai lanci fisici dei dadi D6.

## 10. Rete

SeedGen è progettato per funzionare offline.

Il programma non richiede una connessione di rete per la generazione.

## 11. Wordlist

Le wordlist richieste dal programma devono essere presenti nella directory prevista dall'installazione:

- `bip39_wordlist.txt`
- `diceware_wordlist.txt`

## 12. Piattaforma binaria

La release binaria ufficiale v1.0.0 è fornita per:

- Linux x86_64.

Il codice sorgente Python può essere eseguito separatamente tramite Python 3.

## 13. Installazione

L'installazione Linux viene effettuata tramite:

    INSTALLA_SEEDGEN.sh

L'installer copia il programma e le risorse necessarie nella directory locale dell'utente e crea il launcher nel menu Applicazioni.

## 14. Avvio

Il launcher principale è:

    AVVIA_SEEDGEN.sh

Il launcher verifica l'architettura del sistema, individua il binario e apre una finestra terminale per l'esecuzione.

## 15. Identità della versione

Versione:

    1.0.0

SHA-256 del sorgente `seedgen.py`:

    db687c2c9a9443f2588d9005e02f9eecb1291676a493f27a43566088455ea43a

SHA-256 del binario Linux x86_64:

    43b18f0c53698ed4c16a7dee703a9a6033f379d6a85329a3d9f644476ec4d3c2
