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
 dict(slug="money_on_the_table",
   scenes=[(s_hook,2.4,(["You're leaving","$3,000/mo","on the table"],"$3,000/mo",None,1)),
           (s_commission,5.0,("Lost to messy tracking",3000,"every month - gone")),
           (s_cta,3.0,("Plug the leak in Notion","Launching this week"))],
   total=10.4,
   cap=("You're leaving $3,000/mo on the table 💸",
        "Missed follow-ups = missed commissions. One Notion page tracks every deal so nothing slips. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #commission #realestateincome #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity")),
 dict(slug="commission_realtime",
   scenes=[(s_hook,2.4,(["Your commission,","in real","time"],"real",None,1)),
           (s_commission,5.0,("Closed this month",24800,"auto, zero formulas")),
           (s_cta,3.0,("Always know your number","Launching this week"))],
   total=10.4,
   cap=("Your commission, in real time 💸",
        "Add a deal, see your commission instantly - no spreadsheet math. Always know what you're making. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #commission #realestateincome #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity")),
 dict(slug="hundredk_year",
   scenes=[(s_hook,2.4,(["Track your way","to a $100k","year"],"$100k",None,1)),
           (s_commission,5.0,("Year to date",102000,"every deal adds up")),
           (s_cta,3.0,("Build your six-figure year","Launching this week"))],
   total=10.4,
   cap=("Track your way to a $100k year 💰",
        "Every closed deal adds up automatically. Watch your year-to-date income climb in one Notion page. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #commission #realestateincome #notion #notiontemplate #realestatecrm #realtortips #realestatetips #money")),
 dict(slug="stop_paying_99",
   scenes=[(s_hook,2.4,(["Stop paying","$99/mo for","a CRM"],"$99/mo",None,1)),
           (s_pricecompare,4.8,()),
           (s_cta,3.0,("$39 once. Yours forever.","Launching this week"))],
   total=10.2,
   cap=("Stop paying $99/mo for a real estate CRM 💸",
        "Most realtor CRMs bill you every month, forever. This Notion template does the same job for $39 - once. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #realestatecrm #crm #notion #notiontemplate #realtortips #realestatetips #realestatemarketing #money")),
 dict(slug="pays_in_one_deal",
   scenes=[(s_hook,2.4,(["This $39 tool","pays for itself","in one deal"],"one deal",None,2)),
           (s_features,5.4,("Replace your whole stack",[("Spreadsheets","-> gone","CRM",BLUE_),("Sticky notes","-> gone","TASKS",AMBER_),("Calculator","-> auto","$$$",TEAL_)])),
           (s_cta,3.0,("One deal pays it back 100x","Launching this week"))],
   total=10.8,
   cap=("This $39 tool pays for itself in one deal 💰",
        "Replace 5 apps with one Notion page. The first commission you protect pays it back 100x. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #commission #realestateincome #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity")),
 dict(slug="never_miss_commission",
   scenes=[(s_hook,2.4,(["Never miss","a commission","again"],"commission",None,1)),
           (s_leads,5.2,("Every lead = future cash",[("Michael Smith","Buyer","ACTIVE",GREEN_),("Sarah Davis","Seller","HOT",AMBER_),("David Lee","Buyer","NEW",BLUE_),("Anna Roe","Seller","ACTIVE",GREEN_)])),
           (s_cta,3.0,("Never leave money behind","Launching this week"))],
   total=10.6,
   cap=("Never miss a commission again 💸",
        "Every lead is future cash. Track buyers, sellers and follow-ups so no deal - and no commission - slips. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #realestateleads #commission #notion #notiontemplate #realestatecrm #realtortips #realestatetips #realestateincome")),
 dict(slug="pipeline_paycheck",
   scenes=[(s_hook,2.4,(["Your pipeline","is your","paycheck"],"paycheck",None,2)),
           (s_kanban,5.0,()),
           (s_cta,3.0,("Move deals = move money","Launching this week"))],
   total=10.4,
   cap=("Your pipeline is your paycheck 💰",
        "Every deal on the board is money in motion. See your whole pipeline from lead to closed in Notion. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #dealflow #pipeline #notion #notiontemplate #realestatecrm #realtortips #realestatetips #realestateincome")),
 dict(slug="apps_costing_deals",
   scenes=[(s_hook,2.4,(["6 apps are","costing you","deals"],"costing",None,1)),
           (s_apps_chaos,5.4,()),
           (s_cta,3.0,("One page. More closings.","Launching this week"))],
   total=10.8,
   cap=("6 apps are costing you deals 💸",
        "Jumping between Excel, Notes and your inbox loses deals - and commissions. Put it all in one Notion page. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #productivity #realtortips #realestatetips #realestateincome #newrealtor")),
 dict(slug="track_every_dollar",
   scenes=[(s_hook,2.4,(["Track every","dollar you","earn"],"dollar",None,1)),
           (s_checklist,5.2,("Your money, organized",["Lead CRM","Deal pipeline","Commission tracker","Follow-up reminders","Income dashboard"])),
           (s_cta,3.0,("Know your income to the $","Launching this week"))],
   total=10.6,
   cap=("Track every dollar you earn 💰",
        "Lead CRM, pipeline, commissions and an income dashboard - all connected in one Notion page. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #commission #realestateincome #notion #notiontemplate #realestatecrm #realtortips #realestatetips #productivity")),
 dict(slug="inside_money_machine",
   scenes=[(s_hook,2.4,(["See inside your","real estate","money machine"],"money machine",None,2)),
           (s_reveal,5.0,()),
           (s_cta,3.0,("The all-in-one realtor template","Launching this week"))],
   total=10.4,
   cap=("See inside your real estate money machine 💰",
        "5 connected databases, one page, built to grow your income. Launching this week ⤵️",
        "#realestate #realtor #realestateagent #realtorlife #notion #notiontemplate #realestatecrm #realestateincome #realtortips #realestatetips #productivity #newagent")),
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
