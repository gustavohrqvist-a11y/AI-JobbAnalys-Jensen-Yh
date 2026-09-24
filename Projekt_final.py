#========================================
#       AI JOBBMATCHNING V6
#========================================
# Mål: Matcha användarens profil mot jobbannonser
# och visa vilka jobb som passar bäst.
#========================================


#========================================
#       IMPORTER
#========================================

import requests                  # Används för att skicka HTTP-anrop till API:t.
import json                      # Används för att läsa och spara JSON-filer.
from datetime import datetime    # Används för att spara datum och tid.


#========================================
#       HJÄLPMETODER
#========================================

def normalisera(text):                           # Funktion som gör text enklare att jämföra.
    return text.lower().strip()                  # Gör texten till små bokstäver och tar bort mellanslag.


def visa_kompetenser(kompetenser):               # Tar emot en lista med kompetenser.
    return ", ".join(kompetenser) if kompetenser else "Inga"  # Gör listan till text eller visar "Inga".


#========================================
#       KLASSER
#========================================

#====================
# Inhämtning av data                             #Inhämtning av data från användaren.
#====================
class MatchningsData:                            # Basklass för gemensam information.

    def __init__(self):                           # Körs när ett objekt skapas.
        self.plats = []                           # Lista för platser.
        self.kompetenser = []                     # Lista för kompetenser.


class Profil(MatchningsData):                    # Profil ärver plats och kompetenser från basklassen.

    def __init__(self):
        super().__init__()                        # Kör basklassens __init__ och skapar plats/kompetenser.
        self.jobb = []                            # Lista över jobb användaren vill ha.


    def input_jobb(self):                         # Hämtar användarens önskade jobb.
        self._input("Vad hade du velat jobba som? ", "jobb")  # Anropar den gemensamma inmatningsfunktionen.


    def input_plats(self):                        # Hämtar önskade arbetsplatser.
        self._input("Vart hade du velat jobba? ", "plats")  # Anropar samma funktion för plats.


    def input_kompetenser(self):                  # Hämtar användarens kompetenser.
        self._input("Vad har du för kompetenser? ", "kompetenser")  # Anropar samma funktion för kompetenser.


    def _input(self, text, attribut):             # Gemensam funktion för all användarinmatning.

        print("\n" + "=" * 40)                    # Skriver ut en avgränsare.

        try:
            värden = [                              # Skapar en lista med användarens svar.
                normalisera(x)                      # Normaliserar varje värde.
                for x in input(text).split(",")    # Delar upp svaret vid kommatecken.
                if x.strip()                        # Tar bara med värden som inte är tomma.
            ]
            getattr(self, attribut).extend(värden) # Hittar rätt lista och lägger till värdena.

        except (KeyboardInterrupt, EOFError):      # Fångar Ctrl+C och avslutad inmatning.
            print("\nInmatningen avbröts.")


#====================
# MATCHARE                                        # Matchare är ansvarig för att jämföra profil mot jobbannonser och räkna ut poäng.
#====================

class Jobbannons(MatchningsData):                 # Klass som representerar en jobbannons.

    def __init__(self, jobb, plats, kompetenser, länk):
        super().__init__()                         # Hämtar plats och kompetenser från basklassen.
        self.jobb = jobb                           # Sparar jobbets titel.
        self.plats = plats                         # Sparar jobbets plats.
        self.kompetenser = kompetenser             # Sparar matchande kompetenser.
        self.länk = länk                           # Sparar länken till annonsen.


class Matchare:                                   # Ansvarar för att matcha profil mot jobb.

    def __init__(self, profil, arbetsmarknad):
        self.profil = profil                       # Sparar användarens profil.
        self.arbetsmarknad = arbetsmarknad         # Sparar alla jobbannonser.


    def match(self):                               # Räknar ut matchningspoäng.

        matchningar = []                           # Lista där godkända matchningar sparas.

        for jobb in self.arbetsmarknad:            # Går igenom varje jobbannons.

            jobb_matchar = False                   # Börjar med att anta att jobbet inte matchar.

            for önskat_jobb in self.profil.jobb:   # Går igenom användarens önskade jobb.
                if önskat_jobb in jobb.jobb:       # Kontrollerar om önskat jobb finns i jobbtiteln.
                    jobb_matchar = True            # Jobbet har rätt titel.
                    break                           # Slutar kontrollera fler jobbtitlar.

            if not jobb_matchar:                   # Om titeln inte matchade...
                continue                            # ...hoppa över jobbet.

            poäng = 0                              # Börjar matchningen med 0 poäng.

            for plats in self.profil.plats:        # Går igenom användarens önskade platser.
                if plats in jobb.plats:            # Kontrollerar om platsen matchar.
                    poäng += 2                      # Rätt plats ger 2 poäng.
                    break                           # En platsmatch räcker.

            for kompetens in self.profil.kompetenser:  # Går igenom användarens kompetenser.
                if kompetens in jobb.kompetenser:      # Kontrollerar om kompetensen finns i jobbet.
                    poäng += 1                          # Varje kompetens ger 1 poäng.

            if poäng == 0:                          # Om titel matchade men inget annat gjorde det...
                poäng = 1                            # ...får jobbet ändå 1 poäng.

            matchningar.append((jobb, poäng))        # Sparar jobbet tillsammans med poängen i en tuple.

        matchningar.sort(                             # Sorterar matchningarna.
            key=lambda x: x[1],                     # Använder poängen som sorteringsvärde.
            reverse=True                             # Högsta poängen hamnar först.
        )

        return matchningar                            # Returnerar den färdiga listan.


#========================================
#       API-FUNKTION
#========================================

def hämta_jobb_från_api(profil):                         # Skapar funktionen som hämtar jobb från API:t.
    if not profil.jobb:                                  # Kontrollerar om användaren har valt något jobb.
        print("Du måste ställa in din profil först.")    # Informerar användaren att profilen måste fyllas i.
        return []                                        # Returnerar en tom lista när ingen profil finns.

    url = "https://jobsearch.api.jobtechdev.se/search"   # Sparar adressen till JobTechs API.
    jobbannonser = []                                    # Skapar en lista för jobbannonser.
    alla_data = []                                       # Skapar en lista för rådata från API:t.

    try:                                                 # Försöker köra kod som kan ge ett fel.
        for sökord in profil.jobb:                       # Söker efter varje önskat jobb.
            print(f"\nSöker efter: {sökord}")            # Visar vilket sökord som används.

            response = requests.get(                    # Skickar ett GET-anrop till API:t.
                url,                                    # Anger API-adressen som ska anropas.
                params={"q": sökord, "limit": 10},       # Skickar sökord och begränsar resultatet till tio annonser.
                timeout=10                               # Avbryter anropet om API:t inte svarar inom tio sekunder.
            )                                           # Kodrad som används för programmets funktion.

            print("Statuskod:", response.status_code)   # Visar HTTP-statuskoden från API:t.

            if response.status_code != 200:              # Kontrollerar om API-anropet lyckades.
                print("Kunde inte hämta jobbannonser.")  # Informerar om att annonserna inte kunde hämtas.
                continue                                 # Hoppar vidare till nästa jobb.

            data = response.json()                       # Omvandlar API-svaret från JSON till Python-data.
            alla_data.append(data)                       # Sparar API-svaret i listan med rådata.

            träffar = data.get("hits", [])               # Hämtar jobbträffarna från API-svaret.
            print("Antal träffar:", len(träffar))        # Visar antalet hittade jobb.

            for jobb in träffar:                         # Går igenom varje hittad jobbannons.
                titel = normalisera(jobb.get("headline") or "")  # Hämtar och normaliserar jobbets titel.

                adress = jobb.get("workplace_address") or {}     # Hämtar arbetsplatsens adress eller en tom dictionary.
                plats = normalisera(adress.get("municipality") or "") # Hämtar kommunen eller använder tom text.

                länk = jobb.get("webpage_url") or ""     # Hämtar länken till jobbannonsen.

                beskrivning = jobb.get("description") or {}       # Hämtar beskrivningsobjektet.
                beskrivning = normalisera(beskrivning.get("text") or "") # Hämtar beskrivningens text eller tom text.

                matchade_kompetenser = []                # Skapar en lista för kompetenser som matchar.

                for kompetens in profil.kompetenser:     # Går igenom användarens kompetenser.
                    if kompetens in beskrivning:         # Kontrollerar om kompetensen finns i beskrivningen.
                        matchade_kompetenser.append(kompetens)  # Lägger till den matchande kompetensen.

                jobbannonser.append(                     # Lägger till en ny jobbannons i listan.
                    Jobbannons(titel, plats, matchade_kompetenser, länk) # Skapar ett Jobbannons-objekt.
                )

        try:                                             # Försöker köra kod som kan ge ett fel.
            with open("jobbdata.json", "w", encoding="utf-8") as f: # Öppnar en fil.
                json.dump(alla_data, f, ensure_ascii=False, indent=4) # Skriver Python-data till JSON-format.

        except OSError as fel:                            # Fångar fel vid filhantering.
            print("\nKunde inte spara jobbdata.")         # Informerar om att jobbdata inte kunde sparas.
            print(fel)                                   # Visar felmeddelandet.

        return jobbannonser                               # Returnerar de hämtade jobbannonserna.

    except requests.exceptions.RequestException as fel:  # Fångar nätverksfel från requests.
        print("\nEtt fel uppstod när API:t kontaktades.") # Informerar om API-felet.
        print(fel)                                       # Visar felmeddelandet.
        return []                                        # Returnerar en tom lista.

    except json.JSONDecodeError:                         # Fångar felaktig JSON-data.
        print("\nKunde inte läsa svaret från API:t.")    # Informerar om att API-svaret inte kunde läsas.
        return []                                        # Returnerar en tom lista.


        #========================================
        #       SPARA API-DATA
        #========================================

        try:
            with open(                             # Öppnar filen för skrivning.
                "jobbdata.json",                   # Filen som ska sparas.
                "w",                               # "w" betyder skrivläge.
                encoding="utf-8"                   # Gör att svenska tecken fungerar.
            ) as f:
                json.dump(                          # Skriver Python-data som JSON.
                    alla_data,                      # Data som ska sparas.
                    f,                              # Filen som datan skrivs till.
                    ensure_ascii=False,             # Behåller svenska tecken.
                    indent=4                        # Gör JSON-filen lättare att läsa.
                )

        except OSError as fel:                     # Fångar fel vid filskrivning.
            print("\nKunde inte spara jobbdata.")
            print(fel)

        return jobbannonser                         # Returnerar alla skapade jobbannonser.

    except requests.exceptions.RequestException as fel:  # Fångar nätverksfel.
        print("\nEtt fel uppstod när API:t kontaktades.")
        print(fel)
        return []

    except json.JSONDecodeError:                   # Fångar felaktig JSON från API:t.
        print("\nKunde inte läsa svaret från API:t.")
        return []


#========================================
#       HISTORIK
#========================================

def spara_historik(profil, matchningar):           # Sparar en sökning i historiken.

    try:
        with open(                                  # Öppnar historikfilen. / stänger filen automatiskt när vi är klara.
            "historik.json",                        # Filens namn.
            "r",                                    # "r" betyder läsläge.
            encoding="utf-8"
        ) as f:                                     # Här ger vi den öppnade filen namnet: f
            historik = json.load(f)                 # Läser JSON och gör om till Python-data.

    except (FileNotFoundError, json.JSONDecodeError):  # Om filen saknas eller är trasig.
        historik = []                               # Börjar då med en tom historik.


    ny_sökning = {                                  # Skapar en ny historikpost.
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M"),  # Sparar aktuellt datum och tid.
        "profil": {                                 # Sparar användarens profil.
            "jobb": profil.jobb,
            "plats": profil.plats,
            "kompetenser": profil.kompetenser
        },
        "matchningar": []                           # Här kommer matchande jobb sparas.
    }


    for jobb, poäng in matchningar:                 # Går igenom alla matchningar.
        ny_sökning["matchningar"].append({          # Lägger till varje jobb i historiken.
            "jobb": jobb.jobb,
            "plats": jobb.plats,
            "poäng": poäng,
            "kompetenser": jobb.kompetenser,
            "länk": jobb.länk
        })

    historik.append(ny_sökning)                     # Lägger den nya sökningen sist i historiken.


    try:
        with open(                                  # Öppnar historikfilen för skrivning. / Stänger filen automatiskt när vi är klara.
            "historik.json",                        #filen som ska sparas.
            "w",                                    #Write läge / Skrivläge
            encoding="utf-8"                        #tilåtter svenskt alfabete och tecken
        ) as f:                                     #Här ger vi den öppnade filen namnet f
            json.dump(                              # Sparar hela historiken som JSON.
                historik,
                f,
                ensure_ascii=False,
                indent=4
            )

    except OSError as fel:                          # Fångar fel när filen ska sparas.
        print("\nKunde inte spara historiken.")
        print(fel)
        return

    print("\nSökningen har sparats i historiken.")


def visa_historik():                                # Visar sparade sökningar.

    try:
        with open(                                  # Öppnar historikfilen.
            "historik.json",
            "r",
            encoding="utf-8"
        ) as f:
            historik = json.load(f)                 # Läser in historiken.

    except FileNotFoundError:                       # Om historikfilen inte finns.
        print("\nDet finns ingen historik ännu.")
        return

    except json.JSONDecodeError:                    # Om JSON-filen är felaktig.
        print("\nHistorikfilen kunde inte läsas.")
        return

    if not historik:                                # Kontrollerar om listan är tom.
        print("\nDet finns ingen historik ännu.")
        return

    print("\n" + "=" * 40)
    print("              HISTORIK")
    print("=" * 40)

    for nummer, sökning in enumerate(historik, 1):  # Går igenom historiken med löpnummer.

        print(f"\nSökning {nummer}")
        print(f"Datum: {sökning['datum']}")
        print(f"Jobb: {', '.join(sökning['profil']['jobb'])}")  # Gör jobblistan till text.
        print(f"Plats: {', '.join(sökning['profil']['plats'])}")  # Gör platslistan till text.
        print(f"Kompetenser: {', '.join(sökning['profil']['kompetenser'])}")  # Gör kompetenslistan till text.

        print("\nMatchningar:")

        for jobb in sökning["matchningar"]:         # Går igenom alla jobb i sökningen.

            print(f"  - {jobb['jobb']}")
            print(f"    Plats: {jobb['plats']}")
            print(f"    Poäng: {jobb['poäng']}")
            print("    Matchande kompetenser: " + visa_kompetenser(jobb["kompetenser"]))
            print(f"    Länk: {jobb['länk']}")

        print("-" * 40)


#========================================
#       VISA MATCHNINGAR
#========================================

def visa_matchningar(profil):                       # Hämtar, matchar och visar jobb.

    print("\nHämtar aktuella jobbannonser...")

    jobb_fran_api = hämta_jobb_från_api(profil)      # Hämtar jobb från API:t.

    if not jobb_fran_api:                            # Om inga jobb hämtades.
        print("Inga jobbannonser kunde hämtas.")
        return

    matchningar = Matchare(                         # Skapar en Matchare.
        profil,                                      # Skickar in användarens profil.
        jobb_fran_api                                 # Skickar in hämtade jobb.
    ).match()                                        # Kör matchningsfunktionen direkt.

    if not matchningar:                              # Om inga jobb matchade.
        print("\nInga jobb matchade din profil.")
        return

    spara_historik(profil, matchningar)              # Sparar resultatet.

    print("\n" + "=" * 40)
    print("           DINA MATCHNINGAR")
    print("=" * 40)

    for jobb, poäng in matchningar:                  # Går igenom matchningarna i poängordning.

        print(f"\n- {jobb.jobb}")
        print(f"  Plats: {jobb.plats}")
        print(f"  Poäng: {poäng}")
        print("  Matchande kompetenser: " + visa_kompetenser(jobb.kompetenser))
        print(f"  Länk: {jobb.länk}")


#========================================
#       ANVÄNDARGRÄNSSNITT
#========================================

profil = Profil()                                    # Skapar programmets profil.


def user_ui():                                       # Programmets huvudmeny.

    while True:                                      # Kör menyn tills användaren avslutar.

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
            svar = input("Välj ett alternativ 1-4: ") # Hämtar användarens menyval.

        except (KeyboardInterrupt, EOFError):        # Fångar avbruten inmatning.
            print("\nProgrammet avslutas.")
            break


        #========================================
        #       PROFIL
        #========================================

        if svar == "1":                              # Användaren väljer profil.

            profil.input_jobb()                      # Hämtar önskade jobb.
            profil.input_plats()                     # Hämtar önskade platser.
            profil.input_kompetenser()               # Hämtar kompetenser.

            print("\nProfil ändrad!")
            print(f"\nJobb: {profil.jobb}")
            print(f"Plats/Ort: {profil.plats}")
            print(f"Kompetenser: {profil.kompetenser}")


        #========================================
        #       MATCHNINGAR
        #========================================

        elif svar == "2":                            # Användaren väljer matchningar.
            visa_matchningar(profil)                 # Hämtar och visar matchande jobb.


        #========================================
        #       HISTORIK
        #========================================

        elif svar == "3":                            # Användaren väljer historik.
            visa_historik()                          # Visar tidigare sökningar.


        #========================================
        #       AVSLUTA
        #========================================

        elif svar == "4":                            # Användaren väljer att avsluta.
            print("\nTack för denna gång!")
            break                                    # Avslutar while-loopen.


        #========================================
        #       FELAKTIGT VAL
        #========================================

        else:                                        # Körs om valet inte är 1–4.
            print("\nFelaktigt val.")
            print("Välj en siffra mellan 1 och 4.")


#========================================
#       STARTA PROGRAMMET
#========================================

user_ui()                                            # Startar programmets huvudmeny.

