"""LCD views, dark blue panels and orange focus, drawn locally with Pillow."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from i18n import tr
BG='#101827'; PANEL='#22344f'; CARD='#2d486b'; ORANGE='#ff9d24'; TEXT='#ffffff'; MUTED='#b6c9df'
KEYBOARD_COLUMNS=6
CONTENT_TOP = 42
CONTENT_BOTTOM = 232
MARGIN = 8
GAP = 6

def font(size,bold=False):
    return ImageFont.truetype(str(Path(__file__).resolve().parent/'fonts'/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)

def fitted(draw,text,f,max_width):
    text=str(text)
    if draw.textlength(text,font=f)<=max_width:return text
    while text and draw.textlength(text+'...',font=f)>max_width:text=text[:-1]
    return text+'...'

def centered(draw,box,text,f,fill):
    b=draw.textbbox((0,0),text,font=f)
    draw.text(((box[0]+box[2]-(b[2]-b[0]))/2-b[0],(box[1]+box[3]-(b[3]-b[1]))/2-b[1]),text,font=f,fill=fill)

def frame(width,title,back_focused=False,is_home=False,power_focused=False):
    im=Image.new('RGB',(width,240),BG);d=ImageDraw.Draw(im)
    if is_home:
        x=width-22
        d.rounded_rectangle((width-38,5,width-6,33),radius=6,fill=ORANGE if power_focused else CARD)
        color=BG if power_focused else ORANGE
        d.arc((x-9,10,x+9,28),-55,235,fill=color,width=2)
        d.line((x,8,x,19),fill=color,width=3)
        title_font = font(19, True)
        centered(d,(42,4,width-42,34),fitted(d,title,title_font,width-84),title_font,TEXT)
    else:
        d.rounded_rectangle((5,4,width-5,34),radius=7,fill=PANEL)
        if back_focused:d.rounded_rectangle((7,5,31,33),radius=5,fill=ORANGE)
        d.line((23,12,16,19,23,26),fill=BG if back_focused else ORANGE,width=3)
        d.text((36,7),fitted(d,title,font(18,True),width-44),font=font(18,True),fill=TEXT)
    return im,d


def cell_span(start, end, count, index):
    """Divide an inclusive pixel range into cells with equal gaps."""
    pixels = end - start + 1 - GAP * (count - 1)
    left = start + index * GAP + index * pixels // count
    right = start + index * GAP + (index + 1) * pixels // count - 1
    return left, right


def render(ui,width,title,lines,help_text):
    im,d=frame(width,title,getattr(ui,'back_focused',False))
    rows = list(lines)[:5]
    options=getattr(ui,'menu_active',False) or any(str(line).startswith('> ') for line in rows)
    right = width - MARGIN
    if options:
        for row, line in enumerate(rows):
            selected = str(line).startswith('> ')
            label = str(line)[2:] if selected else str(line)
            y, bottom = cell_span(CONTENT_TOP, CONTENT_BOTTOM, len(rows), row)
            d.rounded_rectangle((MARGIN,y,right,bottom),radius=6,fill=ORANGE if selected else CARD)
            centered(d,(15,y,width-15,bottom),fitted(d,label,ui.font,width-30),ui.font,BG if selected else TEXT)
    elif rows:
        d.rounded_rectangle((MARGIN,CONTENT_TOP,right,CONTENT_BOTTOM),radius=8,fill=PANEL)
        line_height = 29
        top = (CONTENT_TOP + CONTENT_BOTTOM - len(rows) * line_height) // 2
        for row, line in enumerate(rows):
            y = top + row * line_height
            centered(d,(9,y,width-9,y+line_height),fitted(d,line,ui.font,width-18),ui.font,TEXT)
    ui.disp.show_image(im,0,0)

def keyboard(ui, width, number, prefix, keys, focus, invalid, suggestions):
    image, draw = frame(width, tr('Parola %d' % number), focus == -1)
    word_font = font(20, True)
    typed = fitted(draw, prefix or '—', word_font, width - 20)
    centered(draw, (10, 38, width - 10, 65), typed, word_font, TEXT)
    if suggestions:
        preview = '  ·  '.join(suggestions[:2])
        if len(suggestions) > 2:
            preview += '  …'
        suggestion_font = font(14, True)
        draw.rounded_rectangle((6, 64, width - 6, 85), radius=4, fill=PANEL)
        centered(draw, (9, 64, width - 9, 85), fitted(draw, preview, suggestion_font, width - 18), suggestion_font, ORANGE)
    next_letters = {word[len(prefix)] for word in suggestions if len(word) > len(prefix)}
    key_font = font(15, True)
    cell_width = (width - 12) // KEYBOARD_COLUMNS
    for index, label in enumerate(keys):
        row, col = divmod(index, KEYBOARD_COLUMNS)
        left = 6 + col * cell_width
        top = 89 + row * 24
        box = (left, top, left + cell_width - 3, top + 22)
        active = index == focus
        draw.rounded_rectangle(box, radius=4, fill=ORANGE if active else CARD)
        available = not prefix or label in next_letters or label in ('DEL', 'OK')
        color = (BG if active else TEXT) if available else ('#574738' if active else MUTED)
        centered(draw, box, label, key_font, color)
    hint = tr('Parola non trovata') if invalid else tr('K1: cancella · K3: esci')
    if suggestions and focus >= 0:
        hint = 'K2: ' + (suggestions[0] if len(suggestions) == 1 else tr('Parole suggerite'))
    hint_font = font(13)
    centered(draw, (6, 212, width - 6, 237), fitted(draw, hint, hint_font, width - 12), hint_font, MUTED)
    ui.disp.show_image(image, 0, 0)


def die(d,box,value,selected=False):
    fill=ORANGE if selected else '#eaf0fa';ink=BG
    d.rounded_rectangle(box,radius=5,fill=fill)
    x,y,x2,y2=box;cx=(x+x2)/2;cy=(y+y2)/2;dx=(x2-x)*.25;dy=(y2-y)*.25
    points={1:[(0,0)],2:[(-1,-1),(1,1)],3:[(-1,-1),(0,0),(1,1)],4:[(-1,-1),(1,-1),(-1,1),(1,1)],5:[(-1,-1),(1,-1),(-1,1),(1,1),(0,0)],6:[(-1,-1),(1,-1),(-1,0),(1,0),(-1,1),(1,1)]}[value]
    for px,py in points:
        xx=cx+px*dx;yy=cy+py*dy;r=2.3
        d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=ink)

def dice(ui,width,value,done,total,rolls,diceware=False):
    title = 'Parola %d/%d' % (done // 5 + 1, total // 5) if diceware else 'Lancio %d/%d' % (done + 1, total)
    im,d=frame(width,tr(title),getattr(ui,'back_focused',False))
    d.rounded_rectangle((10,40,width-10,48),radius=3,fill=PANEL)
    if done:d.rounded_rectangle((10,40,10+(width-20)*done/total,48),radius=3,fill=ORANGE)
    f=font(16)
    status = 'Lancio %d/5' % (done % 5 + 1) if diceware else 'Ultimi: ' + ''.join(map(str,rolls[-12:]))
    centered(d,(10,49,width-10,77),tr(status),f,MUTED)
    for i in range(6):
        left, right = cell_span(MARGIN, width - MARGIN, 3, i % 3)
        top, bottom = cell_span(79, CONTENT_BOTTOM, 2, i // 3)
        die(d,(left,top,right,bottom),i+1,selected=i+1==value and not getattr(ui,'back_focused',False))
    ui.disp.show_image(im,0,0)

def icon(d,kind,cx,cy,color):
    if kind==0:die(d,(cx-14,cy-14,cx+14,cy+14),5,False)
    elif kind==1:
        d.rounded_rectangle((cx-15,cy-1,cx+15,cy+17),radius=4,outline=color,width=2)
        d.arc((cx-10,cy-17,cx+10,cy+7),180,360,fill=color,width=3)
        d.ellipse((cx-2,cy+5,cx+2,cy+9),fill=color)
    elif kind==2:d.line((cx-15,cy,cx-4,cy+12,cx+16,cy-14),fill=color,width=4)
    else:
        d.ellipse((cx-15,cy-15,cx+15,cy+15),outline=color,width=3)
        for off in (-8,0,8):d.line((cx-18,cy+off,cx+18,cy+off),fill=color,width=2)

def home(ui,width,index):
    im,d=frame(width,'SEEDGEN',is_home=True,power_focused=index==4)
    labels=tuple(tr(v) for v in ('Seed BIP39','Passphrase','Verifica','Strumenti'))
    for i, label in enumerate(labels):
        left, right = cell_span(MARGIN, width - MARGIN, 2, i % 2)
        top, bottom = cell_span(CONTENT_TOP, CONTENT_BOTTOM, 2, i // 2)
        active = i == index
        d.rounded_rectangle((left,top,right,bottom),radius=8,fill=ORANGE if active else CARD)
        color = BG if active else TEXT
        icon(d,i,(left+right)/2,top+32,color)
        size = 18
        label_font = font(size,True)
        while size > 11 and label_font.getlength(label) > right - left - 8:
            size -= 1
            label_font = font(size,True)
        centered(d,(left,top+56,right,bottom-5),label,label_font,color)
    ui.disp.show_image(im,0,0)

def power_menu(ui,width,index):
    im,d=frame(width,'Power',back_focused=index==-1)
    for position,label in enumerate(('Restart','Power off')):
        left, right = cell_span(MARGIN, width - MARGIN, 2, position)
        cx=(left+right)//2
        cy=111
        active=position==index
        color=BG if active else TEXT
        d.rounded_rectangle((left,CONTENT_TOP,right,CONTENT_BOTTOM),radius=8,fill=ORANGE if active else CARD)
        if position==0:
            d.arc((cx-17,cy-17,cx+17,cy+17),-75,245,fill=color,width=4)
            d.polygon(((cx-16,cy-18),(cx-4,cy-19),(cx-10,cy-8)),fill=color)
        else:
            d.arc((cx-17,cy-17,cx+17,cy+17),-55,235,fill=color,width=4)
            d.line((cx,cy-20,cx,cy),fill=color,width=4)
        centered(d,(left,150,right,191),label,font(16,True),color)
    ui.disp.show_image(im,0,0)
