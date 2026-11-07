# Porting Raspberry Pi Zero — SEEDGEN Pi V9

Proposta di integrazione a SeedGen di SatoSats, a cura di Andrea (@ilbitcoiner) / Bitvero. Il core originale v1.0.2 rimane invariato; il frontend LCD è separato dal programma CLI alla radice.

## Profilo hardware

Raspberry Pi Zero originale v1.3 ARMv6, Waveshare 1,3" ST7789 240×240 con joystick e KEY1/2/3. Questo profilo non riguarda Pi Zero 2 W, Luckfox o SeedSigner Plus 320×240.

Pin fisici BOARD: Su 31, Giù 35, Sinistra 29, Destra 37, Centro 33, KEY1 40, KEY2 38, KEY3 36. Il display usa il driver ST7789 di SeedSigner 0.8.7. Alimentazione dalla porta PWR IN.

## Funzioni e comandi

Home: Seed BIP39, Password, Verifica, Strumenti. Seed BIP39 supporta 12/15/18/21/24 parole. Password offre soltanto Custom, Diceware classico (6–9 parole) e Diceware BIP39; fonte esclusivamente dadi fisici D6. Diceware BIP39 genera una password, non una mnemonic con checksum.

Frecce per scegliere, centro/KEY2 per confermare. Nei menu Su dalla prima voce o Sinistra seleziona Indietro; centro lo attiva. Nelle pagine informative e dei risultati Su seleziona Indietro. KEY3 resta una scorciatoia. Nella griglia dadi centro registra il risultato fisico, KEY1 cancella l’ultimo; Su dalla riga superiore seleziona Indietro. Uscire annulla l’operazione.

Su dai riquadri superiori della home seleziona Power. Lo spegnimento richiede conferma esplicita e Annulla è predefinito.

Lingue UI: italiano, inglese, francese, spagnolo. La scelta è in RAM e torna italiano al riavvio. Dizionari e segreti non vengono tradotti. Splash SEEDGEN/by Bitvero incluso.

## Test host

Da questa cartella, creare un ambiente Python e installare Pillow (versione host verificata: 13.0.0):

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install Pillow==13.0.0
cd 240x240
python3 -m unittest -v test_ui test_passwords test_navigation
shasum -a 256 -c SOURCE-SHA256SUMS
```

54 test: UI/core, password e navigazione/lingue. Nei test sono eseguiti anche i 14 self-test originali; non sono 14 casi aggiuntivi ai 48. Nessun GPIO o display richiesto per i test host. Il manutentore ha provato funzionalmente la V9 sullo schermo piccolo. I test non sostituiscono un audit indipendente.

## Compilazione

Git, Docker/Compose avviato e shasum richiesti. Eseguire dalla directory `raspberry/240x240`:

```bash
bash build-v9.sh
```

Su Mac si può usare `caffeinate -i bash build-v9.sh`. Lo script usa la directory corrente: partire dalla cartella indicata. Scarica SeedGen v1.0.2, SeedSigner OS 0.8.7 e SeedSigner 0.8.7 in work/, verifica i file vendor, installa il frontend nell’overlay e costruisce il profilo pi0. Su Apple silicon usa emulazione linux/amd64 e può richiedere diverse ore.

Attendere uscita Docker 0 e [8/8] DONE. Risultato: `images/seedgen_os.v1.0.2.pi0.v9.img`, 128 MiB, con checksum locale `images/SHA256SUMS-v9`. Una build fallita può lasciare un’immagine precedente: non usarla come risultato del tentativo corrente. Non compilare in parallelo nella stessa cartella. Docker viene ricreato; upstream può pulire /output, quindi la cache non garantisce una ripresa rapida. Non è dichiarata riproducibilità bit-per-bit.

Scrivere l’immagine personalizzata su microSD dedicata con Raspberry Pi Imager, senza personalizzazioni, attendendo la verifica. La scrittura cancella la SD scelta.

## Ambito, limiti e licenze

Il core congelato in `240x240/vendor/` ha SHA-256 a347d11ec5d23dac0799c5d19ef5495d74b744e479eb67e706c0a7ad62c2564b. Core e dizionari originali invariati, licenza MIT di SatoSats conservata. Le aggiunte usano la licenza MIT in LICENSE; font DejaVu e dizionario EFF corto hanno attribuzioni incluse. Il dizionario corto resta incluso per self-test ma non compare nel menu V9. SeedSigner OS e driver mantengono le rispettive licenze nei repository scaricati.

Il frontend richiede PASS per tutti i self-test e blocca generazione/verifica in presenza di swap o interfacce non-loopback amministrativamente UP, con controlli passivi. Non certifica l’isolamento o l’affidabilità dell’OS. Nessun segreto è intenzionalmente salvato/stampato; CPython non garantisce cancellazione sicura della RAM.

La forza nominale presume dadi equi e indipendenti. Il filtro diagnostico non certifica l’entropia e condiziona i blocchi accettati: non si dichiara uniformità esatta dell’intero processo filtrato. SEEDGEN non deriva indirizzi, non conserva fondi e non firma transazioni.

Il porting include branding Bitvero e integra driver/build SeedSigner; la sua proposta non implica approvazione ufficiale da parte di quei progetti.

Questa integrazione aggiunge solo la cartella raspberry/. I launcher e i documenti della distribuzione originale restano quelli upstream. La release binaria del fork è disponibile separatamente: https://github.com/ilbitcoiner/SeedGen/releases/tag/pi-v9 .
