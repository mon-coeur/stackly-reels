#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Runner CLOUD (GitHub Actions). Genere le prochain Reel du POOL pas encore envoye,
# ecrit caption.txt (description + hashtags en 1 paragraphe), met a jour state/used.json.
# Le workflow commit le mp4 + l'etat, puis pousse la notif ntfy (video + caption) sur le tel.
import os, sys, json, shutil
import datetime
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo=None
HERE=os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("REEL_ASSETS", os.path.join(HERE,"assets"))
from daily import POOL          # meme POOL que le moteur local (source unique)
from scenes import render
from engine import OUT

STATE=os.path.join(HERE,"state","used.json")
OUTDIR=os.path.join(HERE,"out"); os.makedirs(OUTDIR,exist_ok=True)

def used():
    try: return json.load(open(STATE))
    except: return []
def save(u): json.dump(u,open(STATE,"w"),indent=1)
def pick(u):
    for v in POOL:
        if v["slug"] not in u: return v
    return None
def emit(k,v):
    gh=os.environ.get("GITHUB_OUTPUT")
    if gh: open(gh,"a").write(f"{k}={v}\n")

def main():
    # Garde-fou horaire : ne generer qu a 3h heure de Paris (cron UTC double).
    if os.environ.get("GITHUB_EVENT_NAME")=="schedule" and ZoneInfo is not None:
        h=datetime.datetime.now(ZoneInfo("Europe/Paris")).hour
        if h!=3:
            print(f"Pas 3h a Paris (il est {h}h) -> skip"); emit("slug",""); return 0
    u=used(); v=pick(u)
    if v is None:
        print("POOL_EXHAUSTED - ajouter des variantes au POOL"); emit("slug",""); return 0
    slug=v["slug"]
    render(slug, v["scenes"], v["total"])
    shutil.copyfile(os.path.join(OUT, slug+".mp4"), os.path.join(OUTDIR,"Reel_"+slug+".mp4"))
    nom,desc,tags=v["cap"]
    open(os.path.join(HERE,"caption.txt"),"w",encoding="utf-8").write(f"{desc} {tags}")
    u.append(slug); save(u); emit("slug",slug)
    print("GENERATED", slug)
    return 0

if __name__=="__main__":
    sys.exit(main())
