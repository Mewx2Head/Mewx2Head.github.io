"""Remplit le tableau de synthèse E5 (documents/tableau-synthese-E5.xlsx) puis le convertit en PDF.

Modifier les listes FORMATION / PREMIERE_ANNEE / ALTERNANCE ci-dessous, puis lancer :
    python3 scripts/tableau.py
La conversion en PDF utilise LibreOffice (commande soffice).
"""
import os
import subprocess
import openpyxl
from openpyxl.styles import Alignment, Font

DOCS = os.path.join(os.path.dirname(__file__), "..", "documents")
XLSX = os.path.join(DOCS, "tableau-synthese-E5.xlsx")
wb = openpyxl.load_workbook(XLSX)
ws = wb.active

# Colonnes compétences : C=patrimoine D=incidents E=présence en ligne F=projet G=mise à disposition H=dév. pro
COL = {'C1': 'C', 'C2': 'D', 'C3': 'E', 'C4': 'F', 'C5': 'G', 'C6': 'H'}
FORMATION = [
    ("Création et mise à jour de ce portfolio (https://mewx2head.github.io)", "Depuis 09/25", ['C3', 'C6']),
    ("Mise en production d'un contrôleur de domaine sous Windows Server 2019 (AD DS, DNS, DHCP)\nDocument : diaporama « Infrastructure Active Directory » (portfolio)", "03/26 à 04/26", ['C1', 'C5']),
    ("Mise en place d'une politique de sécurité des mots de passe via AD DS (GPO, verrouillage, audit)\nDocument : diaporama « Infrastructure Active Directory » (portfolio)", "30/03/26", ['C1', 'C5']),
    ("StratAdvise : infrastructure réseau segmentée (VLAN, DHCP, routage inter-VLAN)\nDocument : présentation « StratAdvise » (portfolio)", "11/25", ['C5']),
    ("Gestion du parc et support utilisateur avec la solution ITSM GLPI", "12/25 à 05/27", ['C1', 'C2']),
    ("Création d'un profil LinkedIn présentant mes réalisations techniques", "12/25", ['C3', 'C6']),
    ("Parcours Cisco Networking Academy : Premiers pas avec Packet Tracer, Exploring Networking, Exploring IoT", "11/25", ['C5', 'C6']),
]
PREMIERE_ANNEE = []

ALTERNANCE = [
    ("Déploiement de 3 salles de réunion Microsoft Teams Rooms (caméra Logitech, Tap IP, comptes de ressource, licences Teams Rooms Pro)", "09/26", ['C1', 'C4', 'C5']),
    ("Administration des comptes utilisateurs et des licences Microsoft 365", "Depuis le 24/08/26", ['C1', 'C2']),
    ("Enrôlement des nouveaux postes de travail dans Microsoft Intune", "Depuis le 24/08/26", ['C1', 'C5']),
    ("Gestion de la téléphonie : création de lignes, changement de titulaire ou de numéro, téléphones", "Depuis le 24/08/26", ['C1', 'C2']),
    ("Support utilisateurs : impression, SharePoint, cloud, écrans défectueux", "Depuis le 24/08/26", ['C1', 'C2']),
]

def fill(rows, first, last):
    for r in range(first, last + 1):
        for c in "ABCDEFGH":
            ws[f"{c}{r}"].value = None
    for k, (title, period, comps) in enumerate(rows):
        r = first + k
        assert r <= last, "plus de lignes que dans le modèle"
        ws[f"A{r}"].value = title
        ws[f"B{r}"].value = period
        for comp in comps:
            ws[f"{COL[comp]}{r}"].value = "X"
    for r in range(first, last + 1):
        ws[f"A{r}"].alignment = Alignment(wrap_text=True, vertical="center", horizontal="left")
        ws[f"A{r}"].font = Font(name=ws[f"A{r}"].font.name, sz=10, b=False)
        ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws[f"B{r}"].font = Font(name=ws[f"B{r}"].font.name, sz=9)
        for c in "CDEFGH":
            ws[f"{c}{r}"].alignment = Alignment(vertical="center", horizontal="center")
            ws[f"{c}{r}"].font = Font(name=ws[f"{c}{r}"].font.name, sz=14, b=True)
        ws.row_dimensions[r].height = 42

fill(FORMATION, 9, 18)
ws["A19"].value = "Réalisations en milieu professionnel en cours de première année"
fill(PREMIERE_ANNEE, 20, 26)
ws["A27"].value = "Réalisations en milieu professionnel en cours de seconde année (alternance IT chez QSRP)"
fill(ALTERNANCE, 28, 34)
ws["A8"].value = "Réalisations en cours de formation"
for r in (8, 19, 27):
    ws.row_dimensions[r].height = 22
    ws[f"A{r}"].alignment = Alignment(horizontal="center", vertical="center")
    ws[f"A{r}"].font = Font(name=ws[f"A{r}"].font.name, sz=11, b=True)
from copy import copy
for r in list(range(9, 19)) + list(range(20, 27)) + list(range(28, 35)):
    for c in "ABCDEFGH":
        ws[f"{c}{r}"].border = copy(ws[f"{c}9"].border)
ws.print_area = "A1:H34"
wb.save(XLSX)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", DOCS, XLSX],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Tableau mis à jour : documents/tableau-synthese-E5.xlsx et .pdf")
