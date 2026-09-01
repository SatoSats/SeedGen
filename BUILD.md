# BUILD - SEEDGEN v1.0.2

## 1. Scopo

Questo documento descrive la procedura congelata per ricostruire il binario Linux x86_64 della release SeedGen v1.0.2 a partire dal sorgente identificato dall'hash riportato di seguito.

La build utilizza PyInstaller e produce un singolo eseguibile.

## 2. Requisiti

Sono richiesti:

- Linux x86_64;
- Python 3;
- PyInstaller;
- `sha256sum`;
- `readelf`;
- il sorgente `seedgen.py`;
- le wordlist del progetto.

Per verificare Python:

    python3 --version

Per verificare PyInstaller:

    pyinstaller --version

## 3. Sorgente congelato

La release v1.0.2 utilizza il seguente sorgente:

    seedgen.py

SHA-256 del sorgente:

    a347d11ec5d23dac0799c5d19ef5495d74b744e479eb67e706c0a7ad62c2564b

Lo script `build.sh` verifica automaticamente questo hash prima di avviare la compilazione.

Se l'hash non corrisponde, la build viene interrotta.

Il branch `main` può contenere modifiche successive non ancora rilasciate. In tal caso è intenzionale che `build.sh` rifiuti il sorgente corrente: lo script resta congelato sulla release v1.0.2 finché non viene deliberata e preparata una nuova release.

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

    /tmp/seedgen-v1.0.2-build-scripted

Il binario prodotto è:

    /tmp/seedgen-v1.0.2-build-scripted/dist/seedgen-v1.0.2-linux-x86_64

## 5. Verifica del binario

Dopo la build:

    ls -lh /tmp/seedgen-v1.0.2-build-scripted/dist/

Calcolare l'hash:

    sha256sum /tmp/seedgen-v1.0.2-build-scripted/dist/seedgen-v1.0.2-linux-x86_64

Per la build di riferimento v1.0.2 l'hash del binario è:

    9f90c5566eb21b0ef3e9766378ea33db406a85623d2855e8b4078e682519765f

## 6. Verifica dell'architettura

Verificare l'architettura del sistema:

    uname -m

La build v1.0.2 è destinata a:

    x86_64

Verificare anche il tipo di file:

    file /tmp/seedgen-v1.0.2-build-scripted/dist/seedgen-v1.0.2-linux-x86_64

### Verifica requisito GLIBC

Il requisito GLIBC non deve essere ricavato controllando soltanto l'eseguibile ELF esterno prodotto da PyInstaller.

Una build `--onefile` contiene infatti librerie native incorporate che possono richiedere versioni GLIBC più recenti rispetto al bootloader esterno.

Estrarre quindi tutti i componenti PyInstaller di tipo binario in una directory temporanea e controllare ciascun file con `readelf`.

Per la build v1.0.2 sono stati verificati tutti i 20 componenti binari incorporati.

Il simbolo GLIBC più recente richiesto è:

    GLIBC_2.38

Il requisito minimo del launcher è quindi GLIBC 2.38.

In particolare, nella build di riferimento richiedono `GLIBC_2.38`:

- `libpython3.12.so.1.0`;
- `libcrypto.so.3`;
- `libexpat.so.1`;
- `python3.12/lib-dynload/_decimal.cpython-312-x86_64-linux-gnu.so`.

Questo audit deve essere ripetuto integralmente su ogni nuova build. Non è sufficiente controllare il solo ELF esterno e il requisito non deve essere dedotto dalla sola versione GLIBC del sistema usato per compilare.

## 7. Test del binario

Il binario richiede le wordlist del progetto.

Per eseguire il test dalla directory del repository, copiare il binario nella directory corrente:

    cp /tmp/seedgen-v1.0.2-build-scripted/dist/seedgen-v1.0.2-linux-x86_64 .

quindi avviarlo:

    ./seedgen-v1.0.2-linux-x86_64

Il programma deve avviarsi correttamente e completare i propri self-test prima di permettere la generazione.

## 8. Installazione

L'installer previsto per la release v1.0.2 è:

    INSTALLA_SEEDGEN.sh

Dalla directory contenente il binario e i file del progetto:

    ./INSTALLA_SEEDGEN.sh

L'installer copia i componenti necessari nell'installazione locale dell'utente e crea il launcher nel menu Applicazioni.

## 9. Riproducibilità della build

La build v1.0.2 è associata a:

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

    1.0.2

SHA-256 sorgente:

    a347d11ec5d23dac0799c5d19ef5495d74b744e479eb67e706c0a7ad62c2564b

SHA-256 binario Linux x86_64:

    9f90c5566eb21b0ef3e9766378ea33db406a85623d2855e8b4078e682519765f
