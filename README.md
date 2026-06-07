# Stackly — Reels automatiques dans le cloud (PC éteint)

Chaque jour vers **6h (Paris)**, GitHub génère 1 Reel et l'envoie sur ton **téléphone** via **ntfy**
(la vidéo + la description avec les hashtags en **un seul paragraphe**, prête à copier). Ton ordi peut rester éteint.

## Ton topic ntfy (à garder)
```
stackly-reels-6ea4593711de5d97
```

## Mise en place (une seule fois, ~10 min)

### 1. Compte GitHub
Va sur https://github.com → crée un compte gratuit si tu n'en as pas.

### 2. Créer le repo
- Clique **New repository** → nom : `stackly-reels` → coche **Public** (obligatoire : c'est ce qui héberge la vidéo en permanence) → **Create**.

### 3. Mettre les fichiers
- Sur la page du repo : **Add file → Upload files**.
- Glisse **tout le contenu** de ce dossier (`engine.py`, `scenes.py`, `scenes2.py`, `daily.py`, `cloud_run.py`, `requirements.txt`, le dossier `assets/`, `state/`, `out/`). **Commit**.
- Le dossier `.github` est parfois caché. Si l'upload ne le prend pas : onglet **Actions** → **set up a workflow yourself** → efface le contenu, colle celui de `.github/workflows/daily.yml` (fourni) → **Commit**.

### 4. Ajouter le topic en secret
- **Settings → Secrets and variables → Actions → New repository secret**.
- Name : `NTFY_TOPIC`  |  Secret : `stackly-reels-6ea4593711de5d97`  → **Add secret**.

### 5. Sur ton téléphone
- Installe l'app **ntfy** (App Store / Play Store, gratuite).
- **Subscribe to topic** → serveur `ntfy.sh` → topic : `stackly-reels-6ea4593711de5d97` → OK.

### 6. Tester maintenant
- Onglet **Actions** → workflow **stackly-daily-reel** → **Run workflow**.
- En ~1-2 min, ton téléphone reçoit une notif : la vidéo + la caption. ✅

## Au quotidien
- Tu reçois 1 Reel/matin. Tu télécharges la vidéo, tu la postes (TikTok + Reel IG) en ajoutant le **son tendance in-app**, tu copies la caption. Lien bio **vide** jusqu'au lien d'achat.
- Le pool contient **10 variantes** → ~10 jours. Quand c'est épuisé (notif "slug vide"), ajouter des variantes dans `POOL` de `daily.py` puis ré-uploader le fichier.

## Notes
- Heure : GitHub tourne en UTC sans heure d'été → ~6h l'été, ~5h l'hiver. Ajustable dans `daily.yml` (ligne cron).
- Si tu changes le POOL en local, ré-uploade `daily.py` dans le repo pour garder le cloud synchro.
