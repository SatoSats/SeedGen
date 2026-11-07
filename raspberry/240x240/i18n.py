"""UI-only translations. Never apply to words, passwords or physical dice data.
Language choice lives in RAM and resets to Italian when powered off.
"""
import re
LANGUAGES=(('it','Italiano'),('en','English'),('fr','Français'),('es','Español'))
_language='it'
# Key | English | French | Spanish
_DATA='''
Custom|Custom|Personnalisé|Personalizada
Verifica|Verify|Vérifier|Verificar
Strumenti|Tools|Outils|Herramientas
Lingua|Language|Langue|Idioma
Lingua applicata|Language selected|Langue choisie|Idioma seleccionado
Valida per questa sessione.|Applies to this session.|Valable pour cette session.|Válido para esta sesión.
Al riavvio torna italiano.|Italian after restart.|Italien au redémarrage.|Italiano al reiniciar.
Test integrita|Integrity test|Test d'intégrité|Test de integridad
Test pulsanti|Button test|Test des boutons|Prueba de botones
Spegni Raspberry|Power off|Éteindre|Apagar
Spegni ora|Power off now|Éteindre maintenant|Apagar ahora
Spegnimento|Power off|Extinction|Apagado
Spegnimento...|Powering off...|Extinction...|Apagando...
Annulla|Cancel|Annuler|Cancelar
Tipo password|Password type|Mot de passe|Tipo de contraseña
Diceware classico|Classic Diceware|Diceware classique|Diceware clásico
Numero parole|Word count|Nombre de mots|Número de palabras
Nuova seed BIP39|New BIP39 seed|Nouvelle seed BIP39|Nueva seed BIP39
Verifica BIP39|Verify BIP39|Vérifier BIP39|Verificar BIP39
Verifica BIP39 - TEST|Verify BIP39 - TEST|Vérifier BIP39 - TEST|Verificar BIP39 - TEST
Caratteri Custom|Custom characters|Caractères Custom|Caracteres Custom
Minuscole|Lowercase|Minuscules|Minúsculas
Maiuscole|Uppercase|Majuscules|Mayúsculas
Numeri|Digits|Chiffres|Números
Simboli|Symbols|Symboles|Símbolos
%s: SI|%s: YES|%s: OUI|%s: SÍ
%s: NO|%s: NO|%s: NON|%s: NO
Continua|Continue|Continuer|Continuar
Scegli caratteri|Choose characters|Choisir les caractères|Elegir caracteres
Attiva almeno un gruppo.|Enable at least one group.|Activez au moins un groupe.|Activa al menos un grupo.
Forza password|Password strength|Force du mot de passe|Fuerza de contraseña
Separatore|Separator|Séparateur|Separador
Space|Space|Espace|Espacio
Capitalise|Capitalise|Initiales majuscules|Iniciales mayúsculas
None|None|Aucun|Ninguno
Scegli separatore|Choose separator|Choisir le séparateur|Elegir separador
Senza separatore, parole diverse possono confondersi.|Without a separator, word boundaries can be ambiguous.|Sans séparateur, les limites des mots peuvent être ambiguës.|Sin separador, los límites de las palabras pueden ser ambiguos.
Per mantenere la forza scelta usa spazio, punto o maiuscole.|Use spaces, dots or capitals to preserve the chosen strength.|Utilisez espaces, points ou majuscules pour préserver la force choisie.|Usa espacios, puntos o mayúsculas para conservar la fuerza elegida.
Fonte entropia|Entropy source|Source d'entropie|Fuente de entropía
Dadi fisici D6|Physical D6 dice|Dés physiques D6|Dados físicos D6
Fonte: solo dadi fisici D6.|Source: physical D6 dice only.|Source : dés physiques D6.|Fuente: solo dados físicos D6.
Prima di iniziare|Before starting|Avant de commencer|Antes de empezar
Solo dati di prova.|Test data only.|Données de test uniquement.|Solo datos de prueba.
Solo prove, niente fondi.|Tests only, no funds.|Tests uniquement, aucun fonds.|Solo pruebas, sin fondos.
VERSIONE SPERIMENTALE|EXPERIMENTAL VERSION|VERSION EXPÉRIMENTALE|VERSIÓN EXPERIMENTAL
Usa dadi fisici affidabili.|Use reliable physical dice.|Utilisez des dés fiables.|Usa dados físicos fiables.
Niente foto o telecamere.|No photos or cameras.|Ni photos ni caméras.|Sin fotos ni cámaras.
Prepara carta e penna.|Prepare paper and pen.|Préparez papier et stylo.|Prepara papel y bolígrafo.
K3: annulla senza salvare.|Back: cancel without saving.|Retour : annuler sans sauver.|Atrás: cancelar sin guardar.
%d bit nominali con dadi equi e indipendenti.|%d nominal bits with fair, independent dice.|%d bits nominaux avec des dés équilibrés et indépendants.|%d bits nominales con dados justos e independientes.
%d parole|%d words|%d mots|%d palabras
%d caratteri|%d characters|%d caractères|%d caracteres
%d lanci per blocco.|%d rolls per block.|%d lancers par bloc.|%d tiradas por bloque.
I blocchi fuori intervallo vanno rifatti.|Out-of-range blocks must be rerolled.|Les blocs hors intervalle doivent être relancés.|Los bloques fuera del intervalo deben repetirse.
Lancio %d/%d|Roll %d/%d|Lancer %d/%d|Tirada %d/%d
Ultimi: %s|Recent: %s|Derniers : %s|Últimos: %s
Risultato: %d|Result: %d|Résultat : %d|Resultado: %d
Conferma blocco|Confirm block|Confirmer le bloc|Confirmar bloque
Usa questi %d lanci|Use these %d rolls|Utiliser ces %d lancers|Usar estas %d tiradas
Correggi ultimo lancio|Edit last roll|Corriger le dernier lancer|Corregir última tirada
Distribuzione anomala|Unusual distribution|Distribution anormale|Distribución anómala
Tutto il blocco scartato.|Entire block discarded.|Bloc entier rejeté.|Bloque completo descartado.
Blocco scartato.|Block discarded.|Bloc rejeté.|Bloque descartado.
Rifai TUTTI i lanci.|Reroll the ENTIRE block.|Relancez TOUT le bloc.|Repite TODO el bloque.
Rifai tutti i lanci.|Reroll the entire block.|Relancez tout le bloc.|Repite todo el bloque.
Questo test non garantisce|This test does not guarantee|Ce test ne garantit pas|Esta prueba no garantiza
la casualita dei dadi.|randomness of the dice.|le hasard des dés.|la aleatoriedad de los dados.
Blocco rifiutato|Block rejected|Bloc refusé|Bloque rechazado
tutto il blocco scartato.|entire block discarded.|bloc entier rejeté.|bloque completo descartado.
Passphrase Diceware|Diceware passphrase|Phrase Diceware|Frase Diceware
Trascrivi in minuscolo.|Write in lowercase.|Écrivez en minuscules.|Escribe en minúsculas.
Un solo spazio tra parole.|One space between words.|Un espace entre les mots.|Un espacio entre palabras.
Numeri esclusi.|Exclude word numbers.|Sans numéros de mots.|Sin números de palabras.
Conserva separata|Keep it separate|Conservez-la séparément|Guárdala separada
dalla seed BIP39.|from the BIP39 seed.|de la seed BIP39.|de la seed BIP39.
Trascrivi su carta|Write on paper|Écrire sur papier|Escribir en papel
Parole password|Password words|Mots du mot de passe|Palabras de contraseña
Formato da copiare|Format to copy|Format à copier|Formato a copiar
Separatore: %s|Separator: %s|Séparateur : %s|Separador: %s
Parole in minuscolo.|Lowercase words.|Mots en minuscules.|Palabras en minúsculas.
Iniziale maiuscola di ogni parola.|Capitalise each word.|Une majuscule par mot.|Inicial mayúscula de cada palabra.
E una password, non una seed BIP39.|This is a password, not a BIP39 seed.|C'est un mot de passe, pas une seed BIP39.|Es una contraseña, no una seed BIP39.
Copia formato|Copy format|Copier le format|Copiar formato
Nel testo completo * indica un singolo spazio.|In the full text, * means one space.|Dans le texte complet, * indique un espace.|En el texto completo, * indica un espacio.
Non copiare gli asterischi.|Do not copy the asterisks.|Ne copiez pas les astérisques.|No copies los asteriscos.
Copia il testo esattamente.|Copy the text exactly.|Copiez le texte exactement.|Copia el texto exactamente.
Controlla formato|Check format|Vérifier le format|Verificar formato
Verifica anche separatori e maiuscole sul foglio.|Also check separators and capitals on paper.|Vérifiez aussi séparateurs et majuscules sur papier.|Verifica también separadores y mayúsculas en el papel.
Copia esatta|Exact copy|Copie exacte|Copia exacta
Le righe sono solo impaginazione.|Line breaks are only for display.|Les sauts de ligne servent à l'affichage.|Los saltos de línea son solo visuales.
Non aggiungere spazi o ritorni a capo.|Do not add spaces or line breaks.|N'ajoutez ni espaces ni retours à la ligne.|No añadas espacios ni saltos de línea.
%d caratteri totali.|%d total characters.|%d caractères au total.|%d caracteres en total.
Password %d/%d|Password %d/%d|Mot de passe %d/%d|Contraseña %d/%d
Sessione chiusa|Session closed|Session terminée|Sesión cerrada
Nessun salvataggio.|Nothing saved.|Aucun enregistrement.|Nada guardado.
Nessun segreto salvato.|No secret saved.|Aucun secret enregistré.|Ningún secreto guardado.
RAM Python non azzerabile.|Python RAM cannot be securely wiped.|La RAM Python ne peut être effacée sûrement.|La RAM de Python no se borra de forma segura.
Spegni dopo la prova.|Power off after testing.|Éteignez après le test.|Apaga tras la prueba.
Verifica copia|Verify copy|Vérifier la copie|Verificar copia
Usa solo il foglio.|Use only your paper copy.|Utilisez seulement votre feuille.|Usa solo la copia en papel.
Inserisci TUTTE le parole|Enter ALL the words|Saisissez TOUS les mots|Introduce TODAS las palabras
nello stesso ordine.|in the same order.|dans le même ordre.|en el mismo orden.
K3 annulla: non verificata.|Back cancels: unverified.|Retour annule : non vérifiée.|Atrás cancela: sin verificar.
Copia verificata|Copy verified|Copie vérifiée|Copia verificada
Parole e ordine corretti.|Words and order match.|Mots et ordre corrects.|Palabras y orden correctos.
Conserva il foglio al sicuro.|Keep your paper copy safe.|Gardez votre feuille en sécurité.|Guarda el papel en lugar seguro.
Copia non coincide|Copy does not match|La copie ne correspond pas|La copia no coincide
Riprova dal foglio|Retry from paper|Réessayer depuis la feuille|Reintentar desde el papel
Rivedi le parole|Review words|Revoir les mots|Revisar palabras
Annulla (non verificata)|Cancel (unverified)|Annuler (non vérifiée)|Cancelar (sin verificar)
Riscrivi dal foglio.|Re-enter from paper.|Ressaisissez depuis la feuille.|Vuelve a introducir desde el papel.
Maiuscole e simboli contano.|Case and symbols matter.|Respectez casse et symboles.|Respeta mayúsculas y símbolos.
Tutti i caratteri corretti.|All characters match.|Tous les caractères concordent.|Todos los caracteres coinciden.
Copia diversa|Copy mismatch|Copie différente|Copia diferente
Riprova|Retry|Réessayer|Reintentar
Rivedi password|Review password|Revoir le mot de passe|Revisar contraseña
Parola %d|Word %d|Mot %d|Palabra %d
Parola %d: %s|Word %d: %s|Mot %d : %s|Palabra %d: %s
Fine parola|End word|Fin du mot|Fin de palabra
Cancella lettera|Delete letter|Effacer une lettre|Borrar letra
Usa solo seed di prova.|Use test seeds only.|Utilisez des seeds de test.|Usa solo seeds de prueba.
Controlla parole e checksum.|Check words and checksum.|Vérifiez mots et checksum.|Comprueba palabras y checksum.
Non prova che una seed sia|This does not prove a seed is|Cela ne prouve pas qu'une seed est|Esto no demuestra que una seed sea
casuale o sicura.|random or secure.|aléatoire ou sûre.|aleatoria o segura.
Mnemonic non valida|Invalid mnemonic|Mnémonique invalide|Mnemónica no válida
Copia non verificata|Copy not verified|Copie non vérifiée|Copia sin verificar
Checksum BIP39 errato.|Invalid BIP39 checksum.|Checksum BIP39 incorrect.|Checksum BIP39 incorrecto.
Ricontrolla il foglio.|Check your paper copy.|Revérifiez votre feuille.|Revisa la copia en papel.
Checksum BIP39 valido|Valid BIP39 checksum|Checksum BIP39 valide|Checksum BIP39 válido
%d parole riconosciute.|%d words recognised.|%d mots reconnus.|%d palabras reconocidas.
%d bit di entropia.|%d entropy bits.|%d bits d'entropie.|%d bits de entropía.
Verifica chiusa|Verification closed|Vérification terminée|Verificación cerrada
Prova joystick|Test the joystick|Testez le joystick|Prueba el joystick
e tutti i pulsanti.|and all the buttons.|et tous les boutons.|y todos los botones.
Nessuno|None|Aucun|Ninguno
Ultimo: %s|Last: %s|Dernier : %s|Último: %s
K3: termina.|Back: finish.|Retour : terminer.|Atrás: terminar.
Audit: %d parole|Audit: %d words|Audit : %d mots|Auditoría: %d palabras
N = %d lanci|N = %d rolls|N = %d lancers|N = %d tiradas
Blocco >= M: scartato.|Block >= M: rejected.|Bloc >= M : rejeté.|Bloque >= M: rechazado.
Parametri, nessuna seed.|Parameters, no seed.|Paramètres, aucune seed.|Parámetros, ninguna seed.
Controlli in corso...|Checks in progress...|Contrôles en cours...|Comprobando...
Attendi il risultato.|Wait for the result.|Attendez le résultat.|Espera el resultado.
Test superati|Tests passed|Tests réussis|Pruebas superadas
%d controlli PASS|%d checks PASS|%d contrôles PASS|%d controles PASS
Non e un audit di sicurezza.|This is not a security audit.|Ce n'est pas un audit de sécurité.|No es una auditoría de seguridad.
Attendi che il LED|Wait until the LED|Attendez que la LED|Espera a que el LED
smetta di lavorare.|stops working.|cesse son activité.|deje de trabajar.
Poi scollega.|Then unplug.|Puis débranchez.|Después desconecta.
Self-test completi...|Full self-tests...|Autotests complets...|Autopruebas completas...
Attendi.|Please wait.|Veuillez patienter.|Espera.
%d self-test PASS|%d self-tests PASS|%d autotests PASS|%d autopruebas PASS
Sessione annullata|Session cancelled|Session annulée|Sesión cancelada
Copia non confermata.|Copy not confirmed.|Copie non confirmée.|Copia sin confirmar.
Operazione bloccata|Operation blocked|Opération bloquée|Operación bloqueada
Generazione disabilitata.|Generation disabled.|Génération désactivée.|Generación desactivada.
Riesegui Test integrita.|Run Integrity test again.|Relancez le test d'intégrité.|Repite el test de integridad.
Controlla rete e swap.|Check network and swap.|Vérifiez réseau et swap.|Comprueba red y swap.
ERRORE - BLOCCATO|ERROR - LOCKED|ERREUR - BLOQUÉ|ERROR - BLOQUEADO
Avvio o self-test falliti.|Startup or self-tests failed.|Échec du démarrage ou des autotests.|Falló el inicio o las autopruebas.
Non usare seed reali.|Do not use real seeds.|N'utilisez pas de vraies seeds.|No uses seeds reales.
Centro: OK / K3: indietro|Centre: OK / Up: Back|Centre : OK / Haut : Retour|Centro: OK / Arriba: Atrás
Centro: avanti / K3: esci|Centre: next / Up: Back|Centre : suite / Haut : Retour|Centro: seguir / Arriba: Atrás
%d/%d Su/giu: scegli Centro: OK / K3: esci|%d/%d Up/down: choose Centre: OK|%d/%d Haut/bas : choix Centre : OK|%d/%d Arriba/abajo: elegir Centro: OK
Sin/des: pagina K2: avanti / K3: esci|Left/right: page Up: Back / Centre: next|Gauche/droite : page Haut : Retour|Izq./der.: página Arriba: Atrás
Sin/des: pagina Centro: avanti / K3: esci|Left/right: page Up: Back / Centre: next|Gauche/droite : page Haut : Retour|Izq./der.: página Arriba: Atrás
*=spazio / Centro: avanti K3: esci|*=space / Centre: next Up: Back|*=espace / Centre : suite Haut : Retour|*=espacio / Centro: seguir Arriba: Atrás
Frecce: scegli / Centro: salva K1: cancella / K3: esci|Arrows: choose / Centre: OK K1: undo / Up: Back|Flèches: choix / Centre: OK K1: effacer / Haut: retour|Flechas: elegir / Centro: OK K1: borrar / Arriba: atrás
Frecce: scegli / Centro: apri Su: Power|Arrows: choose / Centre: open Up: Power|Flèches : choix / Centre : ouvrir Haut : Power|Flechas: elegir / Centro: abrir Arriba: Power
Freccia: Centro per uscire|Back arrow: press Centre|Retour : appuyez au centre|Atrás: pulsa el centro
Su: indietro / Centro: apri|Up: Back / Centre: open|Haut : Retour / Centre : ouvrir|Arriba: Atrás / Centro: abrir
Wordlist 2048 parole|2048-word list|Liste de 2048 mots|Lista de 2048 palabras
Nessun duplicato BIP39|No BIP39 duplicates|Aucun doublon BIP39|Sin duplicados BIP39
Prima parola: abandon|First word: abandon|Premier mot : abandon|Primera palabra: abandon
Ultima parola: zoo|Last word: zoo|Dernier mot : zoo|Última palabra: zoo
Test vector BIP39 (5 lunghezze)|BIP39 vectors (5 lengths)|Vecteurs BIP39 (5 tailles)|Vectores BIP39 (5 longitudes)
Checksum invalido rilevato|Invalid checksum detected|Checksum invalide détecté|Checksum inválido detectado
Filesystem applicativo|Application filesystem|Système de fichiers applicatif|Sistema de archivos de la aplicación
Riproducibilità deterministica|Deterministic reproducibility|Reproductibilité déterministe|Reproducibilidad determinista
Wordlist integre (SHA-256)|Wordlist integrity (SHA-256)|Intégrité des listes (SHA-256)|Integridad de listas (SHA-256)
Input negativi rifiutati|Negative inputs rejected|Entrées négatives rejetées|Entradas negativas rechazadas
Parametri matematici|Mathematical parameters|Paramètres mathématiques|Parámetros matemáticos
Diceware mapping completo|Complete Diceware mapping|Correspondance Diceware complète|Mapeo Diceware completo
'''
CATALOG={}
for row in _DATA.strip().splitlines():
    cells=row.split('|')
    if len(cells)!=4:raise ValueError('Invalid translation row')
    CATALOG[cells[0]]=dict(zip(('en','fr','es'),cells[1:]))
_PATTERNS=[]
for key in CATALOG:
    if '%' not in key:continue
    parts=re.split(r'(%(?:\.\d+)?[dsf])',key);pattern=''
    for part in parts:
        if re.fullmatch(r'%(?:\.\d+)?[dsf]',part):
            pattern+=r'(.+?)' if part.endswith('s') else r'(\d+(?:\.\d+)?)'
        else:pattern+=re.escape(part)
    _PATTERNS.append((len(key),re.compile('^'+pattern+'$'),key))
_PATTERNS.sort(key=lambda item:item[0],reverse=True)

def language():return _language

def set_language(code):
    global _language
    if code not in dict(LANGUAGES):raise ValueError('Unsupported language')
    _language=code

def tr(text):
    text=str(text)
    if _language=='it':
        if text=='Space':return 'Spazio'
        if text=='Capitalise':return 'Iniziali maiuscole'
        if text=='None':return 'Nessuno'
        if text=='Centro: OK / K3: indietro':return 'Centro: OK / Su: freccia'
        if text=='Centro: avanti / K3: esci':return 'Centro: avanti / Su: freccia'
        if text=='Frecce: scegli / Centro: salva K1: cancella / K3: esci':return 'Frecce: scegli / Centro: salva K1: cancella / Su: freccia'
        if 'Su/giu: scegli Centro: OK / K3: esci' in text:return text.replace(' / K3: esci','')
        if text in ('Sin/des: pagina K2: avanti / K3: esci','Sin/des: pagina Centro: avanti / K3: esci'):return 'Sin/des: pagina / Su: freccia Centro: avanti'
        if text=='*=spazio / Centro: avanti K3: esci':return '*=spazio / Centro: avanti Su: freccia'
        return text
    if text in CATALOG:return CATALOG[text][_language]
    for _,pattern,key in _PATTERNS:
        match=pattern.fullmatch(text)
        if match:
            values=iter(match.groups())
            return re.sub(r'%(?:\.\d+)?[dsf]',lambda _:next(values),CATALOG[key][_language])
    page=re.fullmatch(r'(.+) (\d+/\d+)',text)
    if page:return tr(page[1])+' '+page[2]
    return text
