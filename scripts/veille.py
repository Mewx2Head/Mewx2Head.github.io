"""Récupère les flux RSS de veille et écrit veille.json pour le portfolio.

Lancé automatiquement par GitHub Actions (.github/workflows/veille.yml).
Uniquement la bibliothèque standard Python : rien à installer.
"""
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape

FEEDS = [
    ("CERT-FR", "https://www.cert.ssi.gouv.fr/feed/"),
    ("IT-Connect", "https://www.it-connect.fr/feed/"),
    ("LeMagIT", "https://www.lemagit.fr/rss/ContentSyndication.xml"),
    ("Zataz", "https://www.zataz.com/feed/"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
]

# Mots-clés du thème de veille : sécurité Active Directory et rançongiciels
KEYWORDS = [
    "active directory", "entra", "kerberos", "ntlm", "gpo", "contrôleur de domaine",
    "domain controller", "ransomware", "rançongiciel", "rançon", "windows server",
    "ldap", "kerberoast", "mimikatz", "ad cs",
]

MAX_PER_FEED = 15
MAX_ITEMS = 40
ATOM = "{http://www.w3.org/2005/Atom}"


def text(el):
    return (el.text or "").strip() if el is not None else ""


def clean(s, limit=220):
    s = unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[:limit].rsplit(" ", 1)[0] + "…"


def parse_date(s):
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def read_feed(source, url):
    req = urllib.request.Request(url, headers={"User-Agent": "portfolio-veille/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    items = []
    # RSS 2.0
    for it in root.iter("item"):
        items.append((text(it.find("title")), text(it.find("link")),
                      text(it.find("pubDate")), text(it.find("description"))))
    # Atom
    for it in root.iter(ATOM + "entry"):
        link = it.find(ATOM + "link")
        items.append((text(it.find(ATOM + "title")), link.get("href", "") if link is not None else "",
                      text(it.find(ATOM + "updated")) or text(it.find(ATOM + "published")),
                      text(it.find(ATOM + "summary"))))
    out = []
    for title, link, date, desc in items[:MAX_PER_FEED]:
        d = parse_date(date)
        if not title or not link:
            continue
        blob = (title + " " + desc).lower()
        out.append({
            "source": source,
            "title": clean(title, 200),
            "link": link,
            "date": d.isoformat() if d else None,
            "summary": clean(desc),
            "theme": any(k in blob for k in KEYWORDS),
        })
    return out


def main():
    feeds = json.loads(os.environ["VEILLE_FEEDS"]) if os.environ.get("VEILLE_FEEDS") else FEEDS
    out_path = os.environ.get("VEILLE_OUT", "veille.json")
    items, errors = [], []
    for source, url in feeds:
        try:
            items += read_feed(source, url)
        except Exception as e:  # un flux en panne ne doit pas bloquer les autres
            errors.append(f"{source}: {e}")
    if not items:
        raise SystemExit("Aucun flux n'a pu être lu : " + "; ".join(errors))
    items.sort(key=lambda i: i["date"] or "", reverse=True)
    data = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "sources": sorted({i["source"] for i in items}),
        "items": items[:MAX_ITEMS],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{len(data['items'])} articles écrits dans {out_path}")
    for e in errors:
        print("Flux ignoré :", e)


if __name__ == "__main__":
    main()
