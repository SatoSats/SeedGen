# BUILD - SEEDGEN v1.0.0

## 1. Scopo

Questo documento descrive la procedura congelata per ricostruire il binario Linux x86_64 della release pubblicata SeedGen v1.0.0 a partire dal sorgente identificato dall'hash riportato di seguito.

La build utilizza PyInstaller e produce un singolo eseguibile.

## 2. Requisiti

Sono richiesti:

- Linux x86_64;
- Python 3;
- PyInstaller;
- `sha256sum`;
- il sorgente `seedgen.py`;
- le wordlist del progetto.

Per verificare Python:

    python3 --version

Per verificare PyInstaller:

    pyinstaller --version

## 3. Sorgente congelato

La release v1.0.0 utilizza il seguente sorgente:

    seedgen.py

SHA-256 del sorgente:

    db687c2c9a9443f2588d9005e02f9eecb1291676a493f27a43566088455ea43a

Lo script `build.sh` verifica automaticamente questo hash prima di avviare la compilazione.

Se l'hash non corrisponde, la build viene interrotta.

Il branch `main` può contenere modifiche successive non ancora rilasciate. In tal caso è intenzionale che `build.sh` rifiuti il sorgente corrente: lo script resta congelato sulla release v1.0.0 finché non viene deliberata e preparata una nuova release.

## 4. Build

Dalla directory principale del repository:

    cd ~/Documenti/SeedGen

eseguire:

    ./build.sh

Lo script:

1. verifica l'hash di `seedgen.py`;
2. imposta `PYTHONHASHSEED=1`;
3. crea una directory temporanea di build;
4. esegue PyInstaller;
5. produce un singolo binario Linux x86_64;
6. calcola lo SHA-256 del binario.

La directory temporanea utilizzata è:

    /tmp/seedgen-v1.0.0-build-scripted

Il binario prodotto è:

    /tmp/seedgen-v1.0.0-build-scripted/dist/seedgen-v1.0.0-linux-x86_64

## 5. Verifica del binario

Dopo la build:

    ls -lh /tmp/seedgen-v1.0.0-build-scripted/dist/

Calcolare l'hash:

    sha256sum /tmp/seedgen-v1.0.0-build-scripted/dist/seedgen-v1.0.0-linux-x86_64

Per la build di riferimento v1.0.0 l'hash del binario è:

    43b18f0c53698ed4c16a7dee703a9a6033f379d6a85329a3d9f644476ec4d3c2

## 6. Verifica dell'architettura

Verificare l'architettura del sistema:

    uname -m

La build ufficiale v1.0.0 è destinata a:

    x86_64

Verificare anche il tipo di file:

    file /tmp/seedgen-v1.0.0-build-scripted/dist/seedgen-v1.0.0-linux-x86_64

## 7. Test del binario

Il binario richiede le wordlist del progetto.

Per eseguire il test dalla directory del repository, copiare il binario nella directory corrente:

    cp /tmp/seedgen-v1.0.0-build-scripted/dist/seedgen-v1.0.0-linux-x86_64 .

quindi avviarlo:

    ./seedgen-v1.0.0-linux-x86_64

Il programma deve avviarsi correttamente e completare i propri self-test prima di permettere la generazione.

## 8. Installazione

L'installer ufficiale è:

    INSTALLA_SEEDGEN.sh

Dalla directory contenente il binario e i file del progetto:

    ./INSTALLA_SEEDGEN.sh

L'installer copia i componenti necessari nell'installazione locale dell'utente e crea il launcher nel menu Applicazioni.

## 9. Riproducibilità della build

La build v1.0.0 è associata a:

- versione sorgente;
- hash SHA-256 del sorgente;
- configurazione di build;
- versione del binario;
- hash SHA-256 del binario.

L'hash del sorgente deve essere verificato prima della compilazione.

L'hash del binario deve essere verificato dopo la compilazione.

Una differenza nell'hash indica che il risultato non corrisponde al binario di riferimento e deve essere analizzato prima della distribuzione.

## 10. Release

La release ufficiale deve essere costruita a partire dal sorgente verificato.

Prima della pubblicazione verificare:

1. versione del programma;
2. hash del sorgente;
3. build completata senza errori;
4. hash del binario;
5. architettura del binario;
6. avvio del programma;
7. self-test;
8. presenza delle wordlist richieste;
9. funzionamento dell'installer;
10. funzionamento del launcher.

## 11. Identità della release

Versione:

    1.0.0

SHA-256 sorgente:

    db687c2c9a9443f2588d9005e02f9eecb1291676a493f27a43566088455ea43a

SHA-256 binario Linux x86_64:

    43b18f0c53698ed4c16a7dee703a9a6033f379d6a85329a3d9f644476ec4d3c2
