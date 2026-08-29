# THREAT MODEL - SEEDGEN v1.0.0

## 1. Scopo

Questo documento descrive le principali minacce considerate nel progetto SeedGen v1.0.0 e le relative misure di mitigazione.

SeedGen è un generatore offline di mnemonic BIP39 basato su entropia fisica ottenuta tramite dadi D6.

## 2. Segreto principale

Il segreto generato da SeedGen è costituito dall'entropia utilizzata per produrre la mnemonic BIP39.

Il programma non deve utilizzare un RNG software per sostituire o integrare l'entropia fisica primaria.

## 3. Bias nell'entropia

### Minaccia

Una conversione non uniforme dei risultati dei dadi potrebbe introdurre bias nell'entropia.

### Mitigazione

SeedGen utilizza rejection sampling per convertire i risultati dei D6 evitando il bias derivante dalla rappresentazione binaria.

## 4. Wordlist modificata

### Minaccia

Una wordlist alterata potrebbe produrre mnemonic o passphrase differenti da quelle previste.

### Mitigazione

Le wordlist vengono verificate tramite SHA-256 prima dell'utilizzo.

Se la verifica fallisce, il programma interrompe l'operazione.

## 5. Errori software

### Minaccia

Un errore nelle funzioni critiche potrebbe produrre risultati errati.

### Mitigazione

SeedGen esegue self-test prima della generazione.

I test comprendono:

- conversione dell'entropia;
- conversione BIP39;
- checksum;
- verifica delle wordlist;
- rejection sampling.

In caso di errore la generazione non viene avviata.

## 6. Errore di trascrizione

### Minaccia

L'utente potrebbe trascrivere una mnemonic o una passphrase in modo errato.

### Mitigazione

La procedura di SeedGen richiede una verifica della trascrizione prima di considerare completata la generazione.

## 7. Compromissione del sistema

### Minaccia

Un sistema operativo compromesso potrebbe osservare o modificare il programma o i dati visualizzati.

### Mitigazione

SeedGen è progettato per l'utilizzo offline.

Per operazioni con fondi reali è necessario utilizzare un ambiente affidabile e adeguatamente isolato.

## 8. Persistenza dei dati

### Minaccia

Il sistema operativo potrebbe conservare dati temporanei relativi al segreto, ad esempio tramite memoria, swap o altri meccanismi di persistenza.

### Mitigazione

L'utente deve utilizzare un ambiente appropriato per la generazione di segreti e deve evitare di salvare mnemonic o passphrase su disco.

I segreti devono essere conservati esclusivamente secondo una procedura di cold storage affidabile.

## 9. Manipolazione del binario

### Minaccia

Un binario modificato potrebbe eseguire codice differente da quello previsto.

### Mitigazione

Le release ufficiali devono essere distribuite con dati di integrità SHA-256 e, quando previsto, firma GPG.

L'utente deve verificare l'artefatto prima dell'utilizzo.

## 10. Supply chain

### Minaccia

Un attaccante potrebbe modificare sorgente, wordlist o artefatti durante la distribuzione.

### Mitigazione

Il progetto mantiene identificatori di versione e hash SHA-256 degli artefatti della release.

La chiave pubblica GPG utilizzata per la verifica è distribuita nel repository.

## 11. Attacchi di rete

### Minaccia

Un'applicazione che comunica con servizi esterni potrebbe trasmettere il segreto.

### Mitigazione

SeedGen è progettato per funzionare senza connessione di rete e non richiede servizi online per la generazione.

## 12. Errore umano

### Minaccia

L'utente potrebbe utilizzare dadi non appropriati, effettuare lanci errati, trascrivere male il risultato o conservare il segreto in modo insicuro.

### Mitigazione

La sicurezza complessiva dipende anche dalla procedura utilizzata dall'operatore.

L'utente deve seguire attentamente le istruzioni di generazione, verifica e conservazione.

## 13. Limiti

SeedGen non può proteggere da:

- hardware compromesso;
- sistema operativo compromesso;
- dadi fisicamente manipolati o difettosi;
- osservazione diretta dello schermo;
- errori dell'operatore;
- conservazione insicura del segreto;
- compromissione del dispositivo utilizzato per l'installazione.

## 14. Modello operativo

SeedGen deve essere considerato uno strumento per generare materiale segreto offline.

La sicurezza finale dipende dalla combinazione di:

1. correttezza del software;
2. integrità delle wordlist;
3. qualità dell'entropia fisica;
4. integrità dell'ambiente;
5. corretta procedura dell'operatore;
6. corretta conservazione del segreto.

## 15. Identità della release

Versione:

    1.0.0

SHA-256 sorgente:

    db687c2c9a9443f2588d9005e02f9eecb1291676a493f27a43566088455ea43a

SHA-256 binario Linux x86_64:

    43b18f0c53698ed4c16a7dee703a9a6033f379d6a85329a3d9f644476ec4d3c2
