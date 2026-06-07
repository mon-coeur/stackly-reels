#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trendy vertical video engine (1080x1920) for Notion realtor template promos.
Style: navy/teal brand UI mockups, kinetic typography, count-ups, pops, fast cuts.
No audio (user adds trending sound in-app)."""
import os, math, subprocess
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 24
BASE = os.path.dirname(os.path.abspath(__file__))      # dossier du moteur (portable)
ASSETS = os.environ.get("REEL_ASSETS") or os.path.normpath(os.path.join(BASE, "..", "..", "Output"))  # cloud: REEL_ASSETS
OUT = os.path.join(BASE, "vids")                       # rendus -> Tools/video_engine/vids
os.makedirs(OUT, exist_ok=True)

# ---- palette ----
BG_TOP   = (10, 22, 33)
BG_BOT   = (6, 14, 22)
CARD     = (20, 34, 48)
CARD2    = (26, 42, 58)
LINE     = (44, 64, 84)
WHITE    = (240, 246, 252)
MUTED    = (146, 166, 186)
BLUE     = (96, 165, 250)
TEAL     = (35, 212, 191)
GREEN    = (52, 211, 153)
AMBER    = (251, 191, 95)
RED      = (248, 113, 113)

FONTS = "/usr/share/fonts/truetype/google-fonts/"
@lru_cache(maxsize=256)
def font(w, size):
    f = {"b":"Poppins-Bold.ttf","m":"Poppins-Medium.ttf","r":"Poppins-Regular.ttf","l":"Poppins-Light.ttf"}[w]
    return ImageFont.truetype(FONTS+f, int(size))

_MEAS = ImageDraw.Draw(Image.new("RGB",(8,8)))

# ---- easing ----
def clamp(x,a=0.0,b=1.0): return max(a,min(b,x))
def e_out(t):  t=clamp(t); return 1-(1-t)**3
def e_inout(t):t=clamp(t); return 4*t*t*t if t<.5 else 1-(-2*t+2)**3/2
def e_back(t):
    t=clamp(t); c1=1.70158; c3=c1+1
    return 1+c3*(t-1)**3+c1*(t-1)**2

# ---- background (precomputed once) ----
def make_bg():
    base = Image.new("RGB",(W,H),BG_TOP)
    top=Image.new("RGB",(W,H),BG_TOP); bot=Image.new("RGB",(W,H),BG_BOT)
    mask=Image.new("L",(W,H),0); md=ImageDraw.Draw(mask)
    for y in range(H): md.line([(0,y),(W,y)],fill=int(255*(y/H)))
    base=Image.composite(bot,top,mask)
    # soft brand glows
    glow=Image.new("RGB",(W,H),(0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.ellipse([-200,-260,540,480],fill=(18,52,74))
    gd.ellipse([640,1380,1280,2060],fill=(14,60,58))
    glow=glow.filter(ImageFilter.GaussianBlur(170))
    base=Image.blend(base,Image.composite(glow,base,Image.new("L",(W,H),60)),1.0)
    # subtle grid dots
    d=ImageDraw.Draw(base)
    for gy in range(0,H,90):
        for gx in range(0,W,90):
            d.ellipse([gx-1,gy-1,gx+1,gy+1],fill=(26,42,58))
    return base
BG = make_bg()

# ---- drawing helpers ----
def rrect(draw, box, r, fill=None, outline=None, width=2):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def card(img, box, r=28, fill=CARD, glow=None, shadow=True):
    # fast: draw directly on RGBA (Pillow blends), no per-frame gaussian blur
    x0,y0,x1,y1=box
    d=ImageDraw.Draw(img)
    if shadow:
        d.rounded_rectangle([x0+4,y0+12,x1+4,y1+14],radius=r,fill=(0,0,0,90))
    d.rounded_rectangle(box,radius=r,fill=fill+(255,))
    if glow:
        d.rounded_rectangle([x0,y0,x1,y1],radius=r,outline=glow+(220,),width=3)

def text(img, xy, s, fnt, fill=WHITE, anchor="la", spacing=0, alpha=255):
    # draw directly on RGBA (Pillow blends ink alpha) -> fast, no full-size layers
    if alpha<=0: return
    d=ImageDraw.Draw(img)
    col=fill+(int(alpha),)
    if spacing==0:
        d.text(xy,s,font=fnt,fill=col,anchor=anchor); return
    asc=anchor[0]
    widths=[d.textlength(c,font=fnt)+spacing for c in s]
    tot=sum(widths)-spacing
    x=xy[0]-(tot/2 if asc=="m" else tot if asc=="r" else 0); y=xy[1]
    for c,wd in zip(s,widths):
        d.text((x,y),c,font=fnt,fill=col,anchor="l"+anchor[1]); x+=wd

def tw(s,fnt):
    return _MEAS.textlength(s,font=fnt)

def pill(img, center, label, color):
    f=font("b",30); pad=24
    w=tw(label,f)+pad*2; h=52
    x,y=center; box=[x-w/2,y-h/2,x+w/2,y+h/2]
    d=ImageDraw.Draw(img)
    d.rounded_rectangle(box,radius=26,fill=color+(50,),outline=color+(255,),width=2)
    text(img,(x,y-3),label,f,fill=color,anchor="mm")

def highlight_word(img, center, word, fnt, barcolor=TEAL, txtcolor=(8,16,24)):
    w=tw(word,fnt); x,y=center; pad=18
    box=[x-w/2-pad,y-fnt.size*0.62,x+w/2+pad,y+fnt.size*0.62]
    d=ImageDraw.Draw(img)
    d.rounded_rectangle(box,radius=16,fill=barcolor+(255,))
    text(img,(x,y),word,fnt,fill=txtcolor,anchor="mm")

def progress(img, p):
    y=70
    d=ImageDraw.Draw(img)
    d.rounded_rectangle([60,y,W-60,y+10],radius=5,fill=(255,255,255,40))
    d.rounded_rectangle([60,y,60+(W-120)*clamp(p),y+10],radius=5,fill=TEAL+(255,))

def brandmark(img, alpha=255):
    f=font("b",34)
    text(img,(W/2,H-70),"STACKLY",f,fill=MUTED,anchor="mm",spacing=14,alpha=alpha)

# wrap helper
def wrap(s,fnt,maxw):
    words=s.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if tw(t,fnt)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def fmt_money(v):
    return "$"+f"{int(round(v)):,}"
