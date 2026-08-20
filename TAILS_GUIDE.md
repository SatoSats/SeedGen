# GUIDA TAILS OS - SEEDGEN v15.2 (BETA)

## Procedura per massima sicurezza

### 1. Preparazione (macchina online)
1. Scarica la release v15 da GitHub
2. Verifica SHA-256 del binario
3. Verifica firma GPG
4. Copia tutto su USB

### 2. Avvio Tails
1. Boot da Tails USB
2. Disabilita Wi-Fi e Bluetooth
3. Verifica rete scollegata

### 3. Verifica air-gapped
1. Inserisci USB SeedGen
2. Verifica SHA-256
3. Verifica firma GPG

### 4. Copia in RAM e smonta USB
1. cp -r /media/amnesia/USB/SeedGen /tmp/SeedGen
2. cd /tmp/SeedGen
3. sudo umount /media/amnesia/USB
4. Verifica: ls /media/amnesia/

### 5. Esecuzione dalla RAM
1. cd /tmp/SeedGen
2. ./seedgen-v15-linux-x86_64
3. Self-test
4. Genera seed
5. Trascrivi su carta

### 6. Spegnimento
1. Chiudi il programma
2. Spegni Tails subito
3. Tails riduce il rischio di persistenza

### Vantaggi
- USB smontata prima della generazione
- Codice eseguito dalla RAM
- Nessun dispositivo esterno attivo
