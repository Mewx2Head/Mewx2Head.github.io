# Portfolio BTS SIO SISR · Aness Khenichil

Site : **https://mewx2head.github.io**

Portfolio de l'épreuve E5 du BTS SIO (option SISR) : compétences du Bloc 1, réalisations professionnelles, tableau de synthèse, veille technologique et parcours.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `index.html` | Page principale du portfolio |
| `projets/` | Présentations des projets (Active Directory, StratAdvise) |
| `images/` | Captures d'écran des projets, icône et image de partage |
| `documents/` | CV et tableau de synthèse E5 (PDF et Excel) |
| `veille.json` | Articles du fil de veille, mis à jour automatiquement |
| `scripts/veille.py` | Récupère les flux RSS de veille |
| `scripts/tableau.py` | Remplit le tableau de synthèse et génère le PDF |
| `scripts/build_pdf.js` | Génère le CV en PDF à partir de `documents/cv.html` |
| `.github/workflows/veille.yml` | Lance `veille.py` 3 fois par jour |

## Mettre à jour

**Une réalisation** : modifier la liste `REALISATIONS` dans `index.html`, puis la liste correspondante dans `scripts/tableau.py`, et lancer :

```bash
python3 scripts/tableau.py
```

**Le CV** : modifier `documents/cv.html`, puis lancer :

```bash
node scripts/build_pdf.js
```

**La veille** : rien à faire, le fil se met à jour tout seul. Pour forcer une mise à jour : onglet *Actions* → *Veille RSS* → *Run workflow*.
