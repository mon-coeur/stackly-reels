#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Set 2 : hooks tranches + scenes distinctes (apps chaos, prix, checklist, kanban, reveal/starter).
import sys, os, math
from PIL import Image, ImageDraw
from engine import *
from scenes import s_hook, s_cta, deal_card, render

def s_apps_chaos(img, lt, dur):
    apps=[("Excel",(150,360)),("Google Sheets",(640,330)),("Sticky notes",(190,560)),
          ("WhatsApp",(700,580)),("Gmail",(150,820)),("Calendar",(640,830))]
    tphase=2.4; cx,cy=W/2,1030
    a0=int(255*clamp(lt/0.4))
    if lt<tphase+0.55:
        if lt<tphase: text(img,(W/2,200),"too many apps?",font("b",60),fill=RED,anchor="mm",alpha=a0)
        for i,(name,(x,y)) in enumerate(apps):
            j=10*math.sin(lt*6+i); prog=clamp((lt-tphase)/0.55)
            xx=x+(cx-x)*e_inout(prog); yy=y+(cy-y)*e_inout(prog); sc=1-0.55*prog
            f=font("b",max(10,int(40*sc))); w=tw(name,f)+50; h=max(20,int(72*sc))
            ImageDraw.Draw(img).rounded_rectangle([xx-w/2,yy-h/2+j,xx+w/2,yy+h/2+j],radius=18,fill=(48,28,32),outline=RED+(190,),width=2)
            text(img,(xx,yy+j),name,f,fill=(232,184,184),anchor="mm",alpha=int(255*(1-prog*0.4)))
    if lt>=tphase+0.35:
        l2=lt-(tphase+0.35); p=e_back(l2/0.5)
        if p>0:
            dy=(1-clamp(p))*80; box=[140,760+dy,W-140,1180+dy]
            card(img,box,r=34,fill=CARD,glow=TEAL)
            text(img,(W/2,850+dy),"One Notion page.",font("b",66),fill=WHITE,anchor="mm")
            text(img,(W/2,930+dy),"That's it.",font("m",46),fill=TEAL,anchor="mm")
            for i,lb in enumerate(["Leads","Deals","Tasks","Commissions"]):
                px=200+(i%2)*440; py=1020+dy+(i//2)*80
                pill(img,(px,py),lb.upper(),[BLUE,AMBER,GREEN,TEAL][i])

def s_pricecompare(img, lt, dur):
    text(img,(W/2,290),"Do the math.",font("b",60),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    if e_back((lt-0.4)/0.5)>0:
        card(img,[120,430,W-120,820],r=30,fill=(46,30,33))
        text(img,(W/2,520),"Other real estate CRMs",font("m",44),fill=(230,180,180),anchor="mm")
        text(img,(W/2,650),"$99",font("b",150),fill=RED,anchor="mm")
        text(img,(W/2,760),"every month. forever.",font("r",40),fill=MUTED,anchor="mm")
    if lt>1.0:
        text(img,(W/2,880),"VS",font("b",54),fill=WHITE,anchor="mm",alpha=int(255*clamp((lt-1.0)/0.4)))
    if e_back((lt-1.4)/0.5)>0:
        card(img,[120,950,W-120,1340],r=30,fill=CARD,glow=TEAL)
        text(img,(W/2,1040),"This Notion template",font("m",44),fill=TEAL,anchor="mm")
        text(img,(W/2,1170),"$39",font("b",150),fill=TEAL,anchor="mm")
        text(img,(W/2,1280),"once. yours forever.",font("b",42),fill=WHITE,anchor="mm")

def s_checklist(img, lt, dur, title, items):
    text(img,(W/2,300),title,font("b",58),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    top=470
    for i,it in enumerate(items):
        ap=0.4+i*0.4; p=clamp((lt-ap)/0.3)
        if p<=0: continue
        y=top+i*150; card(img,[110,y,W-110,y+120],r=22,fill=CARD)
        bx=180; by=y+60; checked=lt>ap+0.18; col=GREEN if checked else LINE
        ImageDraw.Draw(img).rounded_rectangle([bx-34,by-34,bx+34,by+34],radius=14,fill=(col+(60,)) if checked else (0,0,0,0),outline=col+(255,),width=4)
        if checked:
            d=ImageDraw.Draw(img)
            d.line([bx-16,by+2,bx-4,by+16],fill=GREEN+(255,),width=8)
            d.line([bx-4,by+16,bx+18,by-14],fill=GREEN+(255,),width=8)
        text(img,(250,by),it,font("b",44),fill=WHITE,anchor="lm",alpha=int(255*p))

def s_kanban(img, lt, dur):
    text(img,(W/2,300),"Your pipeline, as a board",font("b",52),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    cols=[("NEW",BLUE,[("Smith","12 Oak St")]),
          ("ACTIVE",AMBER,[("Davis","5 Pine Ct"),("Lee","9 Birch")]),
          ("CLOSED",GREEN,[("Wilson","240 Elm")])]
    cw=300; gap=30; x0=(W-(cw*3+gap*2))/2; top=440
    for ci,(name,col,cards) in enumerate(cols):
        cx=x0+ci*(cw+gap)
        if clamp((lt-0.3-ci*0.2)/0.4)<=0: continue
        ImageDraw.Draw(img).rounded_rectangle([cx,top,cx+cw,top+820],radius=24,fill=(18,30,42,255))
        pill(img,(cx+cw/2,top+50),name,col)
        for k,(nm,ad) in enumerate(cards):
            kp=e_back((lt-(0.6+ci*0.2+k*0.3))/0.5)
            if kp<=0: continue
            dy=(1-clamp(kp))*40; cy=top+120+k*180+dy
            card(img,[cx+18,cy,cx+cw-18,cy+150],r=18,fill=CARD)
            ImageDraw.Draw(img).rounded_rectangle([cx+18,cy,cx+28,cy+150],radius=5,fill=col+(255,))
            text(img,(cx+50,cy+50),nm,font("b",34),fill=WHITE,anchor="lm")
            text(img,(cx+50,cy+100),ad,font("r",28),fill=MUTED,anchor="lm")
    if lt>2.0:
        ci=int((lt-2.0)/1.0)%3; cx=x0+ci*(cw+gap); pulse=0.5+0.5*math.sin((lt-2.0)*3)
        ImageDraw.Draw(img).rounded_rectangle([cx,top,cx+cw,top+820],radius=24,outline=TEAL+(int(80+100*pulse),),width=4)

# reveal : vrai template (cover) dans un cadre navigateur
_COVER=Image.open(os.path.join(ASSETS,"cover_desktop_2048x1280.png")).convert("RGB")
_FW=W-160; _FH=int(_FW*_COVER.height/_COVER.width)
_FRAME=Image.new("RGBA",(_FW,_FH+70),(0,0,0,0)); _fd=ImageDraw.Draw(_FRAME)
_fd.rounded_rectangle([0,0,_FW,_FH+70],radius=28,fill=CARD+(255,))
_fd.ellipse([24,28,44,48],fill=RED+(255,)); _fd.ellipse([60,28,80,48],fill=AMBER+(255,)); _fd.ellipse([96,28,116,48],fill=GREEN+(255,))
_cmask=Image.new("L",(_FW,_FH),0); ImageDraw.Draw(_cmask).rounded_rectangle([0,0,_FW,_FH],radius=16,fill=255)
_FRAME.paste(_COVER.resize((_FW,_FH)),(0,70),_cmask)
def s_reveal(img, lt, dur):
    text(img,(W/2,300),"This is the actual template",font("b",52),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.4)))
    if e_out((lt-0.3)/0.7)>0:
        fy=int(560+(1-clamp(e_out((lt-0.3)/0.7)))*200); img.alpha_composite(_FRAME,(80,fy))
    if lt>2.0:
        text(img,(W/2,H-260),"5 connected databases. one page.",font("m",40),fill=MUTED,anchor="mm",alpha=int(255*clamp((lt-2.0)/0.5)))

# starter : page Notion propre construite nativement (alternative au reveal)
def s_starter(img, lt, dur):
    text(img,(W/2,290),"Everything in one page",font("b",54),fill=WHITE,anchor="mm",alpha=int(255*clamp(lt/0.3)))
    p=clamp((lt-0.1)/0.3)
    ImageDraw.Draw(img).rounded_rectangle([W/2-90,338,W/2-90+180*p,346],radius=4,fill=TEAL+(255,))
    card(img,[110,420,W-110,1340],r=30,fill=CARD)
    text(img,(170,505),"NOTION TEMPLATE",font("b",26),fill=TEAL,anchor="lm",spacing=4,alpha=int(255*clamp((lt-0.2)/0.3)))
    text(img,(170,565),"Real Estate Hub",font("b",52),fill=WHITE,anchor="lm",alpha=int(255*clamp((lt-0.25)/0.3)))
    mods=[("Leads & contacts","24 active",BLUE),("Listings & properties","8 live",AMBER),
          ("Deal pipeline","5 deals",GREEN),("Tasks & follow-ups","3 today",TEAL),("Commissions","$16,500",TEAL)]
    top0=690; rowh=128
    for i,(nm,val,col) in enumerate(mods):
        rp=e_out((lt-(0.45+i*0.16))/0.3)
        if rp<=0: continue
        ry=top0+i*rowh; dx=(1-rp)*40; a=int(255*clamp(rp)); d=ImageDraw.Draw(img)
        d.ellipse([170+dx,ry-14,198+dx,ry+14],fill=col+(a,))
        text(img,(230+dx,ry),nm,font("b",42),fill=WHITE,anchor="lm",alpha=a)
        text(img,(W-175,ry),val,font("m",38),fill=col,anchor="rm",alpha=a)
        if i<len(mods)-1: d.line([170,ry+64,W-170,ry+64],fill=LINE+(int(a*0.6),),width=2)
    hold0=0.45+len(mods)*0.16+0.4
    if lt>hold0:
        k=int((lt-hold0)/0.8)%len(mods); ry=top0+k*rowh; pulse=0.5+0.5*math.sin((lt-hold0)*3.2)
        ImageDraw.Draw(img).rounded_rectangle([150,ry-50,W-150,ry+50],radius=16,outline=TEAL+(int(70+90*pulse),),width=3)

V2={}
V2["06_apps"]=([(s_hook,2.4,(["POV: you juggle","6 apps to close","ONE deal"],"6 apps",None,1)),(s_apps_chaos,5.4,()),(s_cta,3.0,("Run it all from one Notion page","Launching this week"))],10.8)
V2["07_price"]=([(s_hook,2.4,(["Your CRM should","NOT cost","$99/month"],"$99/month",None,2)),(s_pricecompare,4.8,()),(s_cta,3.0,("Same system. $39, once.","Launching this week"))],10.2)
V2["08_checklist"]=([(s_hook,2.4,(["Everything a realtor","needs in","ONE page"],"ONE page",None,2)),(s_checklist,5.2,("A realtor's whole system",["Leads & contacts","Listings & properties","Deal pipeline","Tasks & follow-ups","Commissions"])),(s_cta,3.0,("The all-in-one realtor template","Launching this week"))],10.6)
V2["09_kanban"]=([(s_hook,2.4,(["Drag. Drop.","Close.","Repeat."],"Close.",None,1)),(s_kanban,5.0,()),(s_cta,3.0,("Track every deal on one board","Launching this week"))],10.4)
V2["10_reveal"]=([(s_hook,2.4,(["New real estate agent?","Start with","THIS"],"THIS",None,2)),(s_reveal,5.0,()),(s_cta,3.0,("Your business, organized from day one","Launching this week"))],10.4)

if __name__=="__main__":
    pick=sys.argv[1] if len(sys.argv)>1 else "all"
    for name,(scns,dur) in V2.items():
        if pick!="all" and pick not in name: continue
        print("rendering",name,"...",flush=True); render(name,scns,dur); print("  done",flush=True)
