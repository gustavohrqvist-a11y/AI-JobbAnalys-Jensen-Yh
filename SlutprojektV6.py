
#========================================
#       AI JOBBMATCHNING V6
#========================================
# Mål: Matcha användarens profil mot jobbannonser
# och visa vilka jobb som passar bäst.
#========================================


#========================================
#       IMPORTER
#========================================

import requests
import json
from datetime import datetime


#========================================
#       HJÄLPMETODER
#========================================

def normalisera(text):
    """Gör texten enklare att jämföra."""
    return text.lower().strip()


def visa_kompetenser(kompetenser):
    """Returnerar matchande kompetenser som text."""
    if kompetenser:
        return ", ".join(kompetenser)
    return "Inga"


#========================================
#       KLASSER
#========================================

class MatchningsData:
    """Basklass för gemensam information."""
    
    def __init__(self):
        self.plats = []
        self.kompetenser = []


class Profil(MatchningsData):
    """Användarens profil."""

    def __init__(self):
        super().__init__()
        self.jobb = []

    def input_jobb(self):
        print("\n" + "=" * 40)

        try:
            jobb_input = input(
                "Vad hade du velat jobba som? "
            ).split(",")

            jobb_input = [
                normalisera(jobb)
                for jobb in jobb_input
                if jobb.strip()
            ]

            self.jobb.extend(jobb_input)

        except (KeyboardInterrupt, EOFError):
            print("\nInmatningen avbröts.")

    def input_plats(self):
        print("\n" + "=" * 40)

        try:
            plats_input = input(
                "Vart hade du velat jobba? "
            ).split(",")

            plats_input = [
                normalisera(plats)
                for plats in plats_input
                if plats.strip()
            ]

            self.plats.extend(plats_input)

        except (KeyboardInterrupt, EOFError):
            print("\nInmatningen avbröts.")

    def input_kompetenser(self):
        print("\n" + "=" * 40)

        try:
            kompetens_input = input(
                "Vad har du för kompetenser? "
            ).split(",")

            kompetens_input = [
                normalisera(kompetens)
                for kompetens in kompetens_input
                if kompetens.strip()
            ]

            self.kompetenser.extend(kompetens_input)

        except (KeyboardInterrupt, EOFError):
            print("\nInmatningen avbröts.")


class Jobbannons(MatchningsData):
    """Innehåller information om en jobbannons."""

    def __init__(self, jobb, plats, kompetenser, länk):
        super().__init__()

        self.jobb = jobb
        self.plats = plats
        self.kompetenser = kompetenser
        self.länk = länk


class Matchare:
    """Matchar användarens profil mot jobbannonser."""

    def __init__(self, profil, arbetsmarknad):
        self.profil = profil
        self.arbetsmarknad = arbetsmarknad

    def match(self):
        matchningar = []

        # Går igenom alla jobbannonser
        for jobb in self.arbetsmarknad:

            jobb_matchar = False

            # Kontrollerar om jobbtiteln matchar
            for önskat_jobb in self.profil.jobb:

                if önskat_jobb in jobb.jobb:
                    jobb_matchar = True
                    break

            # Hoppa över jobbet om titeln inte matchar
            if not jobb_matchar:
                continue

            poäng = 0

            # Matchar önskad plats
            for plats in self.profil.plats:

                if plats in jobb.plats:
                    poäng += 2
                    break

            # Matchar användarens kompetenser
            for kompetens in self.profil.kompetenser:

                if kompetens in jobb.kompetenser:
                    poäng += 1

            # Ett jobb som matchar titeln får minst 1 poäng
            if poäng == 0:
                poäng = 1

            matchningar.append((jobb, poäng))

        # Högsta poäng visas först
        matchningar.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return matchningar


#========================================
#       API
#========================================

def hämta_jobb_från_api(profil):

    if not profil.jobb:
        print("Du måste ställa in din profil först.")
        return []

    url = "https://jobsearch.api.jobtechdev.se/search"

    jobbannonser = []
    alla_data = []

    try:

        # Söker efter varje önskat jobb
        for sökord in profil.jobb:

            print(f"\nSöker efter: {sökord}")

            params = {
                "q": sökord,
                "limit": 10
            }

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            print("Statuskod:", response.status_code)

            if response.status_code != 200:
                print("Kunde inte hämta jobbannonser.")
                continue

            data = response.json()
            alla_data.append(data)

            träffar = data.get("hits", [])

            print("Antal träffar:", len(träffar))

            # Skapar Jobbannons-objekt
            for jobb in träffar:

                titel = normalisera(
                    jobb.get("headline") or ""
                )

                plats_info = jobb.get(
                    "workplace_address"
                ) or {}

                plats = normalisera(
                    plats_info.get("municipality") or ""
                )

                länk = jobb.get(
                    "webpage_url"
                ) or ""

                beskrivning = normalisera(
                    jobb.get(
                        "description", {}
                    ).get("text") or ""
                )

                matchade_kompetenser = []

                # Letar efter användarens kompetenser
                # i jobbannonsens beskrivning
                for kompetens in profil.kompetenser:

                    if kompetens in beskrivning:
                        matchade_kompetenser.append(
                            kompetens
                        )

                annons = Jobbannons(
                    titel,
                    plats,
                    matchade_kompetenser,
                    länk
                )

                jobbannonser.append(annons)

        #========================================
        #       SPARA API-DATA
        #========================================

        try:

            with open(
                "jobbdata.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    alla_data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

        except OSError as fel:

            print("\nKunde inte spara jobbdata.")
            print(fel)

        return jobbannonser

    except requests.exceptions.RequestException as fel:

        print("\nEtt fel uppstod när API:t kontaktades.")
        print(fel)

        return []

    except json.JSONDecodeError:

        print("\nKunde inte läsa svaret från API:t.")

        return []


#========================================
#       HISTORIK
#========================================

def spara_historik(profil, matchningar):

    try:

        with open(
            "historik.json",
            "r",
            encoding="utf-8"
        ) as f:

            historik = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):

        historik = []

    ny_sökning = {
        "datum": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),

        "profil": {
            "jobb": profil.jobb,
            "plats": profil.plats,
            "kompetenser": profil.kompetenser
        },

        "matchningar": []
    }

    # Sparar alla matchningar
    for jobb, poäng in matchningar:

        ny_sökning["matchningar"].append({
            "jobb": jobb.jobb,
            "plats": jobb.plats,
            "poäng": poäng,
            "kompetenser": jobb.kompetenser,
            "länk": jobb.länk
        })

    historik.append(ny_sökning)

    try:

        with open(
            "historik.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                historik,
                f,
                ensure_ascii=False,
                indent=4
            )

    except OSError as fel:

        print("\nKunde inte spara historiken.")
        print(fel)
        return

    print("\nSökningen har sparats i historiken.")


def visa_historik():

    try:

        with open(
            "historik.json",
            "r",
            encoding="utf-8"
        ) as f:

            historik = json.load(f)

    except FileNotFoundError:

        print("\nDet finns ingen historik ännu.")
        return

    except json.JSONDecodeError:

        print("\nHistorikfilen kunde inte läsas.")
        return

    if not historik:

        print("\nDet finns ingen historik ännu.")
        return

    print("\n" + "=" * 40)
    print("              HISTORIK")
    print("=" * 40)

    # Går igenom tidigare sökningar
    for nummer, sökning in enumerate(
        historik,
        start=1
    ):

        print(f"\nSökning {nummer}")
        print(f"Datum: {sökning['datum']}")

        print(
            f"Jobb: "
            f"{', '.join(sökning['profil']['jobb'])}"
        )

        print(
            f"Plats: "
            f"{', '.join(sökning['profil']['plats'])}"
        )

        print(
            f"Kompetenser: "
            f"{', '.join(sökning['profil']['kompetenser'])}"
        )

        print("\nMatchningar:")

        for jobb in sökning["matchningar"]:

            print(f"  - {jobb['jobb']}")
            print(f"    Plats: {jobb['plats']}")
            print(f"    Poäng: {jobb['poäng']}")

            print(
                "    Matchande kompetenser: "
                + visa_kompetenser(
                    jobb["kompetenser"]
                )
            )

            print(f"    Länk: {jobb['länk']}")

        print("-" * 40)


#========================================
#       VISA MATCHNINGAR
#========================================

def visa_matchningar(profil):

    print("\nHämtar aktuella jobbannonser...")

    jobb_fran_api = hämta_jobb_från_api(profil)

    if not jobb_fran_api:

        print("Inga jobbannonser kunde hämtas.")
        return

    matchare = Matchare(
        profil,
        jobb_fran_api
    )

    matchningar = matchare.match()

    if not matchningar:

        print("\nInga jobb matchade din profil.")
        return

    # Sparar sökningen i historiken
    spara_historik(
        profil,
        matchningar
    )

    print("\n" + "=" * 40)
    print("           DINA MATCHNINGAR")
    print("=" * 40)

    for jobb, poäng in matchningar:

        print(f"\n- {jobb.jobb}")
        print(f"  Plats: {jobb.plats}")
        print(f"  Poäng: {poäng}")

        print(
            "  Matchande kompetenser: "
            + visa_kompetenser(
                jobb.kompetenser
            )
        )

        print(f"  Länk: {jobb.länk}")


#========================================
#       ANVÄNDARGRÄNSSNITT
#========================================

profil = Profil()


def user_ui():

    while True:

        print("\n")
        print("=" * 40)
        print("       VÄLKOMMEN TILL AI-JOBBANALYS")
        print("=" * 40)

        print("1. Ställ in profil")
        print("2. Visa matchningar")
        print("3. Historik")
        print("4. Avsluta")

        print("=" * 40)

        try:

            svar = input(
                "Välj ett alternativ 1-4: "
            )

        except (KeyboardInterrupt, EOFError):

            print("\nProgrammet avslutas.")
            break

        #========================================
        #       PROFIL
        #========================================

        if svar == "1":

            profil.input_jobb()
            profil.input_plats()
            profil.input_kompetenser()

            print("\nProfil ändrad!")

            print(
                f"\nJobb: {profil.jobb}"
                f"\nPlats/Ort: {profil.plats}"
                f"\nKompetenser: {profil.kompetenser}"
            )

        #========================================
        #       MATCHNINGAR
        #========================================

        elif svar == "2":

            visa_matchningar(profil)

        #========================================
        #       HISTORIK
        #========================================

        elif svar == "3":

            visa_historik()

        #========================================
        #       AVSLUTA
        #========================================

        elif svar == "4":

            print("\nTack för denna gång!")
            break

        #========================================
        #       FELAKTIGT VAL
        #========================================

        else:

            print("\nFelaktigt val.")
            print("Välj en siffra mellan 1 och 4.")


#========================================
#       STARTA PROGRAMMET
#========================================

user_ui()


#========================================
#       UTVECKLINGSPLAN
#========================================

# 1. Profil:
#    Jobb, Plats, Kompetenser
#
# 2. API:
#    Hämta aktuella jobbannonser
#
# 3. Matchning:
#    Matcha jobb, plats, kompetenser
#
# 4. Resultat:
#    Visa jobb och matchningspoäng
#
# 5. Förbättringar:
#    Validering, Historik, Bättre UI
#
# 6. Testning:
#    Testa och färdigställ programmet

