# SPECIFICHE TECNICHE - SEEDGEN v1.0.1

## 1. Scopo

SeedGen è un generatore offline di mnemonic BIP39 ottenute da entropia fisica generata tramite dadi D6.

Il programma può inoltre generare passphrase basate su Diceware.

SeedGen non è un wallet e non gestisce fondi o transazioni.

## 2. Entropia

L'entropia primaria viene fornita esclusivamente dai lanci fisici di dadi D6.

Prima dell'estrazione dell'entropia, SeedGen controlla la distribuzione dei risultati dei lanci. Una sequenza viene considerata anomala se un singolo valore compare per più del 40% dei lanci oppure se sono presenti soltanto 1 o 2 valori distinti tra le sei facce del dado.

In caso di distribuzione anomala, il blocco viene scartato e SeedGen richiede di rifare tutti i lanci oppure di annullare la generazione.

La conversione dei risultati utilizza rejection sampling. Se il blocco viene rifiutato dal rejection sampling, tutti i lanci del blocco vengono scartati e viene richiesto un nuovo blocco.

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

SeedGen può generare passphrase di 6, 7, 8 o 9 parole utilizzando una wordlist Diceware.

La wordlist viene verificata prima dell'utilizzo.

Sono controllati formato, codici, sequenza, numero di parole e assenza di duplicati.

Per ogni parola vengono effettuati 5 lanci di un dado D6. La combinazione dei cinque risultati determina direttamente un indice da 1 a 7776 nella wordlist Diceware.

Al termine della raccolta dei lanci viene applicato il controllo della distribuzione descritto nella sezione 2. Se la distribuzione viene considerata anomala, tutti i lanci della passphrase vengono rifatti oppure la generazione viene annullata.

La passphrase viene quindi mostrata e la procedura richiede la verifica obbligatoria della trascrizione.

## 6. Integrità delle wordlist

Le wordlist vengono sottoposte a verifica SHA-256 prima dell'utilizzo.

Una wordlist modificata o non valida provoca l'interruzione del programma.

## 7. Self-test

SeedGen esegue controlli automatici prima della generazione.

I test verificano le funzioni critiche di conversione dell'entropia, BIP39, checksum, wordlist e rejection sampling.

I self-test possono produrre tre stati:

- `PASS`: test eseguito e superato;
- `FAIL`: test eseguito e fallito;
- `SKIPPED`: test non eseguibile nell'ambiente corrente.

Se un test è in stato `FAIL`, l'avvio del programma viene bloccato. Uno stato `SKIPPED` viene segnalato ma non blocca l'avvio.

## 8. Verifica della trascrizione

La procedura di generazione richiede una verifica esplicita della trascrizione del segreto.

La generazione non deve essere considerata completata semplicemente perché il segreto è stato visualizzato.

## 9. RNG software

Il software non utilizza un RNG software per generare il segreto principale.

L'entropia utilizzata per la mnemonic deriva dai lanci fisici dei dadi D6.

## 10. Rete

SeedGen è progettato per funzionare offline.

Il programma non richiede una connessione di rete per la generazione.

Dopo i self-test e prima del menu principale, SeedGen verifica la raggiungibilità Internet tentando connessioni TCP verso `1.1.1.1`, `8.8.8.8` e `1.0.0.1` sulla porta 443, con timeout di 1,5 secondi per tentativo.

Al primo tentativo riuscito Internet viene considerato raggiungibile e viene mostrato un avviso con due possibilità:

- `[1] Sono consapevole, continua`;
- `[2] Chiudi SeedGen`.

Se nessun tentativo riesce, non viene mostrato alcun avviso e viene aperto il menu principale.

Il controllo può generare esclusivamente traffico di rilevamento della raggiungibilità. Mnemonic, passphrase e altri segreti non vengono trasmessi.

## 11. Wordlist

Le wordlist richieste dal programma devono essere presenti nella directory prevista dall'installazione:

- `bip39_wordlist.txt`
- `diceware_wordlist.txt`

## 12. Piattaforma binaria

La release binaria v1.0.1 è destinata a:

- Linux x86_64.

Il binario della release v1.0.1 richiede simboli GLIBC fino a `GLIBC_2.14` e richiede quindi GLIBC 2.14 o successiva.

Il codice sorgente Python può essere eseguito separatamente tramite Python 3.

## 13. Installazione

L'installazione Linux viene effettuata tramite:

    INSTALLA_SEEDGEN.sh

L'installer copia il programma e le risorse necessarie nella directory locale dell'utente e crea il launcher nel menu Applicazioni.

## 14. Avvio

Il launcher principale è:

    AVVIA_SEEDGEN.sh

Il launcher verifica l'architettura del sistema e la presenza del binario.

Se `getconf GNU_LIBC_VERSION` permette di rilevare la versione GLIBC e questa è inferiore alla 2.14, il launcher blocca l'avvio e mostra un messaggio che indica l'incompatibilità della distribuzione Linux. Il messaggio raccomanda di aggiornare la distribuzione o utilizzarne una più recente e di non aggiornare manualmente GLIBC separatamente dal sistema.

Se la versione GLIBC è almeno 2.14, oppure non viene rilevata nel formato previsto, il launcher prosegue e apre una finestra terminale per l'esecuzione del binario.

## 15. Identità della versione

Versione:

    1.0.1

SHA-256 del sorgente `seedgen.py` della release v1.0.1:

    9e0257cfabdfad75274f8572569d52551aff6e3ecd4906d487ec77bc38001d98

SHA-256 del binario Linux x86_64 della release v1.0.1:

    b85c0e21177d0edcc627761e2b486c75412f509561dda400d7c9e620ee90a28e
