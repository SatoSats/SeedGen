# SeedGen v1.0.0

SeedGen è un generatore offline di mnemonic BIP39 e passphrase Diceware opzionali.

SeedGen non è un wallet. Non conserva fondi, non deriva indirizzi, non firma transazioni e non invia dati in rete.

## Installazione Linux

Eseguire:

    ./INSTALLA_SEEDGEN.sh

L'installer installa SeedGen in ~/.local/share/seedgen e crea il launcher nel menu Applicazioni.

## Avvio

SeedGen può essere avviato dal menu Applicazioni oppure tramite AVVIA_SEEDGEN.sh.

## Generazione

SeedGen utilizza entropia fisica ottenuta da dadi D6 e rejection sampling.

Sono supportate le lunghezze BIP39 standard da 128 a 256 bit.

È disponibile anche la generazione opzionale di passphrase Diceware.

## Verifiche

Le wordlist vengono verificate tramite SHA-256 e il programma esegue self-test prima della generazione.

La procedura richiede la verifica della trascrizione del segreto.

## Sicurezza

Per l utilizzo con fondi reali lavorare offline, usare un ambiente affidabile e conservare i segreti esclusivamente su supporto fisico.

## Integrità v1.0.0

SHA-256 sorgente:
db687c2c9a9443f2588d9005e02f9eecb1291676a493f27a43566088455ea43a

SHA-256 binario Linux x86_64:
43b18f0c53698ed4c16a7dee703a9a6033f379d6a85329a3d9f644476ec4d3c2

## Licenza

SeedGen è distribuito con licenza MIT. Vedere LICENSE.
