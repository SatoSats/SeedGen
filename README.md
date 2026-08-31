# SeedGen v1.0.1

SeedGen è un generatore di mnemonic BIP39 e passphrase Diceware opzionali, progettato per essere utilizzato offline.

SeedGen non è un wallet. Non conserva fondi, non deriva indirizzi e non firma transazioni. Non trasmette mnemonic, passphrase o altri segreti in rete. Il controllo iniziale della raggiungibilità Internet può effettuare brevi tentativi di connessione TCP verso endpoint pubblici sulla porta 443.

## Installazione Linux

Eseguire:

    ./INSTALLA_SEEDGEN.sh

L'installer installa SeedGen in ~/.local/share/seedgen e crea il launcher nel menu Applicazioni.

Il binario Linux x86_64 della release v1.0.1 richiede GLIBC 2.14 o successiva. Il launcher corrente verifica la versione GLIBC rilevata prima di avviare il binario e, se è troppo vecchia, mostra un messaggio di incompatibilità.

## Avvio

SeedGen può essere avviato dal menu Applicazioni oppure tramite AVVIA_SEEDGEN.sh.

Dopo i self-test e prima del menu principale, SeedGen controlla se Internet è raggiungibile. Se rileva una connessione, avvisa l'utente e permette di continuare consapevolmente oppure chiudere SeedGen. Se Internet non viene rilevato, il menu principale viene mostrato senza alcun avviso.

## Generazione

SeedGen utilizza entropia fisica ottenuta da dadi D6 e rejection sampling.

Sono supportate le lunghezze BIP39 standard da 128 a 256 bit.

È disponibile anche la generazione opzionale di passphrase Diceware.

## Verifiche

Le wordlist vengono verificate tramite SHA-256 e il programma esegue self-test prima della generazione.

La procedura richiede la verifica della trascrizione del segreto.

## Sicurezza

Per l'utilizzo con fondi reali lavorare offline, usare un ambiente affidabile e conservare i segreti esclusivamente su supporto fisico.

## Integrità release v1.0.1

Gli hash seguenti appartengono agli artefatti congelati della release v1.0.1.

SHA-256 sorgente della release:
9e0257cfabdfad75274f8572569d52551aff6e3ecd4906d487ec77bc38001d98

SHA-256 binario Linux x86_64:
b85c0e21177d0edcc627761e2b486c75412f509561dda400d7c9e620ee90a28e

## Licenza

SeedGen è distribuito con licenza MIT. Vedere LICENSE.
