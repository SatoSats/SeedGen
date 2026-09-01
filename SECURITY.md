# SECURITY POLICY - SEEDGEN v1.0.2

## Versione supportata

La versione attuale supportata è:

| Versione | Stato |
|----------|-------|
| v1.0.2 | ✅ Versione corrente |

Le versioni precedenti alla serie v1.0.0 non fanno parte della distribuzione corrente.

## Segnalazione di vulnerabilità

Per segnalare una vulnerabilità di sicurezza, non aprire una issue pubblica con dettagli tecnici sfruttabili.

Utilizzare il canale privato di sicurezza disponibile nel repository GitHub.

Fornire, quando possibile:

- descrizione del problema;
- versione interessata;
- procedura per riprodurlo;
- eventuali messaggi di errore;
- impatto osservato.

## Tempi di risposta

- Conferma della ricezione: entro 48 ore.
- Prima valutazione: entro 7 giorni.
- Correzione: in funzione della severità e della complessità del problema.

## Divulgazione coordinata

Quando una vulnerabilità viene confermata:

1. il problema viene analizzato privatamente;
2. viene preparata una correzione;
3. la correzione viene verificata;
4. viene pubblicata una nuova versione quando necessario;
5. la vulnerabilità può essere resa pubblica dopo la disponibilità della correzione.

## Integrità delle release

Le release pubblicate devono essere considerate immutabili.

Una correzione che modifica il software deve produrre una nuova versione.

Gli asset di una release già pubblicata non devono essere sostituiti con file differenti.

## Firma e verifica

Le release ufficiali devono essere accompagnate dai relativi dati di integrità e, quando previsto, dalla firma GPG.

La chiave pubblica utilizzata per la verifica è distribuita nel repository tramite:

    chiave_pubblica_gpg.asc

Prima di utilizzare una release destinata a fondi reali, verificare sempre:

- autenticità della firma;
- SHA-256 dell'artefatto;
- corrispondenza della versione;
- provenienza del pacchetto.

## Limitazioni

SeedGen è uno strumento per la generazione di segreti e non è un wallet.

La sicurezza complessiva dipende anche da:

- hardware utilizzato;
- sistema operativo;
- ambiente di esecuzione;
- procedura di generazione;
- gestione e conservazione del segreto generato.

Per fondi reali è raccomandato utilizzare un ambiente offline e affidabile.

Prima del menu principale, SeedGen verifica se Internet è raggiungibile. Se rileva una connessione, avvisa l'utente e permette di continuare consapevolmente oppure chiudere il programma. Il controllo non trasmette mnemonic, passphrase o altri segreti.

## Principio di sicurezza

SeedGen è progettato per generare l'entropia del segreto a partire da lanci fisici di dadi D6.

Il programma non utilizza un RNG software per generare il segreto.

La conversione dei lanci utilizza rejection sampling per evitare bias nell'estrazione dell'entropia.
