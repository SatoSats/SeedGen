# GUIDA SEEDGEN v1.0.2

━━━━━━━━━━━━━━━━━━━━━━  1. SCARICARE SEEDGEN  ━━━━━━━━━━━━━━━━━━━━━━

Dal computer collegato a Internet:

Collegati al Repository di GitHub:
https://github.com/SatoSats/SeedGen

Guarda sulla destra e clicca sulla release (Latest).

Scarica i cinque file che trovi in Assets.

- GUIDA_INSTALLAZIONE_SEEDGEN.md
- chiave_pubblica_gpg.asc
- seedgen-v1.0.2-linux-x86_64.tar.gz
- seedgen-v1.0.2-linux-x86_64.tar.gz.asc
- seedgen-v1.0.2-linux-x86_64.tar.gz.sha256

Salvali in una chiavetta USB.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ CONTINUA SUL COMPUTER OFFLINE O DA TAILS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inserisci la chiavetta USB e aprila. (In Tails: App → Accessori → File)

Dovrai avere al suo interno i cinque file:

- GUIDA_INSTALLAZIONE_SEEDGEN.md
- chiave_pubblica_gpg.asc
- seedgen-v1.0.2-linux-x86_64.tar.gz
- seedgen-v1.0.2-linux-x86_64.tar.gz.asc
- seedgen-v1.0.2-linux-x86_64.tar.gz.sha256

━━━━━━━━━━━━━━━━━━━━━━  2. VERIFICA SHA-256  ━━━━━━━━━━━━━━━━━━━━━━

Clicca con il tasto destro del mouse in un punto vuoto della cartella.

Apri il Terminale (su Tails si chiama "Console").

Eseguire:

sha256sum -c seedgen-v1.0.2-linux-x86_64.tar.gz.sha256

(Premi Invio)

Come risultato corretto deve dare:

✅ seedgen-v1.0.2-linux-x86_64.tar.gz: OK

━━━━━━━━━━━━━━━━━━━━━━  3. VERIFICA FIRMA GPG  ━━━━━━━━━━━━━━━━━━━━━━

Prima di utilizzare la chiave pubblica, controlla la fingerprint.

Eseguire:

gpg --show-keys --fingerprint chiave_pubblica_gpg.asc

(Premi Invio)

La fingerprint deve essere esattamente:

✅ EA83 1AF9 D252 F9E4 43EE 6A1D ECD3 0979 3F79 E833

Se la fingerprint è corretta, importa la chiave:

gpg --import chiave_pubblica_gpg.asc

(Premi Invio)

Eseguire:

gpg --verify seedgen-v1.0.2-linux-x86_64.tar.gz.asc seedgen-v1.0.2-linux-x86_64.tar.gz

(Premi Invio)

Come risultato corretto deve dare:

✅ Firma valida da "SatoSats SatoSats@users.noreply.github.com"

━━━━━━━━━━━━━━━━━━━━━━  4. ESTRARRE IL PACCHETTO  ━━━━━━━━━━━━━━━━━━━━━━

Clicca con il tasto destro del mouse sul pacchetto:

seedgen-v1.0.2-linux-x86_64.tar.gz

Seleziona "Estrai qui".

Verrà estratta la cartella chiamata:

seedgen-v1.0.2-linux-x86_64

Entra nella cartella appena estratta.

━━━━━━━━━━━━━━━━━━━━━━  5. INSTALLAZIONE  ━━━━━━━━━━━━━━━━━━━━━━

Clicca con il tasto destro del mouse in un punto vuoto della cartella.

Apri il Terminale (su Tails si chiama "Console").

Eseguire:

bash INSTALLA_SEEDGEN.sh

(Premi Invio)

Il terminale deve mostrare un messaggio di installazione completata senza errori.

✅ SeedGen è installato nel menu Applicazioni.

━━━━━━━━━━━━━━━━━━━━━━  6. AVVIO  ━━━━━━━━━━━━━━━━━━━━━━

SeedGen è ora installato nel menu Applicazioni.

Lo trovi nella categoria:

Accessori → SeedGen

oppure

premi il tasto Windows sulla tastiera (bandiera Windows) e nel campo di ricerca digita:

SeedGen

Clicca sull'icona per avviare.

✅ Procedura completata. SeedGen è pronto per l'utilizzo.


⚠️ Su Tails, il tastierino numerico laterale potrebbe non funzionare correttamente. 
Questa limitazione non dipende da SeedGen, ma dal modo in cui Tails gestisce e configura le periferiche di input. 
In questi casi, è necessario utilizzare i tasti numerici standard presenti nella parte superiore della tastiera.

━━━━━━━━━━━━━━━━━━━━━━  7. DISINSTALLA SEEDGEN  ━━━━━━━━━━━━━━━━━━━━━━

Per disinstallare SeedGen:

Apri il Terminale.

Eseguire:

rm -rf ~/.local/share/seedgen
rm -f ~/.local/share/applications/seedgen.desktop
rm -f ~/.local/share/icons/seedgen-icon.svg

(Premi Invio)

SeedGen è stato rimosso dal computer.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Utilizzo sicuro:

    - lavorare offline;
    - non fare fotografie della schermata;
    - non salvare la mnemonic sul computer;
    - usare carta e penna.

SeedGen non è un wallet, non conserva fondi, non invia dati e funziona offline.
