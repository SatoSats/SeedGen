# Guida all'uso di SeedGen su Tails OS

Questa guida spiega come usare SeedGen v14 in modo sicuro su Tails OS (Live USB).

## Principio di sicurezza

Tails esegue tutto in RAM e cancella ogni traccia allo spegnimento. SeedGen deve essere usato esclusivamente offline su Tails.

## Preparazione (su computer normale)

### 1. Scarica e verifica

Scarica dalla release v14:
- seedgen-v14-linux-x86_64.tar.gz
- seedgen-v14-linux-x86_64.tar.gz.asc

Verifica la firma GPG:

gpg --verify seedgen-v14-linux-x86_64.tar.gz.asc seedgen-v14-linux-x86_64.tar.gz

Verifica hash SHA-256:

sha256sum seedgen-v14-linux-x86_64.tar.gz

Hash atteso:

c2b74cc300b84b834d8b70186ce3d815f344ac9052d68c70efbc1d84b74a61aa

### 2. Prepara una USB separata

- Usa una USB diversa da quella di Tails
- Formatta in FAT32 o ext4
- Scompatta l'archivio e copia la cartella dist/ sulla USB

## Avvio su Tails

### 3. Avvia Tails

- Inserisci la USB di Tails
- Riavvia il computer
- Seleziona l'avvio da USB nel BIOS/UEFI
- NON connetterti a internet

### 4. Inserisci la USB con SeedGen

- Dopo l'avvio di Tails, inserisci la seconda USB
- Tails la monterà automaticamente
- Apri il file manager (Places -> USB)

### 5. Esegui SeedGen

Opzione A: Interfaccia grafica
- Apri la cartella dist/
- Clicca su SeedGen.desktop
- Se richiesto, clicca su Trust and Launch

Opzione B: Terminale

cd /media/amnesia/NOME_USB/dist
./seedgen-v14-linux-x86_64

### 6. Genera il seed

- Segui le istruzioni del programma
- Lancia i dadi fisici
- Scrivi il seed su carta o metallo
- NON fotografare il seed
- NON salvare su dispositivi elettronici

### 7. Spegnimento sicuro

- Chiudi il programma
- Espelli la USB con SeedGen
- Spegni Tails
- Tails cancella automaticamente tutto dalla RAM

## Verifica finale

Prima di usare il seed per fondi reali:
1. Verifica la firma GPG
2. Verifica hash SHA-256
3. Testa con importi minimi
4. Conserva il seed in un luogo sicuro

## Domande frequenti

Posso usare il Persistent Storage di Tails?
Sì, ma è meno sicuro. La procedura consigliata è usare una USB separata.

Devo connettermi a internet su Tails?
NO. SeedGen è air-gapped. Non serve internet per usarlo.

Posso usare lo stesso computer per scaricare e generare?
Sì, ma assicurati che il download avvenga su un sistema normale, non su Tails.

Quanto dura la sessione su Tails?
Finché il computer è acceso. Allo spegnimento, Tails cancella tutto.
