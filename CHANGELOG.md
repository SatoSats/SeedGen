# CHANGELOG - SeedGen

## Non rilasciato

### Modifiche

- Aggiunto un controllo iniziale della raggiungibilità Internet: se Internet viene rilevato prima del menu principale, SeedGen avvisa l'utente e permette di continuare consapevolmente oppure chiudere il programma.
- Il controllo di raggiungibilità utilizza tentativi di connessione TCP verso endpoint pubblici sulla porta 443 e non trasmette mnemonic, passphrase o altri segreti.
- Aggiunto nel launcher il controllo della versione GLIBC prima dell'avvio del binario.
- Se la GLIBC rilevata è inferiore alla versione minima richiesta, il launcher mostra un messaggio di incompatibilità e non avvia il binario.
- Per il binario pubblicato v1.0.0 il simbolo GLIBC più recente richiesto è GLIBC_2.14. Il requisito deve essere ricavato nuovamente per ogni futura build.

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
