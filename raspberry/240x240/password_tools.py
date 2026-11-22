"""Experimental dice-only passwords. No RNG, hashing or seed derivation.

An accepted complete base-6 block is reduced into a whole fixed-length output
space. Rejecting the incomplete tail avoids modulo bias, assuming fair,
independent physical rolls. Nominal strength describes independent choices;
separator-free variable-length words are explicitly not offered as strong.
"""
import hashlib
from pathlib import Path
import string

SHORT_HASH='8f5ca830b8bffb6fe39c9736c024a00a6a6411adb3f83a9be8bfeeb6e067ae69'
BASE85='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
SETS=(string.ascii_lowercase,string.ascii_uppercase,string.digits,'!#$%&()*+-./:;<=>?@[]^_{|}~')
FORMATS=('Custom','Diceware classico','Diceware BIP39')
STRENGTHS=(64,128,256)

def load_short(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SHORT_HASH:
        raise ValueError('EFF short wordlist mismatch')
    pairs=[line.split() for line in raw.decode('ascii').splitlines()]
    if len(pairs)!=1296 or any(len(p)!=2 for p in pairs):
        raise ValueError('EFF short structure')
    words=[]
    for index,(label,word) in enumerate(pairs):
        x=index; digits=[]
        for _ in range(4): digits.append(str(x%6+1)); x//=6
        if label!=''.join(reversed(digits)) or not word.replace('-','').isalpha() or not word.islower():
            raise ValueError('EFF short order')
        words.append(word)
    if len(set(words))!=1296: raise ValueError('Duplicate words')
    return words

def choice_count(base,bits):
    if type(base) is not int or base<2 or bits not in STRENGTHS:
        raise ValueError('Invalid strength/alphabet')
    count=1
    while base**count<1<<bits: count+=1
    return count

def roll_plan(base,count):
    if type(base) is not int or type(count) is not int or base<2 or not 1<=count<=256:
        raise ValueError('Invalid output space')
    space=base**count; n=1
    while 6**n<space: n+=1
    return n,space,(6**n//space)*space

def decode_block(rolls,base,count):
    n,space,limit=roll_plan(base,count)
    if len(rolls)!=n or any(type(v) is not int or not 1<=v<=6 for v in rolls):
        raise ValueError('Invalid physical dice block')
    x=0
    for roll in rolls: x=x*6+roll-1
    if x>=limit: return None
    x%=space; result=[0]*count
    for i in range(count-1,-1,-1): result[i]=x%base; x//=base
    return result

def format_words(words,separator):
    if separator=='Capitalise': return ''.join(w.capitalize() for w in words)
    if separator=='Space': return ' '.join(words)
    if separator=='.': return '.'.join(words)
    # Variable-length concatenations can collide and reduce nominal strength.
    # Do not silently promise the selected bit strength for that format.
    raise ValueError('Choose an unambiguous word separator')

def self_test(short):
    if len(short)!=1296 or len(set(BASE85))!=85: raise ValueError('Password dictionaries')
    # Exhaustive small space: all 36 roll pairs, 25 outputs, 11 rejections.
    seen=[0]*25; rejected=0
    for x in range(36):
        result=decode_block([x//6+1,x%6+1],5,2)
        if result is None: rejected+=1
        else: seen[result[0]*5+result[1]]+=1
    if seen!=[1]*25 or rejected!=11: raise ValueError('Unbiased mapping test')
    for base in (26,85,1296,2048,7776):
        for bits in STRENGTHS:
            count=choice_count(base,bits); n,space,limit=roll_plan(base,count)
            if space<1<<bits or not space<=limit<=6**n or limit%space:
                raise ValueError('Strength test')
    return True
