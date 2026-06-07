#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Genere LE prochain Reel quotidien via le MOTEUR (visuel toujours identique).
# Choisit la 1re variante du POOL pas encore presente dans en_attente/poster.
# Rend -> copie dans Output/video/en_attente/Reel_<slug>.mp4 -> ajoute la caption.
import os, sys, glob, shutil, datetime
from engine import *
from scenes import render, s_hook, s_cta, s_features, s_commission, s_leads, s_beforeafter
from scenes2 import s_apps_chaos, s_pricecompare, s_checklist, s_kanban, s_reveal, s_starter

EN_ATTENTE = os.path.join(ASSETS, "video", "en_attente")
POSTER     = os.path.join(ASSETS, "video", "poster")
CAPTIONS   = os.path.join(ASSETS, "video", "captions.md")
os.makedirs(EN_ATTENTE, exist_ok=True)

GREEN_=GREEN; AMBER_=AMBER; BLUE_=BLUE; TEAL_=TEAL

# POOL : variantes UNIQUES (hook + scene + caption), toutes rendues par le moteur.
POOL = [
 dict(slug="commission_howmuch",
   scenes=[(s_hook,2.4,(["How much did you","ACTUALLY make","this month?"],"ACTUALLY",None,1)),
           (s_commission,5.0,("This month",16500,"auto-calculated, no formulas")),
           (s_cta,3.0,("Your Notion CRM does the math","Launching this week"))],
   total=10.4,
   cap=("How much did you ACTUALLY make this month? \U0001F4B8",
        "Your Notion CRM adds up every commission automatically. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #commission #notion #notiontemplate #realestatecrm #realestateincome #realtortips #realestatetips #productivity")),
 dict(slug="leads_neverlose",
   scenes=[(s_hook,2.4,(["Never lose","a lead","again"],"again",None,2)),
           (s_leads,5.2,("Every lead, tracked",[("Michael Smith","Buyer","ACTIVE",GREEN_),("Sarah Davis","Seller","HOT",AMBER_),("David Lee","Buyer","NEW",BLUE_),("Anna Roe","Seller","ACTIVE",GREEN_)])),
           (s_cta,3.0,("One CRM for every lead","Launching this week"))],
   total=10.6,
   cap=("Never lose a lead again \U0001F3E1",
        "Buyers, sellers, follow-ups — all tracked in one Notion CRM. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #realestateleads #notion #notiontemplate #realestatecrm #leadmanagement #realtortips #realestatetips #newagent")),
 dict(slug="features_5tools",
   scenes=[(s_hook,2.4,(["5 tools.","One Notion","page."],"One Notion",None,1)),
           (s_features,5.4,("Replace your whole stack",[("Spreadsheets","→ gone","CRM",BLUE_),("Sticky notes","→ gone","TASKS",AMBER_),("Calculator","→ auto","$$$",TEAL_)])),
           (s_cta,3.0,("All-in-one for realtors","Launching this week"))],
   total=10.8,
   cap=("5 tools → one Notion page \U0001F5C2️",
        "Stop paying for 5 apps. One template runs your whole real estate business. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #productivity #realtortips #realestatetips #realestatelife #newrealtor")),
 dict(slug="price_stoppaying",
   scenes=[(s_hook,2.4,(["Stop paying","monthly for","a CRM"],"monthly",None,1)),
           (s_pricecompare,4.8,()),
           (s_cta,3.0,("$39 once. Yours forever.","Launching this week"))],
   total=10.2,
   cap=("Stop paying monthly for a real estate CRM \U0001F4B8",
        "$99/mo forever, or $39 once in Notion. Do the math. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #realestatecrm #notion #notiontemplate #realtortips #realestatetips #realestatemarketing #crm #realestatelife")),
 dict(slug="kanban_seeeverydeal",
   scenes=[(s_hook,2.4,(["See every deal","at a","glance"],"glance",None,2)),
           (s_kanban,5.0,()),
           (s_cta,3.0,("Your pipeline on one board","Launching this week"))],
   total=10.4,
   cap=("See every deal at a glance \U0001F3E1",
        "From new lead to closed — your whole pipeline on one Notion board. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #dealflow #pipeline #realtortips #realestatetips #realestatemarketing")),
 dict(slug="apps_tabchaos",
   scenes=[(s_hook,2.4,(["20 browser tabs","to run your","business?"],"20 browser tabs",None,0)),
           (s_apps_chaos,5.4,()),
           (s_cta,3.0,("Close the tabs. Open Notion.","Launching this week"))],
   total=10.8,
   cap=("20 browser tabs to run your real estate business? \U0001F62E‍\U0001F4A8",
        "Close them all. One Notion page does it. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #productivity #realtortips #realestatetips #realestatelife #newrealtor")),
 dict(slug="beforeafter_glowup",
   scenes=[(s_hook,2.4,(["Your business,","glow","up"],"glow",None,1)),
           (s_beforeafter,9.2,()),
           (s_cta,3.0,("From chaos to clarity","Launching this week"))],
   total=14.6,
   cap=("Real estate business glow-up ✨",
        "Messy spreadsheets → one clean Notion system. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #beforeandafter #realtortips #realestatetips #productivity #realestatelife")),
 dict(slug="checklist_doyouhave",
   scenes=[(s_hook,2.4,(["Does your system","have all","5?"],"all",None,1)),
           (s_checklist,5.2,("A realtor needs",["Lead CRM","Listings tracker","Deal pipeline","Follow-up reminders","Commission math"])),
           (s_cta,3.0,("This template has all 5","Launching this week"))],
   total=10.6,
   cap=("Does your system have all 5? ✅",
        "Lead CRM, listings, pipeline, follow-ups, commissions — all in one Notion page. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity #realestatelife #newagent")),
 dict(slug="starter_firstweek",
   scenes=[(s_hook,2.4,(["Your first week","as an","agent"],"first week",None,0)),
           (s_starter,5.4,()),
           (s_cta,3.0,("Start organized from day one","Launching this week"))],
   total=10.8,
   cap=("Your first week as a real estate agent \U0001F3E1",
        "Don't start in 6 messy apps. One Notion page for everything. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #newrealtor #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity #realestatelife")),
 dict(slug="reveal_seeinside",
   scenes=[(s_hook,2.4,(["See inside the","#1 Notion CRM","for agents"],"#1",None,1)),
           (s_reveal,5.0,()),
           (s_cta,3.0,("The all-in-one realtor template","Launching this week"))],
   total=10.4,
   cap=("See inside the Notion CRM built for agents \U0001F440",
        "5 connected databases, one page. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity #realestatelife #newagent")),
]

def used_slugs():
    s=set()
    for d in (EN_ATTENTE, POSTER):
        for f in glob.glob(os.path.join(d,"Reel_*.mp4")):
            s.add(os.path.basename(f)[5:-4])  # strip 'Reel_' and '.mp4'
    return s

def pick():
    used=used_slugs()
    for v in POOL:
        if v["slug"] not in used:
            return v
    return None  # tout le pool est consomme

def append_caption(slug, cap, dur):
    nom,desc,tags=cap
    # Format simple (mise en ligne facile): description, ligne vide, hashtags.
    block="\n---\n**Reel_%s.mp4**\n\n%s\n\n%s\n" % (slug, desc, tags)
    with open(CAPTIONS,"a",encoding="utf-8") as f:
        f.write(block)

def main():
    v=pick()
    if v is None:
        print("POOL epuise - rien a generer (ajouter des variantes au POOL)."); return 1
    slug=v["slug"]
    render(slug, v["scenes"], v["total"])
    src=os.path.join(OUT, slug+".mp4")
    dst=os.path.join(EN_ATTENTE, "Reel_"+slug+".mp4")
    shutil.copyfile(src, dst)
    append_caption(slug, v["cap"], v["total"])
    print("GENERE:", dst)
    return 0

if __name__=="__main__":
    sys.exit(main())
