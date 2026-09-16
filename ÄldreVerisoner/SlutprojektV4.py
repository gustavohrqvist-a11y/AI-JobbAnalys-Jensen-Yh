#========================================
#       AI JOBBMATCHNING V4
#========================================
# Mål: Matcha användarens profil mot jobbannonser
# och visa vilka jobb som passar bäst.
#========================================


#========================================
#       IMPORTER
#========================================

import requests


#========================================
#       KLASSER & METODER
#========================================

class MatchningsData:
    # Grundklass som innehåller gemensam information
    # för användarens profil och jobbannonser.

    def __init__(self):
        self.plats = []
        self.kompetenser = []


class Profil(MatchningsData):
    # Innehåller information om användarens önskemål
    # och kompetenser.

    def __init__(self):
        super().__init__()
        self.jobb = []


    # Låter användaren ange vilket jobb de vill arbeta med.
    def input_jobb(self):
        print("\n" + "=" * 40)

        jobb_input = input(
            "Vad hade du velat jobba som? "
        ).lower().strip().split(",")

        jobb_input = [jobb.strip() for jobb in jobb_input]

        self.jobb.extend(jobb_input)


    # Låter användaren ange var de vill arbeta.
    def input_plats(self):
        print("\n" + "=" * 40)

        plats_input = input(
            "Vart hade du velat jobba? "
        ).lower().strip().split(",")

        plats_input = [plats.strip() for plats in plats_input]

        self.plats.extend(plats_input)


    # Låter användaren ange sina kompetenser
    # och sparar dem i profilen.
    def input_kompetenser(self):
        print("\n" + "=" * 40)

        kompetens_input = input(
            "Vad har du för kompetenser? "
        ).lower().strip().split(",")

        kompetens_input = [
            kompetens.strip()
            for kompetens in kompetens_input
        ]

        self.kompetenser.extend(kompetens_input)


class Jobbannons(MatchningsData):
    # Innehåller information om ett specifikt jobb
    # som hämtas från API:t.

    def __init__(self, jobb, plats, kompetenser, länk):
        super().__init__()

        self.jobb = jobb
        self.plats = plats
        self.kompetenser = kompetenser
        self.länk = länk


#========================================
#       MATCHNING
#========================================

class Matchare:
    # Jämför användarens profil med jobbannonser
    # och räknar ut en matchningspoäng.

    def __init__(self, profil, arbetsmarknad):
        self.profil = profil
        self.arbetsmarknad = arbetsmarknad

    def match(self):
        # Lista där alla jobb som matchar profilen sparas.
        matchningar = []

        # Går igenom alla jobbannonser och jämför
        # dem med användarens profil.
        for jobb in self.arbetsmarknad:

            # Kontrollerar om jobbets titel
            # innehåller något av användarens önskade jobb.
            jobb_matchar = False

            for önskat_jobb in self.profil.jobb:
                if önskat_jobb in jobb.jobb:
                    jobb_matchar = True
                    break

            # Hoppar över jobbet om yrket inte matchar.
            if not jobb_matchar:
                continue

            poäng = 0

            # Ger poäng om jobbets plats
            # matchar användarens önskade plats.
            for plats in self.profil.plats:
                if plats in jobb.plats:
                    poäng += 2
                    break

            # Ger poäng för varje kompetens
            # som matchar jobbannonsen.
            for kompetens in self.profil.kompetenser:
                if kompetens in jobb.kompetenser:
                    poäng += 1

            # Om jobbet matchar yrket men inget annat,
            # får jobbet ändå 1 poäng.
            if poäng == 0:
                poäng = 1

            # Sparar jobbannonsen tillsammans med dess poäng.
            matchningar.append((jobb, poäng))

        # Sorterar jobben från högst till lägst matchningspoäng.
        matchningar.sort(
            key=lambda x: x[1], # Fukntion som byggs på en rad, i detta fall används den för att sortera jobbmatchningarna.
            reverse=True
        )

        return matchningar


#========================================
#       API
#========================================

def hämta_jobb_från_api(profil):
    # Hämtar aktuella jobbannonser från JobTechs API
    # baserat på användarens önskade jobb.

    if not profil.jobb:
        print("Du måste ställa in din profil först.")
        return []

    url = "https://jobsearch.api.jobtechdev.se/search"

    jobbannonser = []

    try:

        # Söker efter varje önskat jobb separat.
        for sökord in profil.jobb:

            print(f"\nSöker efter: {sökord}")

            params = {
                "q": sökord,
                "limit": 20
            }

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            print("Statuskod:", response.status_code)

            # Kontrollerar om API:t kunde genomföra sökningen.
            if response.status_code != 200:
                print("Kunde inte hämta jobbannonser.")
                continue

            data = response.json()

            print(
                "Antal träffar:",
                len(data.get("hits", []))
            )

            # Går igenom jobbannonserna som API:t returnerar.
            for jobb in data.get("hits", []):

                # Hämtar jobbets titel.
                titel = (
                    jobb.get("headline") or ""
                ).strip().lower()

                # Hämtar information om jobbets plats.
                plats_info = (
                    jobb.get("workplace_address") or {}
                )

                plats = (
                    plats_info.get("municipality") or ""
                ).strip().lower()

                # Hämtar länken till jobbannonsen.
                länk = jobb.get("webpage_url") or ""

                # Hämtar texten från jobbannonsens beskrivning.
                beskrivning = (
                    jobb.get("description", {}).get("text") or ""
                ).lower()

                # Hittar användarens kompetenser
                # som finns i jobbannonsens beskrivning.
                matchade_kompetenser = []

                for kompetens in profil.kompetenser:

                    if kompetens in beskrivning:
                        matchade_kompetenser.append(
                            kompetens
                        )

                # Skapar ett Jobbannons-objekt
                # med informationen från API:t.
                annons = Jobbannons(
                    titel,
                    plats,
                    matchade_kompetenser,
                    länk
                )

                jobbannonser.append(annons)

        return jobbannonser

    # Hanterar fel som kan uppstå när API:t kontaktas.
    except requests.exceptions.RequestException as fel:

        print("\nEtt fel uppstod när API:t kontaktades.")
        print(fel)

        return []


#========================================
#       VISA MATCHNINGAR
#========================================

def visa_matchningar(profil):
    # Hämtar aktuella jobbannonser och visar
    # de jobb som matchar användarens profil.

    print("\nHämtar aktuella jobbannonser...")

    jobb_fran_api = hämta_jobb_från_api(profil)

    # Avslutar funktionen om inga jobbannonser hämtades.
    if not jobb_fran_api:
        print("Inga jobbannonser kunde hämtas.")
        return

    # Skapar en matchare med användarens profil
    # och jobbannonserna från API:t.
    matchare = Matchare(
        profil,
        jobb_fran_api
    )

    matchningar = matchare.match()

    # Visar ett meddelande om inga jobb matchade profilen.
    if not matchningar:
        print("\nInga jobb matchade din profil.")
        return

    print("\n" + "=" * 40)
    print("           DINA MATCHNINGAR")
    print("=" * 40)

    # Skriver ut varje matchning och dess poäng.
    for jobb, poäng in matchningar:

        print(f"\n- {jobb.jobb}")
        print(f"  Plats: {jobb.plats}")
        print(f"  Poäng: {poäng}")

        # Visar vilka kompetenser som matchade.
        if jobb.kompetenser:
            print(
                "  Matchande kompetenser: "
                f"{', '.join(jobb.kompetenser)}"
            )
        else:
            print("  Matchande kompetenser: Inga")

        # Visar länken till jobbannonsen.
        print(f"  Länk: {jobb.länk}")


#========================================
#       ANVÄNDARENS PROFIL
#========================================

# Skapar användarens profil.
profil = Profil()


#========================================
#       HUVUDFUNKTION
#========================================

def user_ui():
    # Programmets huvudmeny.

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

        svar = input("Välj ett alternativ 1-4: ")

        #========================================
        #       STÄLL IN PROFIL
        #========================================

        if svar == "1":

            # Låter användaren ange sina önskemål
            # och kompetenser.
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
        #       VISA MATCHNINGAR
        #========================================

        elif svar == "2":

            # Hämtar och visar aktuella jobbmatchningar.
            visa_matchningar(profil)

        #========================================
        #       HISTORIK
        #========================================

        elif svar == "3":

            # Historikfunktionen är ännu inte implementerad.
            print("\nHistorik är inte implementerad ännu.")

        #========================================
        #       AVSLUTA
        #========================================

        elif svar == "4":

            # Avslutar programmet.
            print("\nTack för denna gång!")
            break

        #========================================
        #       FELAKTIGT VAL
        #========================================

        else:

            # Hanterar ett menyval som inte är giltigt.
            print("\nFelaktigt val.")
            print("Välj en siffra mellan 1 och 4.")


#========================================
#       STARTA PROGRAMMET
#========================================

# Startar programmets huvudmeny.

user_ui()


#========================================
#       UTVECKLINGSPLAN
#========================================

# 1. Profil
#    ├── Jobb
#    ├── Plats
#    └── Kompetenser
#
# 2. API
#    └── Hämta aktuella jobbannonser
#
# 3. Matchning
#    ├── Matcha jobb
#    ├── Matcha plats
#    └── Matcha kompetenser
#
# 4. Resultat
#    └── Visa jobb och matchningspoäng
#
# 5. Förbättringar
#    ├── Validering
#    ├── Historik
#    └── Bättre användargränssnitt
#
# 6. Testning
#    └── Testa och färdigställ programmet
