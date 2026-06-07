#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, math, subprocess, os
from PIL import Image, ImageDraw
from engine import *

# ============ SCENE RENDERERS ============

def s_hook(img, lt, dur, lines, keyword=None, sub=None, kw_line=None):
    cy = 720
    n = len(lines)
    maxw = W-120; base = 104
    for _ln in lines:
        while base>52 and tw(_ln, font("b",base))>maxw: base -= 3
    lh = int(base*1.27)
    y0 = cy - (n-1)*lh/2
    for i, ln in enumerate(lines):
        appear = i*0.16
        p = e_back((lt-appear)/0.5)
        if p <= 0: continue
        alpha = int(255*clamp((lt-appear)/0.32))
        scale = 0.7 + 0.3*clamp(p)
        f = font("b", int(base*scale))
        y = y0 + i*lh
        if kw_line == i and keyword and ln.strip()==keyword:
            if p>0.9: highlight_word(img,(W/2,y),keyword,font("b",base))
            else: text(img,(W/2,y),ln,f,fill=TEAL,anchor="mm",alpha=alpha)
        else:
            text(img,(W/2,y),ln,f,fill=WHITE,anchor="mm",alpha=alpha)
    if sub:
        p=clamp((lt-0.5)/0.5)
        text(img,(W/2,y0+n*lh+40),sub,font("m",44),fill=MUTED,anchor="mm",alpha=int(255*p))

def deal_card(img, box, name, sub, status, scolor, p, accent=BLUE):
    dy = (1-e_back(p))*120
    x0,y0,x1,y1 = box
    b=[x0,y0+dy,x1,y1+dy]
    card(img,b,r=26,fill=CARD,glow=accent if status in("ACTIVE","WON") else None)
    ImageDraw.Draw(img).rounded_rectangle([x0,y0+dy,x0+10,y1+dy],radius=5,fill=accent+(255,))
    text(img,(x0+44,y0+dy+34),name,font("b",40),fill=WHITE,anchor="lm")
    text(img,(x0+44,y0+dy+86),sub,font("r",32),fill=MUTED,anchor="lm")
    pill(img,(x1-110,y0+dy+(y1-y0)/2),status,scolor)

def s_features(img, lt, dur, title, items):
    text(img,(W/2,300),title,font("b",60),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    p=clamp((lt-0.2)/0.4)
    ImageDraw.Draw(img).rounded_rectangle([W/2-90,345,W/2-90+180*p,353],radius=4,fill=TEAL+(255,))
    y=470; gap=190
    for i,(name,sub,st,col) in enumerate(items):
        ap=i*0.18+0.3
        pp=clamp((lt-ap)/0.55)
        if pp<=0: continue
        deal_card(img,[100,y+i*gap,W-100,y+i*gap+150],name,sub,st,col,pp,accent=col)
    hold0=0.3+len(items)*0.18+0.6
    if lt>hold0:
        k=int((lt-hold0)/0.95)%len(items)
        yk=y+k*gap; pulse=0.5+0.5*math.sin((lt-hold0)*3.2)
        ImageDraw.Draw(img).rounded_rectangle([100,yk,W-100,yk+150],radius=26,outline=TEAL+(int(110+110*pulse),),width=4)

def s_commission(img, lt, dur, title, target, sub):
    text(img,(W/2,360),title,font("m",48),fill=MUTED,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    cp=e_out((lt-0.4)/2.2)
    val=target*clamp(cp)
    punch = 1.0
    if 2.55<lt<2.95: punch = 1+0.12*math.sin((lt-2.55)/0.4*math.pi)
    elif lt>=2.95: punch = 1+0.018*math.sin((lt-2.95)*2.6)
    f=font("b",int(190*punch))
    text(img,(W/2,720),fmt_money(val),f,fill=TEAL,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    vals=[6.2,8.9,12.4,16.5]
    bw=150; bx=W/2-(len(vals)*bw+(len(vals)-1)*40)/2
    for i,v in enumerate(vals):
        hh=int(360*(v/max(vals))*clamp((lt-0.7-i*0.12)/0.5))
        x=bx+i*(bw+40)
        c = TEAL if i==len(vals)-1 else BLUE
        ImageDraw.Draw(img).rounded_rectangle([x,1180-hh,x+bw,1180],radius=14,fill=c+(220,))
    text(img,(W/2,1260),sub,font("r",40),fill=MUTED,anchor="mm",alpha=int(255*clamp((lt-1.0)/0.5)))

def s_leads(img, lt, dur, title, rows):
    text(img,(W/2,300),title,font("b",58),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    p=clamp((lt-0.2)/0.5)
    if p>0:
        top=440
        card(img,[90,top,W-90,top+len(rows)*120+120],r=30,fill=CARD)
        text(img,(140,top+60),"NAME",font("b",30),fill=MUTED,anchor="lm")
        text(img,(560,top+60),"TYPE",font("b",30),fill=MUTED,anchor="lm")
        text(img,(W-150,top+60),"STATUS",font("b",30),fill=MUTED,anchor="rm")
        ImageDraw.Draw(img).line([140,top+110,W-140,top+110],fill=LINE+(255,),width=2)
        for i,(nm,ty,st,col) in enumerate(rows):
            ap=0.4+i*0.16; rp=clamp((lt-ap)/0.4)
            if rp<=0: continue
            ry=top+170+i*120; dx=(1-e_out(rp))*60
            a=int(255*rp)
            text(img,(140+dx,ry),nm,font("b",38),fill=WHITE,anchor="lm",alpha=a)
            text(img,(560+dx,ry),ty,font("r",34),fill=MUTED,anchor="lm",alpha=a)
            pill(img,(W-220,ry),st,col)
        hold0=0.4+len(rows)*0.16+0.45
        if lt>hold0:
            k=int((lt-hold0)/0.85)%len(rows)
            ry=top+170+k*120; pulse=0.5+0.5*math.sin((lt-hold0)*3.2)
            ImageDraw.Draw(img).rounded_rectangle([120,ry-48,W-120,ry+48],radius=18,outline=TEAL+(int(80+100*pulse),),width=3)

def s_beforeafter(img, lt, dur):
    split=3.2
    if lt<split:
        a=int(255*clamp(lt/0.4))
        if lt>split-0.4: a=int(255*clamp((split-lt)/0.4))
        text(img,(W/2,300),"BEFORE",font("b",64),fill=RED,anchor="mm",alpha=a)
        import random; random.seed(7)
        msgs=["Sheet1 row 14?","=VLOOKUP(#REF!)","lost lead??","follow up...when","commission =0"]
        for i in range(5):
            ry=470+i*150; jit=random.randint(-30,30)
            card(img,[120+jit,ry,W-120+jit,ry+120],r=18,fill=(40,28,30))
            text(img,(160+jit,ry+60),msgs[i],font("m",36),fill=(220,170,170),anchor="lm",alpha=a)
        text(img,(W/2,1320),"spreadsheets = chaos",font("m",44),fill=MUTED,anchor="mm",alpha=a)
    else:
        l2=lt-split
        text(img,(W/2,300),"AFTER",font("b",64),fill=TEAL,anchor="mm",alpha=int(255*clamp(l2/0.4)))
        items=[("Smith - 12 Oak St","Showing","ACTIVE",GREEN),
               ("Davis - 5 Pine Ct","Offer","HOT",AMBER),
               ("Wilson - 240 Elm","Closed","WON",TEAL)]
        for i,(nm,sb,st,col) in enumerate(items):
            p=clamp((l2-0.3-i*0.18)/0.5)
            if p<=0: continue
            deal_card(img,[110,470+i*200,W-110,470+i*200+160],nm,sb,st,col,p,accent=col)
        hold0=0.3+3*0.18+0.6
        if l2>hold0:
            k=int((l2-hold0)/0.95)%3
            yk=470+k*200; pulse=0.5+0.5*math.sin((l2-hold0)*3.2)
            ImageDraw.Draw(img).rounded_rectangle([110,yk,W-110,yk+160],radius=26,outline=TEAL+(int(110+110*pulse),),width=4)
        text(img,(W/2,1360),"one Notion page = clarity",font("m",46),fill=WHITE,anchor="mm",alpha=int(255*clamp((l2-0.6)/0.5)))

def s_cta(img, lt, dur, line1, line2):
    p=e_back(lt/0.6); cy=600
    if p>0:
        od=ImageDraw.Draw(img)
        for k,off in enumerate([60,30,0]):
            c=[BLUE,(70,140,230),TEAL][k]
            od.polygon([(W/2,cy-60+off),(W/2+120,cy+off),(W/2,cy+60+off),(W/2-120,cy+off)],fill=c+(255,))
    a1=int(255*clamp((lt-0.5)/0.5))
    for i,ln in enumerate(wrap(line1,font("b",72),W-160)):
        text(img,(W/2,820+i*92),ln,font("b",72),fill=WHITE,anchor="mm",alpha=a1)
    p=e_back((lt-0.9)/0.6)
    if p>0:
        bw=560*clamp(p); bh=120; bx=W/2-bw/2; by=1120
        ImageDraw.Draw(img).rounded_rectangle([bx,by,bx+bw,by+bh],radius=60,fill=TEAL+(255,))
        if p>0.7: text(img,(W/2,by+bh/2-4),line2,font("b",48),fill=(8,18,24),anchor="mm")
    a=int(255*clamp((lt-1.4)/0.5))
    text(img,(W/2,1320),"Follow so you don't miss it",font("m",40),fill=MUTED,anchor="mm",alpha=a)

# ============ TIMELINE / RENDER ============
def render(name, scenes, totaldur):
    path=f"{OUT}/{name}.mp4"
    cmd=["ffmpeg","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}",
         "-framerate",str(FPS),"-i","-","-c:v","libx264","-pix_fmt","yuv420p","-crf","20",
         "-movflags","+faststart",path]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    nframes=int(totaldur*FPS)
    BG_RGBA=BG.convert("RGBA")
    bounds=[]; acc=0
    for fn,dur,args in scenes:
        bounds.append((acc,acc+dur,fn,args)); acc+=dur
    for fi in range(nframes):
        t=fi/FPS
        img=BG_RGBA.copy()
        for (st,en,fn,args) in bounds:
            if st<=t<en:
                fn(img,t-st,en-st,*args); break
        for b in bounds[1:]:
            cut=b[0]
            if abs(t-cut)<0.07:
                fa=int(120*(1-abs(t-cut)/0.07))
                img.alpha_composite(Image.new("RGBA",img.size,TEAL+(fa,)))
        progress(img,t/totaldur)
        brandmark(img,alpha=200)
        proc.stdin.write(img.convert("RGB").tobytes())
    proc.stdin.close(); proc.wait()
    return path

# ============ VIDEO DEFINITIONS ============
VIDEOS={}

VIDEOS["01_overview"]=([
    (s_hook,2.4,(["Run your WHOLE","real estate biz","in ONE page"],"page",None,2)),
    (s_features,9.0,("All-in-one Notion CRM",[
        ("Leads & contacts","buyers + sellers","CRM",BLUE),
        ("Deal pipeline","drag across stages","KANBAN",AMBER),
        ("Commissions","auto-calculated","AUTO",TEAL),
    ])),
    (s_cta,3.4,("The all-in-one Notion system for realtors","Launching this week")),
],14.8)

VIDEOS["02_pipeline"]=([
    (s_hook,2.4,(["Stop losing","deals in","spreadsheets"],"spreadsheets",None,2)),
    (s_features,9.0,("Your deal pipeline",[
        ("Smith - 12 Oak St","Showing","ACTIVE",GREEN),
        ("Davis - 5 Pine Ct","Offer sent","HOT",AMBER),
        ("Wilson - 240 Elm","Closing","WON",TEAL),
    ])),
    (s_cta,3.4,("Track every deal in one Notion page","Launching this week")),
],14.8)

VIDEOS["03_commissions"]=([
    (s_hook,2.4,(["Your commissions,","auto-","calculated"],"auto-",None,1)),
    (s_commission,9.0,("This month commissions",16500,"auto-calculated from each deal")),
    (s_cta,3.4,("Know your income at a glance","Launching this week")),
],14.8)

VIDEOS["04_leads"]=([
    (s_hook,2.4,(["Every lead.","One place.","Zero chaos."],"One place.",None,1)),
    (s_leads,9.0,("All your leads in one CRM",[
        ("Michael Smith","Buyer","ACTIVE",GREEN),
        ("Jennifer Brown","Seller","ACTIVE",GREEN),
        ("David Johnson","Buyer","NEW",BLUE),
        ("Sarah Davis","Buyer","HOT",AMBER),
    ])),
    (s_cta,3.4,("The CRM built for real estate agents","Launching this week")),
],14.8)

VIDEOS["05_beforeafter"]=([
    (s_hook,2.2,(["Spreadsheets","vs","Notion"],"vs",None,1)),
    (s_beforeafter,9.2,()),
    (s_cta,3.4,("Turn chaos into one clean system","Launching this week")),
],14.8)

if __name__=="__main__":
    pick=sys.argv[1] if len(sys.argv)>1 else "all"
    for name,(scenes,dur) in VIDEOS.items():
        if pick!="all" and pick not in name: continue
        print("rendering",name,"...",flush=True)
        render(name,scenes,dur)
        print("  done",flush=True)
