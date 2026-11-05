"""LCD views, dark blue panels and orange focus, drawn locally with Pillow."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from i18n import tr
BG='#101827'; PANEL='#22344f'; CARD='#2d486b'; ORANGE='#ff9d24'; TEXT='#ffffff'; MUTED='#b6c9df'

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
    d.rounded_rectangle((5,4,width-5,34),radius=7,fill=PANEL)
    if is_home:
        x=width-22
        d.rounded_rectangle((width-38,5,width-6,33),radius=6,fill=ORANGE if power_focused else CARD)
        color=BG if power_focused else ORANGE
        d.arc((x-9,10,x+9,28),-55,235,fill=color,width=2)
        d.line((x,8,x,19),fill=color,width=3)
        d.text((12,7),fitted(d,title,font(18,True),width-58),font=font(18,True),fill=TEXT)
    else:
        if back_focused:d.rounded_rectangle((7,5,31,33),radius=5,fill=ORANGE)
        d.line((23,12,16,19,23,26),fill=BG if back_focused else ORANGE,width=3)
        d.text((36,7),fitted(d,title,font(18,True),width-44),font=font(18,True),fill=TEXT)
    return im,d

def footer(d,width,text):
    # The app supplies at most two useful instruction lines.
    import textwrap
    f=font(13 if width==240 else 15);lines=[];line=''
    for word in str(text).split():
        trial=(line+' '+word).strip()
        if d.textlength(trial,font=f)<=width-16:line=trial
        else:
            if line:lines.append(line)
            line=word
    if line:lines.append(line)
    for row,line in enumerate(lines[:2]):d.text((8,201+row*18),line,font=f,fill=MUTED)

def render(ui,width,title,lines,help_text):
    im,d=frame(width,title,getattr(ui,'back_focused',False))
    options=getattr(ui,'menu_active',False) or any(str(line).startswith('> ') for line in lines)
    for row,line in enumerate(list(lines)[:5]):
        selected=str(line).startswith('> ')
        text=str(line)[2:] if selected else str(line)
        if options:
            y=40+row*30
            d.rounded_rectangle((8,y,width-8,y+27),radius=5,fill=ORANGE if selected else CARD)
            d.text((15,y+1),fitted(d,text,ui.font,width-30),font=ui.font,fill=BG if selected else TEXT)
        else:
            d.text((9,42+row*29),fitted(d,text,ui.font,width-18),font=ui.font,fill=TEXT)
    footer(d,width,help_text);ui.disp.show_image(im,0,0)

def die(d,box,value,selected=False):
    fill=ORANGE if selected else '#eaf0fa';ink=BG
    d.rounded_rectangle(box,radius=5,fill=fill)
    x,y,x2,y2=box;cx=(x+x2)/2;cy=(y+y2)/2;dx=(x2-x)*.25;dy=(y2-y)*.25
    points={1:[(0,0)],2:[(-1,-1),(1,1)],3:[(-1,-1),(0,0),(1,1)],4:[(-1,-1),(1,-1),(-1,1),(1,1)],5:[(-1,-1),(1,-1),(-1,1),(1,1),(0,0)],6:[(-1,-1),(1,-1),(-1,0),(1,0),(-1,1),(1,1)]}[value]
    for px,py in points:
        xx=cx+px*dx;yy=cy+py*dy;r=2.3
        d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=ink)

def dice(ui,width,value,done,total,rolls):
    im,d=frame(width,tr('Lancio %d/%d'%(done+1,total)),getattr(ui,'back_focused',False))
    d.rounded_rectangle((10,40,width-10,48),radius=3,fill=PANEL)
    if done:d.rounded_rectangle((10,40,10+(width-20)*done/total,48),radius=3,fill=ORANGE)
    f=font(16)
    d.text((12,53),tr('Ultimi: '+''.join(map(str,rolls[-12:]))),font=f,fill=MUTED)
    cell=45;gap=12;left=(width-(cell*3+gap*2))//2
    for i in range(6):
        x=left+(i%3)*(cell+gap);y=79+(i//3)*55
        die(d,(x,y,x+cell,y+cell),i+1,selected=i+1==value and not getattr(ui,'back_focused',False))
    footer(d,width,tr('Freccia: Centro per uscire' if getattr(ui,'back_focused',False) else 'Frecce: scegli / Centro: salva K1: cancella / K3: esci'))
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
    labels=tuple(tr(v) for v in ('Seed BIP39','Password','Verifica','Strumenti'))
    cw=(width-24)//2
    for i,label in enumerate(labels):
        x=8+(i%2)*(cw+8);y=43+(i//2)*76
        box=(x,y,x+cw,y+69);active=i==index
        d.rounded_rectangle(box,radius=8,fill=ORANGE if active else CARD)
        color=BG if active else TEXT
        icon(d,i,x+cw/2,y+23,color)
        size=15 if width==240 else 18
        while size>11 and font(size,True).getlength(label)>cw-8:size-=1
        centered(d,(x,y+46,x+cw,y+67),label,font(size,True),color)
    footer(d,width,tr('Frecce: scegli / Centro: apri Su: Power'))
    ui.disp.show_image(im,0,0)
