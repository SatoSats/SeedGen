# THREAT MODEL - SEEDGEN v15

## Scopo
Questo documento descrive le minacce considerate per SeedGen e le relative mitigazioni.

---

## T1 - Compromissione del sorgente
- **Descrizione**: Il codice sorgente viene modificato malevolmente
- **Mitigazione**: PARZIALE (firma GPG, hash SHA-256, audit indipendente)
- **Nota**: La chiave pubblica deve essere verificata tramite canale indipendente

## T2 - Release malevola
- **Descrizione**: Una release contiene codice dannoso
- **Mitigazione**: PARZIALE (firma GPG, hash verificabili)
- **Nota**: Verificare sempre firma e hash prima dell'uso

## T3 - Wordlist modificata
- **Descrizione**: Le wordlist BIP39 o Diceware vengono alterate
- **Mitigazione**: SOFTWARE (SHA-256 verificato all'avvio)
- **Nota**: Un hash non corrispondente blocca il programma

## T4 - OS compromesso
- **Descrizione**: Il sistema operativo è infetto
- **Mitigazione**: FUORI SCOPE (richiede OS pulito/verificato)
- **Nota**: Usare macchina dedicata o live USB

## T5 - Firmware compromesso
- **Descrizione**: BIOS/UEFI o firmware malevolo
- **Mitigazione**: FUORI SCOPE
- **Nota**: Richiede hardware verificato

## T6 - Hardware compromesso
- **Descrizione**: Hardware modificato fisicamente
- **Mitigazione**: FUORI SCOPE
- **Nota**: Ispezione fisica consigliata

## T7 - Dadi non uniformi
- **Descrizione**: Dadi con bias fisico
- **Mitigazione**: PARZIALE (rejection sampling elimina bias conversione)
- **Nota**: NON elimina il bias fisico del dado stesso

## T8 - Errore di trascrizione
- **Descrizione**: Errore umano nel copiare la seed
- **Mitigazione**: PROCEDURA (verifica manuale, doppia trascrizione)
- **Nota**: SeedGen non può rilevare errori di trascrizione

## T9 - Spionaggio visivo (shoulder surfing)
- **Descrizione**: Qualcuno guarda lo schermo
- **Mitigazione**: PROCEDURA (ambiente privato)
- **Nota**: SeedGen mostra avvisi di sicurezza

## T10 - Cattura del terminale
- **Descrizione**: Screen capture o logging del terminale
- **Mitigazione**: PROCEDURA (verifica ambiente)
- **Nota**: Il terminale non deve avere scrollback persistente

## T11 - Swap/Core dump
- **Descrizione**: Segreti trasferiti su disco via swap o crash dump
- **Mitigazione**: PROCEDURA (swap disabilitato, core dump disabilitati)
- **Nota**: SeedGen non può disabilitare swap/core dump

## T12 - Malware/Keylogger
- **Descrizione**: Software che registra tasti o ruba dati
- **Mitigazione**: FUORI SCOPE (richiede OS pulito)
- **Nota**: Usare macchina dedicata

## T13 - Furto fisico
- **Descrizione**: Qualcuno ruba la seed scritta su carta
- **Mitigazione**: FUORI SCOPE (sicurezza fisica)
- **Nota**: Conservare in luogo sicuro

## T14 - Perdita passphrase
- **Descrizione**: La passphrase Diceware viene persa
- **Mitigazione**: FUORI SCOPE (backup separati)
- **Nota**: Perdere la passphrase = perdere il wallet

## T15 - Attacco supply-chain
- **Descrizione**: Compromissione della catena di distribuzione
- **Mitigazione**: PARZIALE (firma GPG, hash, verifica indipendente)
- **Nota**: Verificare sempre la fonte del software

---

## CLASSIFICAZIONE FINALE

| Minaccia | Mitigazione |
|----------|-------------|
| T1 Sorgente compromesso | Parziale (GPG) |
| T2 Release malevola | Parziale (GPG) |
| T3 Wordlist modificata | Software (SHA-256) |
| T4 OS compromesso | Fuori scope |
| T5 Firmware | Fuori scope |
| T6 Hardware | Fuori scope |
| T7 Dadi biased | Parziale (rejection) |
| T8 Errore trascrizione | Procedura |
| T9 Shoulder surfing | Procedura |
| T10 Terminal capture | Procedura |
| T11 Swap/Core dump | Procedura |
| T12 Malware | Fuori scope |
| T13 Furto fisico | Fuori scope |
| T14 Perdita passphrase | Fuori scope |
| T15 Supply chain | Parziale (GPG) |
