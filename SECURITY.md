# SECURITY POLICY - SEEDGEN v15.4 (BETA)

## Versioni Supportate

| Versione | Stato |
|----------|-------|
| v15.4 (BETA) | ✅ Supportata |
| v15.3 e precedenti | ❌ Non supportate |

## Canale Privato per Vulnerabilità

Per segnalare vulnerabilità di sicurezza, NON aprire issue pubbliche.
Contattare privatamente: **SatoSats@users.noreply.github.com**

## Tempi di Risposta

- Conferma ricezione: entro 48 ore
- Prima valutazione: entro 7 giorni
- Correzione: dipende dalla severità

## Politica di Divulgazione Coordinata

1. Il segnalatore contatta privatamente
2. Conferma ricezione entro 48 ore
3. Valutazione congiunta
4. Correzione e release
5. Divulgazione pubblica dopo 30 giorni dalla correzione

## Fingerprint Chiavi Autorizzate

GPG: EA83 1AF9 D252 F9E4 43EE 6A1D ECD3 0979 3F79 E833

## Procedura di Revoca

In caso di compromissione della chiave:
1. Revoca immediata della chiave GPG
2. Pubblicazione nuova chiave tramite canale indipendente
3. Nuova release con nuova firma
4. Avviso alla community

## Limitazioni

- Il progetto è in BETA
- Non usare per fondi significativi senza audit
- La sicurezza dipende anche da hardware e procedura

## Policy Release Immutabili

Le release NON devono essere modificate dopo la pubblicazione.
Qualsiasi correzione deve produrre una NUOVA versione (v15.4, v15.5, ecc).
Gli asset pubblicati non devono essere sostituiti.

Procedura:
1. Correzione → nuovo commit firmato
2. Nuovo tag firmato (vX.Y.Z)
3. Nuova release dal tag
4. La vecchia release resta intatta per riferimento
