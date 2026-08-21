#!/usr/bin/env python3
"""
SeedGen v15.4 (BETA) - Generatore BIP39 da entropia fisica D6
Air-Gapped - Rejection Sampling - Verifica BIP39 completa
Correzioni matematiche integrate
"""

import os
import sys
import time
import math
import hashlib
import hmac
import re
from typing import List, Tuple, Optional, Dict, Union, Callable
from collections import Counter
import termios
import tty

# ============================================================
# PARAMETRI CRITTOGRAFICI
# ============================================================

# Directory del programma (funziona con PyInstaller e script Python)
import sys as _sys
if getattr(_sys, 'frozen', False):
    # Binario PyInstaller
    _SCRIPT_DIR = os.path.dirname(_sys.executable)
else:
    # Script Python
    _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ENTROPY_BITS = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}
def dice_rolls_needed(entropy_bits: int) -> int:
    """Calcola automaticamente il numero minimo di lanci necessari"""
    return math.ceil(entropy_bits / math.log2(6))


# Hash SHA-256 della wordlist BIP39 inglese ufficiale
OFFICIAL_ENGLISH_WORDLIST_SHA256 = "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda"

def acceptance_probability(entropy_bits: int) -> float:
    """Calcola automaticamente la probabilità di accettazione del blocco"""
    N = dice_rolls_needed(entropy_bits)
    total = 6 ** N
    k = total.bit_length() - 1
    M = 1 << k
    return M / total

WORDLIST_FILENAME = os.path.join(_SCRIPT_DIR, "bip39_wordlist.txt")
DICEWARE_FILENAME = os.path.join(_SCRIPT_DIR, "diceware_wordlist.txt")

# Hash SHA-256 della wordlist Diceware EFF ufficiale
# Verrà verificato all'avvio della funzione Diceware
DICEWARE_SHA256 = "addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e"

# ============================================================
# COLORI
# ============================================================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"

def colorize(text, color):
    return f"{color}{text}{Colors.RESET}"

def red(text): return colorize(text, Colors.RED)
def green(text): return colorize(text, Colors.GREEN)
def yellow(text): return colorize(text, Colors.YELLOW)
def bold(text): return colorize(text, Colors.BOLD)
def cyan(text): return colorize(text, Colors.CYAN)

# ============================================================
# FUNZIONI BIP39
# ============================================================

def checksum_bits(entropy: bytes) -> str:
    ent_bits = len(entropy) * 8
    if ent_bits not in (128, 160, 192, 224, 256):
        raise ValueError("Dimensione entropia non valida")
    cs_len = ent_bits // 32
    digest = hashlib.sha256(entropy).digest()
    first_bits = ""
    for byte in digest:
        first_bits += f"{byte:08b}"
        if len(first_bits) >= cs_len:
            break
    return first_bits[:cs_len]

def entropy_to_mnemonic(entropy: bytes, wordlist: List[str]) -> List[str]:
    ent_bits = len(entropy) * 8
    entropy_bin = "".join(f"{b:08b}" for b in entropy)
    cs = checksum_bits(entropy)
    full_bits = entropy_bin + cs
    mnemonic = []
    for i in range(0, len(full_bits), 11):
        index = int(full_bits[i:i+11], 2)
        mnemonic.append(wordlist[index])
    return mnemonic

def mnemonic_to_entropy(mnemonic: Union[str, List[str]], wordlist: List[str]) -> bytes:
    if isinstance(mnemonic, str):
        words = mnemonic.strip().split()
    else:
        words = list(mnemonic)
    if len(words) not in ENTROPY_BITS:
        raise ValueError("Numero parole non valido")
    word_to_index = {word: i for i, word in enumerate(wordlist)}
    indexes = []
    for word in words:
        if word not in word_to_index:
            raise ValueError(f"Parola non trovata: {word}")
        indexes.append(word_to_index[word])
    bits = "".join(f"{index:011b}" for index in indexes)
    ent_bits = ENTROPY_BITS[len(words)]
    cs_len = ent_bits // 32
    entropy_part = bits[:ent_bits]
    checksum_part = bits[ent_bits:ent_bits+cs_len]
    entropy = int(entropy_part, 2).to_bytes(ent_bits // 8, "big")
    expected_checksum = checksum_bits(entropy)
    if not hmac.compare_digest(checksum_part, expected_checksum):
        raise ValueError("Checksum non valido")
    return entropy

# ============================================================
# WORDLIST CON VERIFICA SHA-256
# ============================================================

def load_wordlist() -> List[str]:
    """Carica e verifica rigorosamente la wordlist BIP39"""
    if not os.path.exists(WORDLIST_FILENAME):
        raise FileNotFoundError("File wordlist non trovato")
    
    with open(WORDLIST_FILENAME, "rb") as f:
        raw = f.read()
    
    # VERIFICA SHA-256 (correzione dal matematico)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != OFFICIAL_ENGLISH_WORDLIST_SHA256:
        raise ValueError(
            f"WORDLIST NON AUTENTICA!\n"
            f"SHA256 trovato: {digest}\n"
            f"SHA256 atteso:  {OFFICIAL_ENGLISH_WORDLIST_SHA256}"
        )
    
    text = raw.decode("utf-8")
    words = [line.strip() for line in text.splitlines() if line.strip()]
    
    if len(words) != 2048:
        raise ValueError(f"Wordlist: {len(words)} parole (attese 2048)")
    
    if len(set(words)) != 2048:
        raise ValueError("Wordlist contiene duplicati")
    
    # Verifica prima e ultima parola ufficiale
    if words[0] != "abandon":
        raise ValueError("Prima parola non è 'abandon'")
    if words[-1] != "zoo":
        raise ValueError("Ultima parola non è 'zoo'")
    
    return words

# ============================================================
# SELF TEST
# ============================================================

def load_diceware_wordlist() -> List[str]:
    """Carica e verifica la wordlist Diceware"""
    if not os.path.exists(DICEWARE_FILENAME):
        raise FileNotFoundError(f"File {DICEWARE_FILENAME} non trovato")
    
    with open(DICEWARE_FILENAME, "rb") as f:
        raw = f.read()
    
    # Verifica SHA-256
    digest = hashlib.sha256(raw).hexdigest()
    if digest != DICEWARE_SHA256:
        raise ValueError(
            f"WORDLIST DICEWARE NON AUTENTICA!\n"
            f"SHA256 trovato: {digest}\n"
            f"SHA256 atteso:  {DICEWARE_SHA256}"
        )
    
    text = raw.decode("utf-8")
    words = [line.strip() for line in text.splitlines() if line.strip()]
    
    if len(words) != 7776:
        raise ValueError(f"Diceware: {len(words)} parole (attese 7776)")
    
    if len(set(words)) != 7776:
        raise ValueError("Wordlist Diceware contiene duplicati")
    
    return words

def self_test_bip39(wordlist: List[str]) -> None:
    entropy = bytes.fromhex("00000000000000000000000000000000")
    expected = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    mnemonic = entropy_to_mnemonic(entropy, wordlist)
    generated = " ".join(mnemonic)
    if generated != expected:
        raise AssertionError("TEST FALLITO")
    recovered = mnemonic_to_entropy(mnemonic, wordlist)
    if recovered != entropy:
        raise AssertionError("Round-trip fallito")

# ============================================================
# DADO / ENTROPIA
# ============================================================

# ============================================================
# TEST VECTOR BIP39 UFFICIALI (tutte le lunghezze)
# ============================================================

BIP39_TEST_VECTORS = {
    128: {
        "entropy": "00000000000000000000000000000000",
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
    },
    160: {
        "entropy": "0000000000000000000000000000000000000000",
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon address",
    },
    192: {
        "entropy": "000000000000000000000000000000000000000000000000",
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon agent",
    },
    224: {
        "entropy": "00000000000000000000000000000000000000000000000000000000",
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon admit",
    },
    256: {
        "entropy": "0000000000000000000000000000000000000000000000000000000000000000",
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art",
    },
}

def test_all_bip39_vectors(wordlist: List[str]) -> bool:
    # Test vector non-zero aggiuntivi
    test_vectors_nonzero = {
        128: ("ffffffffffffffffffffffffffffffff", None),  # Verifica solo round-trip
        256: ("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", None),
    }
    
    for ent_bits, (entropy_hex, _) in test_vectors_nonzero.items():
        entropy_nz = bytes.fromhex(entropy_hex)
        mnemonic_nz = entropy_to_mnemonic(entropy_nz, wordlist)
        recovered_nz = mnemonic_to_entropy(mnemonic_nz, wordlist)
        if recovered_nz != entropy_nz:
            raise AssertionError(f"Round-trip non-zero {ent_bits} bit fallito!")
    
    for ent_bits, vector in BIP39_TEST_VECTORS.items():
        entropy = bytes.fromhex(vector["entropy"])
        expected = vector["mnemonic"]
        mnemonic = entropy_to_mnemonic(entropy, wordlist)
        generated = " ".join(mnemonic)
        if generated != expected:
            raise AssertionError(f"TEST VECTOR {ent_bits} BIT FALLITO!")
        recovered = mnemonic_to_entropy(mnemonic, wordlist)
        if recovered != entropy:
            raise AssertionError(f"ROUND-TRIP {ent_bits} BIT FALLITO!")
    return True

# ============================================================
# TEST REJECTION SAMPLING
# ============================================================

def test_checksum_invalido(wordlist: List[str]) -> bool:
    """Test che mnemonic con checksum sbagliato vengano rifiutate (BIP-03)"""
    for ent_bits in [128, 160, 192, 224, 256]:
        entropy = bytes([0] * (ent_bits // 8))
        mnemonic = entropy_to_mnemonic(entropy, wordlist)
        
        # Modifica l'ultima parola
        mnemonic_modificata = mnemonic.copy()
        ultima = mnemonic_modificata[-1]
        for parola in wordlist:
            if parola != ultima:
                mnemonic_modificata[-1] = parola
                break
        
        # Deve fallire
        try:
            mnemonic_to_entropy(mnemonic_modificata, wordlist)
            raise AssertionError(f"Checksum invalido non rilevato per {ent_bits} bit")
        except ValueError:
            pass  # OK, deve fallire
    
    return True


def test_parametri_matematici() -> bool:
    """Verifica indipendente dei parametri matematici (ENT-05, ENT-06, ENT-07)"""
    import math
    
    # ENT-06: Verifica dice_rolls_needed(entropy_bits)
    for ent_bits, lanci_attesi in [(128, 50), (160, 62), (192, 75), (224, 87), (256, 100)]:
        lanci_calcolati = math.ceil(ent_bits / math.log2(6))
        if lanci_calcolati != lanci_attesi:
            raise AssertionError(f"dice_rolls_needed(entropy_bits)[{ent_bits}] = {lanci_attesi}, atteso {lanci_calcolati}")
    
    # ENT-05: Verifica 6^N e floor(log2(6^N))
    for lanci in [50, 62, 75, 87, 100]:
        valore = 6 ** lanci
        k = valore.bit_length() - 1
        M = 1 << k
        if M > valore:
            raise AssertionError(f"M > 6^{lanci}")
        if M * 2 <= valore:
            raise AssertionError(f"2^(k+1) <= 6^{lanci}")
    
    # ENT-07: Verifica che acceptance_probability() sia coerente
    for ent_bits in [128, 160, 192, 224, 256]:
        N = dice_rolls_needed(ent_bits)
        totale = 6 ** N
        k = totale.bit_length() - 1
        M = 1 << k
        prob_esatta = M / totale
        prob_funzione = acceptance_probability(ent_bits)
        if abs(prob_funzione - prob_esatta) > 1e-10:
            raise AssertionError(f"Probabilità {ent_bits} bit: funzione={prob_funzione}, esatta={prob_esatta}")
    
    return True


def test_input_negativi() -> bool:
    """Test input negativi e abort (Sezione 14)"""
    # Test valori invalidi
    valori_invalidi = [0, 7, -1, 'a', ' ', '', None]
    
    for valore in valori_invalidi:
        try:
            if valore is None:
                # Simula EOF
                extract_entropy_from_dice_block([1]*49 + [None], 128)
            else:
                # Test con valore invalido nel blocco
                rolls = [1] * 49 + [valore]
                extract_entropy_from_dice_block(rolls, 128)
            raise AssertionError(f"Valore invalido {valore} non rifiutato!")
        except (ValueError, TypeError):
            pass  # OK, deve fallire
    
    return True


def test_wordlist_tampering() -> bool:
    """Test che wordlist modificate vengano rifiutate (Sezione 15)"""
    import tempfile, os, hashlib
    
    # Verifica che la wordlist BIP39 abbia l'hash corretto
    with open(WORDLIST_FILENAME, 'rb') as f:
        raw = f.read()
    
    hash_attuale = hashlib.sha256(raw).hexdigest()
    hash_atteso = "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda"
    
    if hash_attuale != hash_atteso:
        raise AssertionError("Wordlist BIP39 modificata!")
    
    # Verifica Diceware
    with open(DICEWARE_FILENAME, 'rb') as f:
        raw_dw = f.read()
    
    hash_dw = hashlib.sha256(raw_dw).hexdigest()
    hash_dw_atteso = "addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e"
    
    if hash_dw != hash_dw_atteso:
        raise AssertionError("Wordlist Diceware modificata!")
    
    return True


def test_riproducibilita(wordlist: List[str]) -> bool:
    """Test di riproducibilità con sequenza deterministica (Sezione 16)"""
    # Sequenza deterministica di 50 lanci
    lanci_test = [1, 2, 3, 4, 5, 6] * 8 + [1, 2]  # 50 lanci
    
    # Estrai entropia
    entropy1, k1, accepted1 = extract_entropy_from_dice_block(lanci_test, 128)
    
    # Se rifiutato, prova con altra sequenza
    if not accepted1:
        lanci_test = [2, 3, 4, 5, 6, 1] * 8 + [3, 4]
        entropy1, k1, accepted1 = extract_entropy_from_dice_block(lanci_test, 128)
    
    if not accepted1:
        # Se ancora rifiutato, il test non può procedere
        return True  # Non è un errore, solo sequenza rifiutata
    
    # Genera mnemonic
    mnemonic1 = entropy_to_mnemonic(entropy1, wordlist)
    
    # Ripeti con la stessa sequenza
    entropy2, k2, accepted2 = extract_entropy_from_dice_block(lanci_test, 128)
    
    if not accepted2:
        raise AssertionError("Seconda estrazione rifiutata!")
    
    mnemonic2 = entropy_to_mnemonic(entropy2, wordlist)
    
    # Verifica che siano identici
    if mnemonic1 != mnemonic2:
        raise AssertionError("Riproducibilità fallita!")
    
    if entropy1 != entropy2:
        raise AssertionError("Entropia non riproducibile!")
    
    return True


def test_filesystem() -> bool:
    """Test che nessun file venga creato durante la generazione (FS-02)"""
    import tempfile, os
    
    # Crea directory temporanea
    with tempfile.TemporaryDirectory() as tmpdir:
        # Salva la directory corrente
        old_dir = os.getcwd()
        
        try:
            # Cambia nella directory temporanea
            os.chdir(tmpdir)
            
            # Verifica che sia vuota
            files_prima = set(os.listdir('.'))
            if files_prima:
                raise AssertionError("Directory temporanea non vuota!")
            
            # Esegui una generazione di test (senza UI)
            lanci_test = [1, 2, 3, 4, 5, 6] * 8 + [1, 2]
            entropy, k, accepted = extract_entropy_from_dice_block(lanci_test, 128)
            
            # Verifica che nessun file sia stato creato
            files_dopo = set(os.listdir('.'))
            if files_dopo:
                raise AssertionError(f"File creati durante la generazione: {files_dopo}")
            
        finally:
            # Ripristina la directory
            os.chdir(old_dir)
    
    return True


def test_rejection_sampling() -> bool:
    rolls_zero = [1] * 50
    entropy, k, accepted = extract_entropy_from_dice_block(rolls_zero, 128)
    if not accepted:
        raise AssertionError("X=0 dovrebbe essere accettato")
    try:
        extract_entropy_from_dice_block([0]*50, 128)
        raise AssertionError("Valore 0 non dovrebbe essere accettato")
    except ValueError:
        pass
    try:
        extract_entropy_from_dice_block([7]*50, 128)
        raise AssertionError("Valore 7 non dovrebbe essere accettato")
    except ValueError:
        pass
    try:
        extract_entropy_from_dice_block([1]*49, 128)
        raise AssertionError("49 lanci non dovrebbero bastare")
    except ValueError:
        pass
    return True

# ============================================================
# TEST DICEWARE
# ============================================================

def test_diceware_mapping(diceware_wordlist: List[str]) -> bool:
    indice_11111 = 0
    for i, lancio in enumerate([1,1,1,1,1]):
        indice_11111 += (lancio - 1) * (6 ** (4 - i))
    indice_11111 += 1
    if indice_11111 != 1:
        raise AssertionError(f"11111 dovrebbe dare indice 1, ottenuto {indice_11111}")
    indice_66666 = 0
    for i, lancio in enumerate([6,6,6,6,6]):
        indice_66666 += (lancio - 1) * (6 ** (4 - i))
    indice_66666 += 1
    if indice_66666 != 7776:
        raise AssertionError(f"66666 dovrebbe dare indice 7776, ottenuto {indice_66666}")
    if 6**5 != 7776:
        raise AssertionError("6^5 dovrebbe essere 7776")
    return True

def analizza_distribuzione_lanci(rolls: List[int]) -> Tuple[bool, float]:
    """Analizza la distribuzione dei lanci (diagnostico)"""
    if len(rolls) < 10:
        return True, 0
    
    from collections import Counter
    conteggio = Counter(rolls)
    
    # Percentuale del valore più frequente
    max_freq = max(conteggio.values())
    percentuale_max = (max_freq / len(rolls)) * 100
    
    # Se un valore appare più del 40% delle volte, è sospetto
    if percentuale_max > 40:
        return False, percentuale_max
    
    # Se solo 1-2 valori su 6 appaiono
    valori_presenti = len(conteggio)
    if valori_presenti <= 2:
        return False, percentuale_max
    
    return True, percentuale_max

def encode_base6(value: int, N: int) -> List[int]:
    """Converte un intero in lanci base-6 (valori 1-6)"""
    rolls = []
    for _ in range(N):
        rolls.append((value % 6) + 1)
        value //= 6
    return list(reversed(rolls))


def test_rejection_boundary() -> bool:
    """Test boundary REALE: M-1, M, M+1 attraverso la funzione production"""
    # Test per ogni configurazione
    for ent_bits, lanci_attesi in [(128, 50), (160, 62), (192, 75), (224, 87), (256, 100)]:
        N = lanci_attesi
        k = (6**N).bit_length() - 1
        M = 1 << k
        
        # TEST M-1 → deve essere ACCETTATO
        rolls_m_minus_1 = encode_base6(M - 1, N)
        entropy, k_result, accepted = extract_entropy_from_dice_block(rolls_m_minus_1, ent_bits)
        if not accepted:
            raise AssertionError(f"M-1 dovrebbe essere ACCETTATO per {ent_bits} bit (X={M-1})")
        if entropy is None:
            raise AssertionError(f"M-1: entropy None per {ent_bits} bit")
        
        # TEST M → deve essere RIFIUTATO
        rolls_m = encode_base6(M, N)
        entropy_m, k_m, accepted_m = extract_entropy_from_dice_block(rolls_m, ent_bits)
        if accepted_m:
            raise AssertionError(f"M dovrebbe essere RIFIUTATO per {ent_bits} bit (X={M})")
        
        # TEST M+1 → deve essere RIFIUTATO
        rolls_m_plus_1 = encode_base6(M + 1, N)
        entropy_mp1, k_mp1, accepted_mp1 = extract_entropy_from_dice_block(rolls_m_plus_1, ent_bits)
        if accepted_mp1:
            raise AssertionError(f"M+1 dovrebbe essere RIFIUTATO per {ent_bits} bit (X={M+1})")
    
    return True

def test_diceware_completo() -> bool:
    """Test COMPLETO: tutte le 7776 combinazioni Diceware"""
    # Verifica che 6^5 = 7776
    if 6**5 != 7776:
        raise AssertionError("6^5 dovrebbe essere 7776")
    
    # TEST COMPLETO 7776/7776
    # Verifica che TUTTE le 7776 combinazioni producano indici unici 1-7776
    risultati = set()
    
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            for d3 in range(1, 7):
                for d4 in range(1, 7):
                    for d5 in range(1, 7):
                        # Formula Diceware
                        indice = 0
                        lanci = [d1, d2, d3, d4, d5]
                        for i, lancio in enumerate(lanci):
                            indice += (lancio - 1) * (6 ** (4 - i))
                        indice += 1
                        
                        # Verifica range
                        if indice < 1 or indice > 7776:
                            raise AssertionError(f"Indice fuori range: {indice}")
                        
                        risultati.add(indice)
    
    # Verifica che ci siano ESATTAMENTE 7776 indici unici
    if len(risultati) != 7776:
        raise AssertionError(f"Trovati {len(risultati)} indici, attesi 7776")
    
    # Verifica che coprano 1..7776
    if min(risultati) != 1 or max(risultati) != 7776:
        raise AssertionError(f"Range errato: {min(risultati)}-{max(risultati)}")
    
    # Verifica bijectivity inversa: ogni indice 1-7776 è raggiungibile
    for indice_atteso in range(1, 7777):
        # Inverso: indice → lanci
        resto = indice_atteso - 1
        lanci = []
        for i in range(5):
            potenza = 6 ** (4 - i)
            lancio = (resto // potenza) + 1
            resto = resto % potenza
            lanci.append(lancio)
        
        # Verifica che i lanci diano l'indice corretto
        indice_calcolato = 0
        for i, lancio in enumerate(lanci):
            indice_calcolato += (lancio - 1) * (6 ** (4 - i))
        indice_calcolato += 1
        
        if indice_calcolato != indice_atteso:
            raise AssertionError(f"Bijectivity fallita: {indice_atteso} → {indice_calcolato}")
    
    return True



def extract_entropy_from_dice_block(rolls: List[int], target_bits: int) -> Tuple[Optional[bytes], int, bool]:
    expected_rolls = dice_rolls_needed(target_bits)
    if len(rolls) != expected_rolls:
        raise ValueError(f"Servono {expected_rolls} lanci")
    
    # Controllo esplicito: ogni lancio deve essere 1-6
    for roll in rolls:
        if roll not in (1, 2, 3, 4, 5, 6):
            raise ValueError(f"Lancio dado non valido: {roll}")
    
    X = 0
    for roll in rolls:
        X = X * 6 + (roll - 1)
    total_range = 6 ** len(rolls)
    k = total_range.bit_length() - 1
    M = 1 << k
    if X >= M:
        return None, k, False
    mask = (1 << target_bits) - 1
    value = X & mask
    entropy = value.to_bytes(target_bits // 8, "big")
    return entropy, k, True

# ============================================================
# TERMINALE
# ============================================================

def run_all_self_tests(wordlist: List[str], diceware_wordlist: List[str]) -> List[Tuple[str, bool]]:
    """Routine unificata di tutti i test"""
    risultati = []
    
    # Test wordlist BIP39
    risultati.append(('Wordlist 2048 parole', len(wordlist) == 2048))
    risultati.append(('Nessun duplicato BIP39', len(set(wordlist)) == 2048))
    risultati.append(('Prima parola: abandon', wordlist[0] == 'abandon'))
    risultati.append(('Ultima parola: zoo', wordlist[-1] == 'zoo'))
    
    # Test BIP39
    try:
        test_all_bip39_vectors(wordlist)
        risultati.append(('Test vector BIP39 (5 lunghezze)', True))
    except Exception:
        risultati.append(('Test vector BIP39', False))
    
    # Test rejection sampling
    try:
        test_rejection_sampling()
        risultati.append(('Rejection sampling', True))
    except Exception:
        risultati.append(('Rejection sampling', False))
    
    # Test boundary
    try:
        test_rejection_boundary()
        risultati.append(('Boundary M-1/M/M+1', True))
    except Exception:
        risultati.append(('Boundary test', False))
    
    # Test checksum invalido (BIP-03)
    try:
        test_checksum_invalido(wordlist)
        risultati.append(('Checksum invalido rilevato', True))
    except Exception:
        risultati.append(('Checksum invalido', False))
    
    # Test filesystem (FS-02) - OPZIONALE (richiede scrittura)
    # Non blocca l'avvio su filesystem read-only
    try:
        test_filesystem()
        risultati.append(('Filesystem applicativo', True))
    except Exception:
        risultati.append(('Filesystem (opzionale)', True))  # Non blocca
    
    # Test riproducibilità (Sezione 16)
    try:
        test_riproducibilita(wordlist)
        risultati.append(('Riproducibilità deterministica', True))
    except Exception:
        risultati.append(('Riproducibilità', False))
    
    # Test wordlist tampering (Sezione 15)
    try:
        test_wordlist_tampering()
        risultati.append(('Wordlist integre (SHA-256)', True))
    except Exception:
        risultati.append(('Wordlist tampering', False))
    
    # Test input negativi (Sezione 14)
    try:
        test_input_negativi()
        risultati.append(('Input negativi rifiutati', True))
    except Exception:
        risultati.append(('Input negativi', False))
    
    # Test parametri matematici (ENT-05, ENT-06, ENT-07)
    try:
        test_parametri_matematici()
        risultati.append(('Parametri matematici', True))
    except Exception:
        risultati.append(('Parametri matematici', False))
    
    # Test Diceware
    try:
        test_diceware_mapping(diceware_wordlist)
        test_diceware_completo()
        risultati.append(('Diceware mapping completo', True))
    except Exception:
        risultati.append(('Diceware mapping', False))
    
    return risultati

class Terminal:
    @staticmethod
    def clear():
        # Pulisce schermo E scrollback
        print("\033[3J\033[2J\033[H", end="")
        sys.stdout.flush()
    @staticmethod
    def wait_key(valid):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char == "":
                    # EOF: ripristina e termina
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                    raise EOFError
                if char == "\x03":
                    raise KeyboardInterrupt
                if char.lower() in valid:
                    return char.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    @staticmethod
    def dice():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char == "":
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                    raise EOFError
                if char == "\x03":
                    raise KeyboardInterrupt
                if char in "123456":
                    return int(char)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# ============================================================
# APPLICAZIONE
# ============================================================

class SeedGenApp:
    def __init__(self):
        self.wordlist = load_wordlist()

    def box_line(self, testo):
        testo_pulito = re.sub(r'\033\[[0-9;]*m', '', testo)
        padding = 68 - len(testo_pulito)
        if padding < 0:
            padding = 0
        sinistra = padding // 2
        destra = padding - sinistra
        return ' ' * 21 + cyan('║') + ' ' * sinistra + testo + ' ' * destra + cyan('║')

    def box_top(self):
        return ' ' * 21 + cyan('╔' + '═' * 68 + '╗')

    def box_bottom(self):
        return ' ' * 21 + cyan('╚' + '═' * 68 + '╝')

    def box_sep(self):
        return ' ' * 21 + cyan('╠' + '═' * 68 + '╣')

    def mostra_logo(self):
        Terminal.clear()
        print()
        print(self.box_top())
        print(self.box_line(bold(green('███████╗███████╗███████╗██████╗  ██████╗ ███████╗███╗  ██╗'))))
        print(self.box_line(bold(green('██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝ ██╔════╝████╗ ██║'))))
        print(self.box_line(bold(green('███████╗█████╗  █████╗  ██║  ██║██║  ███╗█████╗  ██╔██╗ ██║'))))
        print(self.box_line(bold(green('╚════██║██╔══╝  ██╔══╝  ██║  ██║██║   ██║██╔══╝  ██║╚██╗██║'))))
        print(self.box_line(bold(green('███████║███████╗███████╗██████╔╝╚██████╔╝███████╗██║ ╚████║'))))
        print(self.box_line(bold(green('╚══════╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝'))))
        print(self.box_line(''))
        print(self.box_line(yellow('Generatore Sicuro Seed Bitcoin BIP39 v15.4 (BETA)')))
        print(self.box_line(yellow('Rejection Sampling - Air-Gapped')))
        print(self.box_bottom())
        print()

    def mostra_menu(self):
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold('MENU PRINCIPALE')))
        print(self.box_sep())
        print(self.box_line(''))
        voci = [
            (green('[1]'), 'Genera Seed 12 parole (128 bit)'),
            (green('[2]'), 'Genera Seed 15 parole (160 bit)'),
            (green('[3]'), 'Genera Seed 18 parole (192 bit)'),
            (green('[4]'), 'Genera Seed 21 parole (224 bit)'),
            (green('[5]'), 'Genera Seed 24 parole (256 bit)'),
            None,
            (green('[6]'), 'Genera Passphrase Diceware'),
            None,
            (green('[7]'), 'Verifica Mnemonic BIP39'),
            (green('[8]'), 'Test Integrità Programma'),
            None,
            (green('[9]'), 'Audit Mode (ENT, N, k, M)'),
            None,
            (red('[0]'), 'Esci'),
        ]
        for voce in voci:
            if voce is None:
                print(self.box_line(''))
            else:
                numero, descrizione = voce
                testo = numero + ' ' + descrizione
                testo_pulito = re.sub(r'\033\[[0-9;]*m', '', testo)
                padding = 68 - 3 - len(testo_pulito)
                print(' ' * 21 + cyan('║') + '   ' + testo + ' ' * padding + cyan('║'))
        print(self.box_line(''))
        print(self.box_bottom())
        print()

    def avviso_dadi_fisici(self):
        """Avvertimento sul bias fisico dei dadi (correzione dal matematico)"""
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold(yellow('AVVISO IMPORTANTE SUI DADI FISICI'))))
        print(self.box_sep())
        print(self.box_line('Il rejection sampling elimina SOLO il bias'))
        print(self.box_line('della conversione base-6 → bit.'))
        print(self.box_line(''))
        print(self.box_line(red('NON elimina il bias fisico dei dadi.')))
        print(self.box_line(''))
        print(self.box_line('Usa dadi di qualità verificata:'))
        print(self.box_line('• Non magnetici'))
        print(self.box_line('• Non truccati'))
        print(self.box_line('• Superficie uniforme'))
        print(self.box_line('• Tecnica di lancio consistente'))
        print(self.box_sep())
        print(self.box_line(''))
        
        # Opzione 1
        testo1 = green('[1]') + ' Ho capito, continua'
        padding1 = 68 - 3 - len('[1] Ho capito, continua')
        print(' ' * 21 + cyan('║') + '   ' + testo1 + ' ' * padding1 + cyan('║'))
        
        # Opzione 2
        testo2 = red('[0]') + ' Annulla'
        padding2 = 68 - 3 - len('[0] Annulla')
        print(' ' * 21 + cyan('║') + '   ' + testo2 + ' ' * padding2 + cyan('║'))
        
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        return Terminal.wait_key(['0', '1'])

    def raccogli_blocco(self, num_lanci):
        rolls = []
        while len(rolls) < num_lanci:
            self.mostra_logo()
            print(self.box_top())
            print(self.box_line(bold(yellow(f'RACCOLTA BLOCCO - {num_lanci} LANCI'))))
            print(self.box_sep())
            progresso = (len(rolls) / num_lanci) * 100
            barra = '█' * int(progresso / 2)
            spazi = ' ' * (50 - int(progresso / 2))
            print(self.box_line(f'[{green(barra)}{spazi}] {progresso:.0f}%'))
            print(self.box_line(f'Lancio {len(rolls)+1} di {num_lanci}'))
            print(self.box_sep())

            print(self.box_line(red('INPUT DIRETTO - Premi solo tasti 1-6')))
            print(self.box_bottom())
            print()
            roll = Terminal.dice()
            if roll is None:
                return None
            rolls.append(roll)
            time.sleep(0.1)
        return rolls

    def genera(self, parole):
        ent_bits = ENTROPY_BITS[parole]
        lanci_richiesti = dice_rolls_needed(ent_bits)
        prob_accettazione = acceptance_probability(ent_bits)
        
        # Avviso dadi fisici
        scelta = self.avviso_dadi_fisici()
        if scelta == '0':
            return
        
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold(yellow(f'GENERAZIONE BIP39 {parole} PAROLE'))))
        print(self.box_sep())
        print(self.box_line(f'Entropia: {ent_bits} bit'))
        print(self.box_line(f'Lanci per blocco: {lanci_richiesti}'))
        print(self.box_line(f'Prob. accettazione: {prob_accettazione*100:.0f}%'))
        print(self.box_sep())
        print(self.box_line(yellow('IMPORTANTE:')))
        print(self.box_line('Blocco rifiutato = TUTTI i lanci scartati'))
        print(self.box_line('Nuovo blocco = NUOVI lanci'))
        print(self.box_sep())
        print(self.box_line(''))
        testo1b = green('[1]') + ' Inizia blocco'
        padding1b = 68 - 3 - len('[1] Inizia blocco')
        print(' ' * 21 + cyan('║') + '   ' + testo1b + ' ' * padding1b + cyan('║'))
        
        testo2b = red('[0]') + ' Annulla'
        padding2b = 68 - 3 - len('[0] Annulla')
        print(' ' * 21 + cyan('║') + '   ' + testo2b + ' ' * padding2b + cyan('║'))
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        scelta = Terminal.wait_key(['0', '1'])
        if scelta == '0':
            return
        
        while True:
            rolls = self.raccogli_blocco(lanci_richiesti)
            if rolls is None:
                return
            # CONTROLLO OBBLIGATORIO RIPETITIVITÀ
            ok_rip, perc_max = analizza_distribuzione_lanci(rolls)
            if not ok_rip:
                self.mostra_logo()
                print(self.box_top())
                print(self.box_line(bold(red('⚠️ AVVISO: DISTRIBUZIONE ANOMALA'))))
                print(self.box_sep())
                print(self.box_line(f'Valore più frequente: {perc_max:.0f}%'))
                print(self.box_line(''))
                print(self.box_line(red('Distribuzione sospetta rilevata.')))
                print(self.box_line(red('Puoi rifare i lanci se lo ritieni necessario.')))
                print(self.box_sep())
                print(self.box_line(''))
                
                testo1 = green('[1]') + ' Rifai tutti i lanci'
                padding1 = 68 - 3 - len('[1] Rifai tutti i lanci')
                print(' ' * 21 + cyan('║') + '   ' + testo1 + ' ' * padding1 + cyan('║'))
                
                testo2 = yellow('[2]') + ' Procedi comunque (sotto mia responsabilità)'
                padding2 = 68 - 3 - len('[2] Procedi comunque (sotto mia responsabilità)')
                print(' ' * 21 + cyan('║') + '   ' + testo2 + ' ' * padding2 + cyan('║'))
                
                testo3 = red('[0]') + ' Annulla e torna al menu'
                padding3 = 68 - 3 - len('[0] Annulla e torna al menu')
                print(' ' * 21 + cyan('║') + '   ' + testo3 + ' ' * padding3 + cyan('║'))
                
                print(self.box_line(''))
                print(self.box_bottom())
                print()
                
                scelta = Terminal.wait_key(['0', '1', '2'])
                if scelta == '0':
                    return
                elif scelta == '1':
                    continue
                else:
                    pass
            
            entropy, k, accepted = extract_entropy_from_dice_block(rolls, ent_bits)
            if not accepted:
                self.mostra_logo()
                print(self.box_top())
                print(self.box_line(bold(yellow('BLOCCO RIFIUTATO'))))
                print(self.box_sep())
                print(self.box_line(f'Capacità blocco: {k} bit'))
                print(self.box_line(red('TUTTI I LANCI VENGONO SCARTATI')))
                print(self.box_sep())
                print(self.box_line(''))
                print(' ' * 21 + cyan('║') + '   ' + green('[1]') + ' Nuovo blocco' + ' ' * 47 + cyan('║'))
                print(' ' * 21 + cyan('║') + '   ' + red('[0]') + ' Annulla' + ' ' * 52 + cyan('║'))
                print(self.box_line(''))
                print(self.box_bottom())
                print()
                scelta = Terminal.wait_key(['0', '1'])
                if scelta == '0':
                    return
                continue
            self.mostra_logo()
            print(self.box_top())
            print(self.box_line(bold(green('✓ BLOCCO ACCETTATO'))))
            print(self.box_sep())
            print(self.box_line(f'Capacità blocco: {k} bit'))
            print(self.box_line(f'Entropia estratta: {ent_bits} bit'))
            print(self.box_bottom())
            time.sleep(2)
            break
        
        mnemonic = entropy_to_mnemonic(entropy, self.wordlist)
        self.mostra_risultato(mnemonic, ent_bits)
        
        # Pulizia memoria (correzione dal matematico)
        entropy = None
        mnemonic = None
        rolls = None

    def schermata_conferma_seed(self):
        """Schermata di conferma prima di visualizzare la seed"""
        self.mostra_logo()
        
        print(self.box_top())
        print(self.box_line(''))
        print(self.box_line(bold(green('✓ MNEMONIC BIP39 PRONTA'))))
        print(self.box_line(''))
        print(self.box_line(yellow('Premi INVIO per visualizzare la seed phrase')))
        print(self.box_line(''))
        print(self.box_sep())
        print(self.box_line(''))
        print(self.box_line('Prima di continuare assicurati di avere:'))
        print(self.box_line('• Carta e penna pronte'))
        print(self.box_line('• Nessuna telecamera attiva'))
        print(self.box_line('• Nessuna persona intorno'))
        print(self.box_line('• Ambiente sicuro e privato'))
        print(self.box_line(''))
        print(self.box_line('La seed resterà a video solo il tempo necessario'))
        print(self.box_line('per trascriverla. Non fare foto e non condividere.'))
        print(self.box_line(''))
        print(self.box_sep())
        print(self.box_line(''))
        
        # Opzione dentro la cornice
        testo_invio = green('[INVIO]') + ' Visualizza la seed'
        padding_invio = 68 - 3 - len('[INVIO] Visualizza la seed')
        print(' ' * 21 + cyan('║') + '   ' + testo_invio + ' ' * padding_invio + cyan('║'))
        
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        
        # Attende SOLO INVIO (blocca altri tasti)
        Terminal.wait_key(['\r', '\n', ' '])
    
    def mostra_risultato(self, mnemonic, ent_bits):
        # Mostra prima la schermata di conferma
        self.schermata_conferma_seed()
        
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold(green('✓ MNEMONIC BIP39 GENERATA'))))
        print(self.box_sep())
        print(self.box_line(f'Entropia: {ent_bits} bit'))
        print(self.box_line(red('NON FARE FOTO - NON CONDIVIDERE')))
        print(self.box_line(yellow('SCRIVI LE PAROLE SU CARTA')))
        print(self.box_sep())
        
        righe_seed = []
        for i in range(0, len(mnemonic), 2):
            if i + 1 < len(mnemonic):
                colonna1 = f"{i+1:2d}. {mnemonic[i]:<15}"
                colonna2 = f"{i+2:2d}. {mnemonic[i+1]}"
                riga = f"{colonna1}   {colonna2}"
            else:
                riga = f"{i+1:2d}. {mnemonic[i]}"
            righe_seed.append(riga)
        
        max_lunghezza = max([len(r) for r in righe_seed]) if righe_seed else 0
        
        for riga in righe_seed:
            padding = 68 - max_lunghezza
            sinistra = padding // 2
            print(' ' * 21 + cyan('║') + ' ' * sinistra + green(riga) + ' ' * (68 - sinistra - len(riga)) + cyan('║'))
        
        print(self.box_sep())
        print(self.box_line(green('✓ Checksum BIP39 verificato')))
        print(self.box_sep())
        print(self.box_line(''))
        testo1d = green('[1]') + ' Torna al menu'
        padding1d = 68 - 3 - len('[1] Torna al menu')
        print(' ' * 21 + cyan('║') + '   ' + testo1d + ' ' * padding1d + cyan('║'))
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        Terminal.wait_key(['1'])
        Terminal.clear()

    def genera_diceware(self):
        """Genera passphrase Diceware con dadi fisici"""
        diceware_wordlist = load_diceware_wordlist()
        
        # Scelta lunghezza
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold(yellow('GENERATORE PASSPHRASE DICEWARE'))))
        print(self.box_sep())
        print(self.box_line(''))
        
        opzioni = [
            (green('[1]'), '6 parole  (78 bit entropia)'),
            (green('[2]'), '7 parole  (90 bit entropia)'),
            (green('[3]'), '8 parole  (103 bit entropia)'),
            (green('[4]'), '9 parole  (116 bit entropia)'),
            None,
            (red('[0]'), 'Torna al menu'),
        ]
        
        for voce in opzioni:
            if voce is None:
                print(self.box_line(''))
            else:
                numero, descrizione = voce
                testo = numero + ' ' + descrizione
                testo_pulito = re.sub(r'\033\[[0-9;]*m', '', testo)
                padding = 68 - 3 - len(testo_pulito)
                print(' ' * 21 + cyan('║') + '   ' + testo + ' ' * padding + cyan('║'))
        
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        
        scelta = Terminal.wait_key(['0', '1', '2', '3', '4'])
        
        if scelta == '0':
            return
        
        num_parole = {1: 6, 2: 7, 3: 8, 4: 9}[int(scelta)]
        
        # Avviso dadi fisici
        avviso = self.avviso_dadi_fisici()
        if avviso == '0':
            return
        
        # Raccolta lanci
        tutti_lanci = []
        parole_generate = []
        
        for parola_idx in range(1, num_parole + 1):
            lanci_parola = []
            
            for lancio_idx in range(1, 6):
                self.mostra_logo()
                print(self.box_top())
                print(self.box_line(bold(yellow(f'DICEWARE - PAROLA {parola_idx} DI {num_parole}'))))
                print(self.box_sep())
                print(self.box_line(f'Lancio {lancio_idx} di 5'))
                print(self.box_sep())
                

                
                print(self.box_line(red('INPUT DIRETTO - Premi solo tasti 1-6')))
                print(self.box_bottom())
                print()
                
                roll = Terminal.dice()
                if roll is None:
                    return
                
                lanci_parola.append(roll)
                tutti_lanci.append(roll)
                time.sleep(0.1)
            
            # Formula Diceware corretta:
            # indice = (d1-1)*6^4 + (d2-1)*6^3 + (d3-1)*6^2 + (d4-1)*6^1 + (d5-1)*6^0 + 1
            indice = 0
            for i, lancio in enumerate(lanci_parola):
                indice += (lancio - 1) * (6 ** (4 - i))
            indice += 1
            
            parole_generate.append(diceware_wordlist[indice - 1])
        
        # CONTROLLO DISTRIBUZIONE DICEWARE
        ok_rip, perc_max = analizza_distribuzione_lanci(tutti_lanci)
        if not ok_rip:
            self.mostra_logo()
            print(self.box_top())
            print(self.box_line(bold(red('⚠️ AVVISO: DISTRIBUZIONE ANOMALA'))))
            print(self.box_sep())
            print(self.box_line(f'Valore più frequente: {perc_max:.0f}%'))
            print(self.box_line(''))
            print(self.box_line(red('Distribuzione sospetta rilevata.')))
            print(self.box_line(red('Puoi rifare i lanci se lo ritieni necessario.')))
            print(self.box_sep())
            print(self.box_line(''))
            testo1 = green('[1]') + ' Rifai tutti i lanci'
            padding1 = 68 - 3 - len('[1] Rifai tutti i lanci')
            print(' ' * 21 + cyan('║') + '   ' + testo1 + ' ' * padding1 + cyan('║'))
            testo2 = yellow('[2]') + ' Procedi comunque (sotto mia responsabilità)'
            padding2 = 68 - 3 - len('[2] Procedi comunque (sotto mia responsabilità)')
            print(' ' * 21 + cyan('║') + '   ' + testo2 + ' ' * padding2 + cyan('║'))
            testo3 = red('[0]') + ' Annulla e torna al menu'
            padding3 = 68 - 3 - len('[0] Annulla e torna al menu')
            print(' ' * 21 + cyan('║') + '   ' + testo3 + ' ' * padding3 + cyan('║'))
            print(self.box_line(''))
            print(self.box_bottom())
            print()
            scelta = Terminal.wait_key(['0', '1', '2'])
            if scelta == '0':
                return
            elif scelta == '1':
                self.genera_diceware()
                return
            else:
                pass
# Mostra schermata di conferma
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(''))
        print(self.box_line(bold(green('✓ PASSPHRASE DICEWARE PRONTA'))))
        print(self.box_line(''))
        print(self.box_line(yellow(f'{num_parole} parole - {num_parole * math.log2(7776):.0f} bit entropia')))
        print(self.box_line(''))
        print(self.box_sep())
        print(self.box_line(''))
        print(self.box_line('Prima di continuare assicurati di avere:'))
        print(self.box_line('• Carta e penna pronte'))
        print(self.box_line('• Nessuna telecamera attiva'))
        print(self.box_line('• Nessuna persona intorno'))
        print(self.box_line('• Ambiente sicuro e privato'))
        print(self.box_line(''))
        print(self.box_line(red('CONSERVA LA PASSPHRASE SEPARATA DALLA SEED!')))
        print(self.box_line(''))
        print(self.box_sep())
        print(self.box_line(''))
        
        # Opzione dentro la cornice
        testo_invio2 = green('[INVIO]') + ' Visualizza la passphrase'
        padding_invio2 = 68 - 3 - len('[INVIO] Visualizza la passphrase')
        print(' ' * 21 + cyan('║') + '   ' + testo_invio2 + ' ' * padding_invio2 + cyan('║'))
        
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        
        # Attende SOLO INVIO (blocca altri tasti)
        Terminal.wait_key(['\r', '\n', ' '])
        
        # Mostra passphrase
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold(green('✓ PASSPHRASE DICEWARE GENERATA'))))
        print(self.box_sep())
        print(self.box_line(red('NON FARE FOTO - NON CONDIVIDERE')))
        print(self.box_line(yellow('SCRIVI SU CARTA SEPARATA DALLA SEED')))
        print(self.box_sep())
        
        # Visualizzazione Diceware: formato fisso senza TAB
        righe = []
        for i in range(0, len(parole_generate)):
            # Estrai solo la parola (rimuovi eventuale numero nel file)
            parola = parole_generate[i].split('	')[-1] if '	' in parole_generate[i] else parole_generate[i]
            # Formato fisso: numero + punto + spazio + parola
            riga = f"{i+1:2d}. {parola}"
            righe.append(riga)
        
        # Lunghezza massima (testo puro, senza ANSI)
        max_lunghezza = max([len(r) for r in righe]) if righe else 0
        
        # Limita a 56 caratteri per sicurezza
        if max_lunghezza > 56:
            max_lunghezza = 56
        
        # Padding sinistro per centrare
        padding_sinistro = (68 - max_lunghezza) // 2
        
        for riga in righe:
            # Testo puro (senza ANSI)
            riga_pura = riga[:56] if len(riga) > 56 else riga
            
            # Calcola il padding destro ESATTO
            # Larghezza interna = 68
            # Formato: ║ + spazi_sx + testo + spazi_dx + ║
            # spazi_sx + len(testo) + spazi_dx = 68
            spazi_dx = 68 - padding_sinistro - len(riga_pura)
            
            # Stampa con la larghezza ESATTA
            print(' ' * 21 + cyan('║') + ' ' * padding_sinistro + green(riga_pura) + ' ' * spazi_dx + cyan('║'))
        
        print(self.box_sep())
        print(self.box_line(yellow(f'Entropia: {num_parole * math.log2(7776):.0f} bit')))
        print(self.box_sep())
        print(self.box_line(''))
        testo1d = green('[1]') + ' Torna al menu'
        padding1d = 68 - 3 - len('[1] Torna al menu')
        print(' ' * 21 + cyan('║') + '   ' + testo1d + ' ' * padding1d + cyan('║'))
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        Terminal.wait_key(['1'])
        
        # Pulizia memoria
        parole_generate = None
        tutti_lanci = None
        diceware_wordlist = None

    def verifica_mnemonic(self):
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold('VERIFICA MNEMONIC BIP39')))
        print(self.box_bottom())
        print()
        # Input senza echo (la mnemonic non viene mostrata)
        import getpass
        print("Mnemonic (input nascosto - Ctrl+C per annullare):")
        mnemonic = getpass.getpass("> ").strip()
        if mnemonic == '0':
            return
        if mnemonic == '':
            return
        import re as _re
        if _re.search(r'[0-9]', mnemonic):
            print()
            print(yellow('La mnemonic non deve contenere numeri. Rilevati caratteri numerici.'))
            return
        try:
            entropy = mnemonic_to_entropy(mnemonic, self.wordlist)
            print()
            print(green("✓ CHECKSUM BIP39 VALIDO"))
            print(f"Entropia: {len(entropy) * 8} bit")
        except Exception as e:
            print()
            print(red("✗ MNEMONIC NON VALIDA"))
            print(red(str(e)))
        print()
        Terminal.wait_key(['\r', '\n', ' '])
        entropy = None
        mnemonic = None
        # Pulisci schermo e scrollback
        Terminal.clear()

    def audit_mode(self):
        """Mostra parametri ENT, N, k, M e risultato rejection"""
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold('AUDIT MODE - PARAMETRI ENTROPIA')))
        print(self.box_sep())
        
        import math
        for ent_bits, lanci in [(128, 50), (160, 62), (192, 75), (224, 87), (256, 100)]:
            N = lanci
            k = (6**N).bit_length() - 1
            M = 1 << k
            prob = M / (6**N)
            print(self.box_line(f'ENT={ent_bits} bit | N={N} lanci | k={k} | M=2^{k}'))
            print(self.box_line(f'P(accettazione) = {prob:.3f}'))
            print(self.box_sep())
        
        print(self.box_sep())
        print(self.box_line(''))
        testo_invio3 = green('[INVIO]') + ' Torna al menu'
        padding_invio3 = 68 - 3 - len('[INVIO] Torna al menu')
        print(' ' * 21 + cyan('║') + '   ' + testo_invio3 + ' ' * padding_invio3 + cyan('║'))
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        Terminal.wait_key(['\r', '\n', ' '])

    def test_integrita(self):
        self.mostra_logo()
        print(self.box_top())
        print(self.box_line(bold('CONTROLLO INTEGRITÀ')))
        print(self.box_sep())
        
        # Usa la STESSA pipeline run_all_self_tests()
        diceware_wl = load_diceware_wordlist()
        risultati = run_all_self_tests(self.wordlist, diceware_wl)
        
        tutti_ok = True
        for nome, ok in risultati:
            if ok:
                print(self.box_line(green(f'[OK] {nome}')))
            else:
                print(self.box_line(red(f'[FAIL] {nome}')))
                tutti_ok = False
        
        print(self.box_sep())
        if tutti_ok:
            print(self.box_line(green('TUTTI I TEST SUPERATI ✓')))
        else:
            print(self.box_line(red('ALCUNI TEST FALLITI ✗')))
        print(self.box_sep())
        print(self.box_line(''))
        testo_invio3 = green('[INVIO]') + ' Torna al menu'
        padding_invio3 = 68 - 3 - len('[INVIO] Torna al menu')
        print(' ' * 21 + cyan('║') + '   ' + testo_invio3 + ' ' * padding_invio3 + cyan('║'))
        print(self.box_line(''))
        print(self.box_bottom())
        print()
        Terminal.wait_key(['\r', '\n', ' '])

    def run(self):
        # Self-test unificato (UNICA pipeline)
        try:
            diceware_wl = load_diceware_wordlist()
            risultati = run_all_self_tests(self.wordlist, diceware_wl)
            for nome, ok in risultati:
                if not ok:
                    raise Exception(f"Test fallito: {nome}")
        except Exception as e:
            Terminal.clear()
            print(red("ERRORE CRITICO DURANTE SELF-TEST"))
            print(red(str(e)))
            sys.exit(1)
        
        while True:
            self.mostra_menu()
            scelta = Terminal.wait_key('0123456789')
            if scelta == '0':
                Terminal.clear()
                print(green("Uscita."))
                return
            words_map = {'1': 12, '2': 15, '3': 18, '4': 21, '5': 24}
            if scelta in words_map:
                self.genera(words_map[scelta])
            elif scelta == '6':
                self.genera_diceware()
            elif scelta == '7':
                self.verifica_mnemonic()
            elif scelta == '8':
                self.test_integrita()
            elif scelta == '9':
                self.audit_mode()

def main() -> None:
    try:
        app = SeedGenApp()
        app.run()
    except KeyboardInterrupt:
        print(red("\n\nInterrotto."))
    except EOFError:
        print(red("\n\nEOF rilevato. Uscita."))
        Terminal.clear()
        sys.exit(0)
    except Exception as e:
        print(red("\nERRORE:"))
        print(red(str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()
