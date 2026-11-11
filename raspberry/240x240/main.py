#!/usr/bin/env python3
# SEEDGEN_PI_V9_MARKER
"""Experimental LCD front end. Core and wordlists are unchanged upstream v1.0.2.
Secrets are not intentionally saved or printed. Python cannot securely erase RAM.
"""
import gc
import hashlib
import hmac
import os
from pathlib import Path
import subprocess
import sys
import time
import password_tools as passwords
import ui_views as views
import i18n
from i18n import tr
CANVAS_WIDTH=240
from PIL import Image, ImageDraw, ImageFont
sys.dont_write_bytecode=True
UPSTREAM=Path(__file__).resolve().parent / 'seedgen_upstream'
if not UPSTREAM.is_dir():
    UPSTREAM=Path(__file__).resolve().parent / 'vendor'
sys.path.insert(0, str(UPSTREAM))
import seedgen as core
CORE_SHA256='a347d11ec5d23dac0799c5d19ef5495d74b744e479eb67e706c0a7ad62c2564b'
LENGTHS=(12,15,18,21,24)
MAIN_MENU=tuple('BIP39: %d parole' % n for n in LENGTHS)+(
    'Diceware', 'Verifica BIP39', 'Test integrita',
    'Audit Mode', 'Test pulsanti', 'Spegni Raspberry')


def diceware_words(rolls, dictionary):
    if not rolls or len(rolls)%5 or any(type(v) is not int or not 1<=v<=6 for v in rolls):
        raise ValueError('Invalid dice block')
    result=[]
    for offset in range(0,len(rolls),5):
        index=0
        for value in rolls[offset:offset+5]: index=index*6+value-1
        result.append(dictionary[index])
    return result


def audit_parameters(count):
    bits=core.ENTROPY_BITS[count]
    n=core.dice_rolls_needed(bits)
    k=(6**n).bit_length()-1
    return bits,n,k,(1<<k)/(6**n)

PINS={"UP":31,"DOWN":35,"LEFT":29,"RIGHT":37,"PRESS":33,"KEY1":40,"KEY2":38,"KEY3":36}

def wrap_lines(lines, font, width=224):
    result=[]
    for line in lines:
        line=str(line)
        if not line:
            result.append(''); continue
        current=''
        for word in line.split():
            candidate=(current+' '+word).strip()
            if font.getlength(candidate)<=width:
                current=candidate
            else:
                if current: result.append(current)
                current=''
                for char in word:
                    if current and font.getlength(current+char)>width:
                        result.append(current); current=''
                    current+=char
        if current: result.append(current)
    return result


def body_font():
    return ImageFont.truetype(str(Path(__file__).resolve().parent / 'fonts' / 'DejaVuSans.ttf'),20)


def splash_image(shutdown=False):
    # Code-drawn brand mark based on the supplied Bitvero reference.
    # Supersampling keeps the small shield and lettering legible on the LCD.
    scale=3
    canvas_width=240
    image=Image.new('RGB',(canvas_width*scale,240*scale),'black')
    draw=ImageDraw.Draw(image)
    fonts=Path(__file__).resolve().parent / 'fonts'
    orange=(255,155,30)
    if not shutdown:
        size=44
        while True:
            font=ImageFont.truetype(str(fonts/'DejaVuSans-Bold.ttf'),size*scale)
            box=draw.textbbox((0,0),'SEEDGEN',font=font)
            if box[2]-box[0]<=(canvas_width-24)*scale: break
            size-=1
        width,height=box[2]-box[0],box[3]-box[1]
        draw.text(((canvas_width*scale-width)//2-box[0],96*scale-height//2-box[1]),
                  'SEEDGEN',font=font,fill=orange)
        draw.line((28*scale,59*scale,(canvas_width-28)*scale,59*scale),fill=orange,width=2*scale)
        draw.line((28*scale,133*scale,(canvas_width-28)*scale,133*scale),fill=orange,width=2*scale)
    byfont=ImageFont.truetype(str(fonts/'DejaVuSans.ttf'),17*scale)
    brandfont=ImageFont.truetype(str(fonts/'DejaVuSans-Bold.ttf'),22*scale)
    by_width=0 if shutdown else draw.textlength('by',font=byfont)+7*scale
    brand_width=draw.textlength('Bitvero',font=brandfont)
    shield_w,shield_h=27*scale,31*scale
    gap=7*scale
    total=by_width+shield_w+gap+brand_width
    left=(canvas_width*scale-total)/2
    cy=(120 if shutdown else 174)*scale
    def text_center_y(x,text,font):
        box=draw.textbbox((0,0),text,font=font)
        draw.text((x-box[0],cy-(box[3]-box[1])/2-box[1]),text,font=font,fill='white')
    if not shutdown:
        text_center_y(left,'by',byfont)
    x=left+by_width; y=cy-shield_h/2
    points=[(.5,0),(1,.12),(.99,.37),(.96,.54),(.89,.70),(.79,.82),(.64,.93),(.5,1),(.36,.93),(.21,.82),(.11,.70),(.04,.54),(.01,.37),(0,.12)]
    draw.polygon([(x+px*shield_w,y+py*shield_h) for px,py in points],fill=(247,124,24))
    # Upright B and two short vertical stems, as on the supplied shield.
    bfont=ImageFont.truetype(str(fonts/'DejaVuSans-Bold.ttf'),24*scale)
    box=draw.textbbox((0,0),'B',font=bfont)
    bx=x+(shield_w-(box[2]-box[0]))/2-box[0]
    by=y+shield_h*.47-(box[3]-box[1])/2-box[1]
    draw.text((bx,by),'B',font=bfont,fill='white')
    for stem in (.40,.56):
        sx=x+shield_w*stem
        draw.rectangle((sx,y+shield_h*.14,sx+1.4*scale,y+shield_h*.82),fill='white')
    text_center_y(x+shield_w+gap,'Bitvero',brandfont)
    return image.resize((canvas_width,240),Image.Resampling.LANCZOS)


class UI:
    def __init__(self):
        import RPi.GPIO as GPIO
        from seedsigner.hardware.displays.display_driver import DisplayDriverFactory, DISPLAY_TYPE__ST7789
        self.GPIO = GPIO
        GPIO.setwarnings(False); GPIO.setmode(GPIO.BOARD)
        for p in PINS.values(): GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.disp=DisplayDriverFactory.instantiate_display_driver(DISPLAY_TYPE__ST7789,width=240,height=240)
        font_path=Path(__file__).resolve().parent / 'fonts' / 'DejaVuSans.ttf'
        self.font=ImageFont.truetype(str(font_path), 20)
        self.footer_font=ImageFont.truetype(str(font_path), 16)

    def splash(self):
        self.disp.show_image(splash_image(),0,0)
        time.sleep(3)

    def render(self,title,lines=(),footer=""):
        views.render(self,CANVAS_WIDTH,title,list(lines),footer)

    def dice(self,value,done,total,rolls):
        views.dice(self,CANVAS_WIDTH,value,done,total,rolls)

    def home(self,index):
        views.home(self,CANVAS_WIDTH,index)

    def power_menu(self,index):
        views.power_menu(self,CANVAS_WIDTH,index)

    def shutdown_logo(self):
        self.disp.show_image(splash_image(shutdown=True),0,0)

    def fit(self, text):
        text=str(text)
        if self.font.getlength(text)<=224: return text
        while text and self.font.getlength(text+'...')>224: text=text[:-1]
        return text+'...'

    def key(self):
        names={'PRESS':'OK','KEY1':'K1','KEY2':'K2','KEY3':'BACK'}
        return names.get((k:=self.wait_key()), k)

    def wait_key(self):
        GPIO=self.GPIO
        while True:
            for name,pin in PINS.items():
                if GPIO.input(pin)==GPIO.LOW:
                    time.sleep(.04)
                    while GPIO.input(pin)==GPIO.LOW: time.sleep(.01)
                    return name
            time.sleep(.01)


class Cancel(Exception):
    pass


def check_core():
    if hashlib.sha256((UPSTREAM / 'seedgen.py').read_bytes()).hexdigest() != CORE_SHA256:
        raise RuntimeError('Sorgente SeedGen non corrispondente')
    wl, dw = core.load_wordlist(), core.load_diceware_wordlist()
    results = core.run_all_self_tests(wl, dw)
    # Fail closed, including tests skipped for filesystem permissions.
    if any(status != 'PASS' for _, status in results):
        raise RuntimeError('Self-test incompleti o falliti')
    short=passwords.load_short(UPSTREAM/'eff_short_wordlist_1.txt')
    passwords.self_test(short)
    return wl, dw, results


def require_offline():
    # Passive check: unlike upstream CLI, do not contact Internet endpoints.
    # Reject any non-loopback interface administratively UP, including USB.
    if len(Path('/proc/swaps').read_text().splitlines()) > 1:
        raise RuntimeError('Swap attiva: disabilitala')
    for interface in Path('/sys/class/net').iterdir():
        if interface.name != 'lo' and int((interface / 'flags').read_text().strip(), 16) & 1:
            raise RuntimeError('Scollega/disattiva rete')

class App:
    def __init__(self, ui):
        self.ui = ui
        self.wl = self.dw = self.tests = None

    def screen(self,title,lines,footer='Centro: OK / K3: indietro',selected=None,translate_lines=True):
        labels=[tr(line) if translate_lines else str(line) for line in lines]
        self.ui.render(tr(title),[('> ' if i==selected else '')+line for i,line in enumerate(labels)],tr(footer))

    def menu(self,title,options,translate_options=True):
        index=0
        try:
            while True:
                self.ui.back_focused=index==-1
                self.ui.menu_active=True
                start=(max(0,index)//5)*5
                footer='Freccia: Centro per uscire' if index==-1 else '%d/%d Su/giu: scegli Centro: OK / K3: esci'%(index+1,len(options))
                self.screen(title,options[start:start+5],footer,selected=index-start if index>=0 else None,translate_lines=translate_options)
                self.ui.menu_active=False
                key=self.ui.key()
                if key=='UP':index=max(-1,index-1)
                elif key=='LEFT':index=-1
                elif key in ('DOWN','RIGHT'):
                    index=0 if index==-1 else (index+1)%len(options)
                elif key in ('OK','K2'):
                    if index==-1:raise Cancel()
                    return index
                elif key=='BACK':raise Cancel()
        finally:
            self.ui.back_focused=False;self.ui.menu_active=False

    def note(self,title,lines):
        wrapped=wrap_lines([tr(line) for line in lines],body_font())
        pages=max(1,(len(wrapped)+4)//5);page=0;back=False
        try:
            while True:
                self.ui.back_focused=back
                heading=title if pages==1 else '%s %d/%d'%(title,page+1,pages)
                self.screen(heading,wrapped[page*5:page*5+5],
                            'Freccia: Centro per uscire' if back else 'Centro: avanti / K3: esci',translate_lines=False)
                key=self.ui.key()
                if back:
                    if key in ('OK','K2','BACK'):raise Cancel()
                    if key in ('DOWN','RIGHT'):back=False
                    continue
                if key in ('OK','K2','RIGHT','DOWN'):
                    if page==pages-1:return
                    page+=1
                elif key=='UP':back=True
                elif key=='LEFT':
                    if page:page-=1
                    else:back=True
                elif key=='BACK':raise Cancel()
        finally:self.ui.back_focused=False

    def collect(self, n):
        rolls = []
        value = 1
        back=False
        while True:
            self.ui.back_focused=back
            if hasattr(self.ui,'dice'):
                self.ui.dice(value,len(rolls),n,rolls)
            else:
                self.screen('Lancio %d/%d' % (len(rolls)+1,n),['Risultato: %d'%value])
            key = self.ui.key()
            if back:
                if key in ('OK','K2','BACK'):
                    self.ui.back_focused=False;raise Cancel()
                if key in ('DOWN','RIGHT'):
                    back=False;self.ui.back_focused=False
                continue
            if key=='UP' and value<=3:
                back=True;continue
            if key=='RIGHT': value=((value-1)//3)*3+value%3+1
            elif key=='LEFT': value=((value-1)//3)*3+(value-2)%3+1
            elif key in ('UP','DOWN'): value=(value+2)%6+1
            elif key == 'K1' and rolls: rolls.pop()
            elif key == 'BACK':
                self.ui.back_focused=False;raise Cancel()
            elif key in ('OK', 'K2'):
                rolls.append(value)
                if len(rolls) == n:
                    if self.menu('Conferma blocco', ['Usa questi %d lanci' % n, 'Correggi ultimo lancio']) == 0:
                        return rolls
                    rolls.pop()
                value = 1

    def choose_word(self, words, number):
        # Prefix selection without ever displaying the expected word.
        prefix = ''
        while True:
            matches = [w for w in words if w.startswith(prefix)]
            if len(matches) <= 7:
                return matches[self.menu('Parola %d' % number,matches,translate_options=False)]
            letters = sorted(set(w[len(prefix):len(prefix)+1] for w in matches))
            labels = [('Fine parola' if not c else prefix+c+'...') for c in letters]
            if prefix:
                labels.append('Cancella lettera')
            choice = self.menu('Parola %d: %s' % (number, prefix), labels)
            if choice == len(letters): prefix = prefix[:-1]
            elif not letters[choice]: return prefix
            else: prefix += letters[choice]

    def display_words(self,words,title):
        page=0;pages=(len(words)+4)//5;back=False
        try:
            while True:
                self.ui.back_focused=back
                items=['%02d  %s'%(i+1,words[i]) for i in range(page*5,min(len(words),page*5+5))]
                self.screen('%s %d/%d'%(title,page+1,pages),items,
                            'Freccia: Centro per uscire' if back else 'Sin/des: pagina K2: avanti / K3: esci',translate_lines=False)
                key=self.ui.key()
                if back:
                    if key in ('OK','K2','BACK'):raise Cancel()
                    if key in ('RIGHT','DOWN'):back=False
                    continue
                if key in ('RIGHT','DOWN'):page=min(pages-1,page+1)
                elif key=='UP':back=True
                elif key=='LEFT':
                    if page:page-=1
                    else:back=True
                elif key=='BACK':raise Cancel()
                elif key in ('OK','K2'):
                    if page==pages-1:return
                    page+=1
        finally:self.ui.back_focused=False

    def verify_copy(self, words, dictionary, *, bip39=False):
        while True:
            self.note('Verifica copia', ['Usa solo il foglio.', 'Inserisci TUTTE le parole', 'nello stesso ordine.', 'K3 annulla: non verificata.'])
            entered = [self.choose_word(dictionary, i+1) for i in range(len(words))]
            good = hmac.compare_digest(' '.join(entered).encode('utf-8'), ' '.join(words).encode('utf-8'))
            if good and bip39:
                try:
                    core.mnemonic_to_entropy(entered, dictionary)
                except Exception:
                    entered = None
                    choice = self.menu('Copia non verificata', ['Riprova dal foglio', 'Annulla (non verificata)'])
                    if choice == 1:
                        raise Cancel()
                    continue
            entered = None
            if good:
                self.note('Copia verificata', ['Parole e ordine corretti.', 'Conserva il foglio al sicuro.'])
                return
            choice = self.menu('Copia non coincide', ['Riprova dal foglio', 'Rivedi le parole', 'Annulla (non verificata)'])
            if choice == 1: self.display_words(words, 'Trascrivi su carta')
            elif choice == 2: raise Cancel()

    def generate(self, count, diceware=False):
        require_offline()
        self.note('Prima di iniziare', ['VERSIONE SPERIMENTALE', 'Solo prove, niente fondi.', 'Usa dadi fisici affidabili.', 'Niente foto o telecamere.', 'Prepara carta e penna.', 'K3: annulla senza salvare.'])
        words = rolls = entropy = None
        try:
            while True:
                n = count*5 if diceware else core.dice_rolls_needed(core.ENTROPY_BITS[count])
                rolls = self.collect(n)
                require_offline()
                valid, _ = core.analizza_distribuzione_lanci(rolls)
                if not valid:
                    rolls = None
                    self.note('Distribuzione anomala', ['Tutto il blocco scartato.', 'Rifai TUTTI i lanci.', 'Questo test non garantisce', "la casualita dei dadi."])
                    continue
                if diceware:
                    words = diceware_words(rolls, self.dw)
                else:
                    entropy, _, accepted = core.extract_entropy_from_dice_block(rolls, core.ENTROPY_BITS[count])
                    if not accepted:
                        rolls = None
                        self.note('Blocco rifiutato', ['Rejection sampling:', 'tutto il blocco scartato.', 'Rifai TUTTI i lanci.'])
                        continue
                    words = core.entropy_to_mnemonic(entropy, self.wl)
                    if core.mnemonic_to_entropy(words, self.wl) != entropy:
                        raise RuntimeError('Verifica BIP39 fallita')
                break
            if diceware:
                self.note('Passphrase Diceware', ['Trascrivi in minuscolo.', 'Un solo spazio tra parole.', 'Numeri esclusi.', 'Conserva separata', 'dalla seed BIP39.'])
            self.display_words(words, 'Diceware' if diceware else 'Seed BIP39')
            self.verify_copy(words, self.dw if diceware else self.wl, bip39=not diceware)
        finally:
            self.screen('Sessione chiusa', ['Nessun segreto salvato.', 'RAM Python non azzerabile.', 'Spegni dopo la prova.'])
            words = rolls = entropy = None
            gc.collect()

    def diagnostics(self):
        last='Nessuno';back=False
        try:
            while True:
                self.ui.back_focused=back
                self.screen('Test pulsanti',['Prova joystick','e tutti i pulsanti.','Ultimo: '+tr(last)],
                            'Freccia: Centro per uscire' if back else 'Su: indietro / Centro: apri')
                key=self.ui.key()
                if key=='BACK' or back and key in ('OK','K2'):return
                last=key
                if key=='UP':back=True
                elif key=='DOWN':back=False
        finally:self.ui.back_focused=False

    def verify_mnemonic(self):
        require_offline()
        words=entropy=None
        try:
            self.note('Verifica BIP39', ['Usa solo seed di prova.', 'Controlla parole e checksum.', 'Non prova che una seed sia', 'casuale o sicura.'])
            count=LENGTHS[self.menu('Numero parole', [str(n)+' parole' for n in LENGTHS])]
            words=[self.choose_word(self.wl,i+1) for i in range(count)]
            require_offline()
            try:
                entropy=core.mnemonic_to_entropy(words,self.wl)
            except ValueError:
                self.note('Mnemonic non valida', ['Checksum BIP39 errato.', 'Ricontrolla il foglio.'])
                return
            self.note('Checksum BIP39 valido', [str(count)+' parole riconosciute.', str(len(entropy)*8)+' bit di entropia.'])
        finally:
            words=entropy=None
            self.screen('Verifica chiusa', ['Nessun segreto salvato.'])
            gc.collect()

    def audit(self):
        for count in LENGTHS:
            bits,n,k,prob=audit_parameters(count)
            self.note('Audit: %d parole' % count, ['ENT = %d bit' % bits, 'N = %d lanci' % n, 'k = %d bit' % k, 'M = 2^%d' % k, 'P(accetta) = %.3f' % prob, 'Blocco >= M: scartato.', 'Parametri, nessuna seed.'])

    def integrity(self):
        self.screen('Test integrita', ['Controlli in corso...', 'Attendi il risultato.'])
        self.ready=False
        self.wl,self.dw,self.tests=check_core()
        self.ready=True
        for title,status in self.tests:
            # Names are public diagnostic text; split for the small screen.
            self.note('Test: '+status, [title])
        self.note('Test superati', ['%d controlli PASS' % len(self.tests), 'Non e un audit di sicurezza.'])

    def shutdown(self):
        if self.menu('Spegnimento', ['Annulla', 'Spegni ora']) == 1:
            self.ui.shutdown_logo()
            subprocess.run(['/sbin/poweroff'], check=True)
            while True:
                time.sleep(60)

    def power_menu(self):
        index=0
        while True:
            self.ui.power_menu(index)
            key=self.ui.key()
            if key=='BACK':
                return
            if key=='UP':
                index=-1
            elif key=='DOWN' and index==-1:
                index=0
            elif key in ('LEFT','RIGHT'):
                index=0 if index==-1 else 1-index
            elif key in ('OK','K2'):
                if index==-1:
                    return
                if index==1:
                    self.shutdown()
                elif self.menu('Riavvio', ['Annulla', 'Riavvia ora']) == 1:
                    subprocess.run(['/sbin/reboot'], check=True)
                    while True:
                        time.sleep(60)
                return

    def home(self):
        index=getattr(self,'home_index',0)
        self.ui.back_focused=False
        while True:
            self.ui.home(index)
            key=self.ui.key()
            if index==4:
                if key in ('OK','K2'):
                    try:self.power_menu()
                    except Cancel:pass
                elif key in ('DOWN','LEFT','BACK'):index=0
                elif key=='RIGHT':index=1
            elif key=='UP':index=4 if index<2 else index-2
            elif key=='DOWN':index=(index+2)%4
            elif key in ('LEFT','RIGHT'):index=(index//2)*2+(index+1)%2
            elif key in ('OK','K2'):
                self.home_index=index;return index
            elif key=='BACK':
                try:self.power_menu()
                except Cancel:pass

    def text_result(self,text,mark_spaces=False):
        # Fixed-width chunks preserve every character and separator, unlike
        # word-wrapping, which would strip or collapse spaces.
        display=text.replace(' ','*') if mark_spaces else text
        chunks=[];line='';font=body_font()
        for char in display:
            if line and font.getlength(line+char)>CANVAS_WIDTH-18:
                chunks.append(line);line=''
            line+=char
        if line:chunks.append(line)
        page=0;pages=(len(chunks)+3)//4;back=False
        while True:
            self.ui.back_focused=back
            self.screen('Password %d/%d'%(page+1,pages),chunks[page*4:page*4+4],
                        'Freccia: Centro per uscire' if back else ('*=spazio / Centro: avanti K3: esci' if mark_spaces else 'Sin/des: pagina Centro: avanti / K3: esci'),translate_lines=False)
            key=self.ui.key()
            if back:
                if key in ('OK','K2','BACK'):
                    self.ui.back_focused=False;raise Cancel()
                if key in ('DOWN','RIGHT'):
                    back=False;self.ui.back_focused=False
                continue
            if key in ('RIGHT','DOWN','OK','K2'):
                if page==pages-1:return
                page+=1
            elif key=='UP':back=True
            elif key=='LEFT':
                if page:page-=1
                else:back=True
            elif key=='BACK':raise Cancel()

    def confirm_string(self,text,alphabet):
        while True:
            self.note('Verifica copia',['Riscrivi dal foglio.', 'Maiuscole e simboli contano.'])
            entered=''.join(self.choose_word(list(alphabet),i+1) for i in range(len(text)))
            good=hmac.compare_digest(entered.encode('ascii'),text.encode('ascii'))
            entered=None
            if good:
                self.note('Copia verificata',['Tutti i caratteri corretti.']);return
            choice=self.menu('Copia diversa',['Riprova','Rivedi password','Annulla'])
            if choice==1:self.text_result(text)
            elif choice==2:raise Cancel()

    def password_menu(self):
        while True:
            kind=self.menu('Tipo passphrase',passwords.FORMATS)
            try:return self.password_flow(kind)
            except Cancel:
                self.ui.back_focused=False
                continue

    def password_settings(self,kind):
        enabled=[True,True,True,False]
        labels=('Minuscole','Maiuscole','Numeri','Simboli')
        stages=['characters','strength','source'] if kind==0 else ['strength','separator','source']
        step=0;bits=64;separator=None
        while step<len(stages):
            try:
                stage=stages[step]
                if stage=='characters':
                    choice=self.menu('Caratteri Custom',[tr(labels[i])+(': SI' if enabled[i] else ': NO') for i in range(4)]+['Continua'])
                    if choice<4:
                        enabled[choice]=not enabled[choice];continue
                    if not any(enabled):
                        self.note('Scegli caratteri',['Attiva almeno un gruppo.']);continue
                elif stage=='strength':
                    bits=passwords.STRENGTHS[self.menu('Forza password',[str(n)+' bit' for n in passwords.STRENGTHS])]
                elif stage=='separator':
                    separator=('None','Capitalise','Space','.')[self.menu('Separatore',['None','Capitalise','Space','.'])]
                    if separator=='None':
                        self.note('Scegli separatore',['Senza separatore, parole diverse possono confondersi.','Per mantenere la forza scelta usa spazio, punto o maiuscole.']);continue
                elif stage=='source':self.menu('Fonte entropia',['Dadi fisici D6'])
                step+=1
            except Cancel:
                if step==0:raise
                step-=1
        alphabet=''.join(group for on,group in zip(enabled,passwords.SETS) if on) if kind==0 else None
        return alphabet,self.wl if kind==2 else None,bits,separator

    def password_flow(self,kind):
        # The parent menu catches cancellation and allows a fresh choice.
        if kind not in (0,1,2):raise ValueError('Invalid password type')
        if kind==1:
            count=(6,7,8,9)[self.menu('Diceware classico',[str(n)+' parole' for n in (6,7,8,9)])]
            return self.generate(count,True)
        alphabet=None;dictionary=None;separator=None;words=None;text=None;rolls=None;indices=None
        try:
            alphabet,dictionary,bits,separator=self.password_settings(kind)
            symbols=dictionary or alphabet
            count=passwords.choice_count(len(symbols),bits)
            n,_,_=passwords.roll_plan(len(symbols),count)
            self.note('Prima di iniziare',['Solo dati di prova.', str(bits)+' bit nominali con dadi equi e indipendenti.',
                      str(count)+(' parole' if dictionary else ' caratteri'),str(n)+' lanci per blocco.',
                      'I blocchi fuori intervallo vanno rifatti.'])
            require_offline()
            while True:
                rolls=self.collect(n);require_offline()
                valid,_=core.analizza_distribuzione_lanci(rolls)
                if not valid:
                    rolls=None
                    self.note('Distribuzione anomala',['Blocco scartato.', 'Rifai tutti i lanci.']);continue
                indices=passwords.decode_block(rolls,len(symbols),count)
                rolls=None
                if indices is not None:break
                self.note('Blocco rifiutato',['Rejection sampling.', 'Rifai tutti i lanci.'])
            if dictionary:
                words=[dictionary[i] for i in indices]
                text=passwords.format_words(words,separator)
                self.note('Formato da copiare',['Separatore: '+tr(separator),
                          'Parole in minuscolo.' if separator!='Capitalise' else 'Iniziale maiuscola di ogni parola.',
                          'E una password, non una seed BIP39.'])
                self.display_words(words,'Parole password')
                self.note('Copia formato',['Nel testo completo * indica un singolo spazio.', 'Non copiare gli asterischi.'] if separator=='Space' else ['Copia il testo esattamente.'])
                self.text_result(text,mark_spaces=separator=='Space')
                self.verify_copy(words,dictionary)
                self.note('Controlla formato',['Verifica anche separatori e maiuscole sul foglio.'])
            else:
                text=''.join(symbols[i] for i in indices)
                self.note('Copia esatta',['Le righe sono solo impaginazione.', 'Non aggiungere spazi o ritorni a capo.',
                          str(len(text))+' caratteri totali.'])
                self.text_result(text)
                self.confirm_string(text,alphabet)
        finally:
            words=text=rolls=indices=alphabet=dictionary=None
            self.screen('Sessione chiusa',['Nessun salvataggio.', 'Spegni dopo la prova.']);gc.collect()

    def language_menu(self):
        while True:
            choice=self.menu('Lingua',[label for _,label in i18n.LANGUAGES],translate_options=False)
            i18n.set_language(i18n.LANGUAGES[choice][0])
            try:self.note('Lingua applicata',['Valida per questa sessione.','Al riavvio torna italiano.'])
            except Cancel:pass
            return

    def tools_menu(self):
        while True:
            choice=self.menu('Strumenti',['Test integrita','Audit Mode','Test pulsanti','Lingua','Spegni Raspberry'])
            try:
                if choice==0:self.integrity()
                elif choice==1:self.audit()
                elif choice==2:self.diagnostics()
                elif choice==3:self.language_menu()
                elif choice==4:self.shutdown()
            except Cancel:self.ui.back_focused=False

    def run(self):
        self.ui.splash()
        self.ready=False
        self.wl,self.dw,self.tests=check_core()
        self.ready=True
        while True:
            try:
                choice=self.home()
                if choice<3 and not self.ready:raise RuntimeError('Esegui test integrita')
                if choice==0:
                    while True:
                        n=self.menu('Nuova seed BIP39',[str(n)+' parole' for n in LENGTHS])
                        try:
                            self.generate(LENGTHS[n]);break
                        except Cancel:self.ui.back_focused=False
                elif choice==1:self.password_menu()
                elif choice==2:self.verify_mnemonic()
                elif choice==3:self.tools_menu()
            except (Cancel, TimeoutError):
                self.screen('Sessione annullata', ['Nessun salvataggio.', 'Copia non confermata.']);gc.collect()
            except Exception:
                self.ready=False
                try:self.note('Operazione bloccata',['Generazione disabilitata.', 'Riesegui Test integrita.', 'Controlla rete e swap.'])
                except Cancel:pass


def main():
    ui=UI()
    try:
        App(ui).run()
    except Exception:
        ui.render('ERRORE - BLOCCATO', ['Avvio o self-test falliti.', 'Non usare seed reali.'])
        while True: time.sleep(60)
    finally:
        ui.GPIO.cleanup()

if __name__=='__main__': main()
