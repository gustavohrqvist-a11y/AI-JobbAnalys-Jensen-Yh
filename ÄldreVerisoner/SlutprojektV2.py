#========================================
#       VÄLKOMMEN TILL AI-JOBBANALYS
#========================================

#Mål: Förenkla och effektivisera moment för att hitta jobb som passar in på vissa kriterier och profiler.

#========================================
#       API & Förvaring av input.
#========================================

#förvalda_jobb = [] # Tom lista där användarens input sparas.#

#förvald_plats = [] # Tom lista där användarens input sparas.#

användare = { #istället för att använda flera olika listor kan man kombinera dem i en dictonary för att spara tillhörande info på samma plats.

"jobb":[],
"plats":[],
"erfarenhet": {}


}

historik_jobb_plats = [] # Lista där användarens tidigare val sparas.

arbetsmarknad = [ # Denna lista aggerar API tills jag har importerat Bilbliotek.
{"jobb": "pilot", "plats": "stockholm,", "erfarenhet": 2},
{"jobb": "pilot", "plats": "göteborg", "erfarenhet": 2},
{"jobb": "systemutvecklare", "plats": "stockholm", "erfarenhet": 60},
{"jobb": "systemutvecklare", "plats": "malmö", "erfarenhet": 5},
{"jobb": "djurskötare", "plats": "uppsala", "erfarenhet": 0},
]


#========================================
#       HuvudFunktioner
#========================================

def user_ui():
# Programmets huvudmeny / användargränssnitt.
# Här väljer användaren vad programmet ska göra.

    while True:

        print("\n")#--------------------------------------
        print("=" * 40)                                  #\
        print("       VÄLKOMMEN TILL AI-JOBBANALYS")      #\
        print("=" * 40)                                    #\
        print("1. Sök jobb")                                # Denna funktion är själva UI för användaren / Användar menyn.
        print("2. Kontrollera vad som efterfrågas")         #/
        print("3. Historik")                              #/
        print("4. Avsluta")                             #/
        print("=" * 40) #-------------------------------

        svar = input("Välj ett alternativ 1-4: ").strip()

        # Om användaren väljer 1 startas jobbsökningen
        if svar == "1":
            inmatning_jobb(användare) 
            inmatning_plats(användare)
            inmatning_erfarenhet(användare)
            # Användaren anger vilka jobb och platser som ska sökas.

        # Om användaren väljer 2 visas alla jobb i "API-källan"
        elif svar == "2":
            #visa_alla_jobben()
            print("underutveckling")
            # Denna funktion ska senare visa/analysera vilka jobb som efterfrågas.

        # Om användaren väljer 3 visas historiken
        elif svar == "3":
            #visa_historik()
            print("underutveckling")
            if historik_jobb_plats == []:
                print("Det finns ingen historik just nu")
            else:
                print(f"Du har valt: \n {användare['jobb']}")

            # Visar användarens tidigare val och sökningar.

        # Om användaren väljer 4 avslutas programmet
        elif svar == "4":
            print("\nTack för denna gång!")
            break
            # Avslutar programmet.

        # Om användaren skriver något annat än 1-4
        else:
            print("\nFelaktigt val.")
            print("Välj en siffra mellan 1 och 4.")
            # Kontrollerar att användaren väljer ett giltigt alternativ.


#========================================
#       Stödfunktioner
#========================================

def inmatning_jobb(användare):
# Användaren anger vilka jobbroller som personen vill söka.

    print("\n")
    print("=" * 40)
    print(f"Svara på följande frågor")
    print("=" * 40)

    while True:
        alternativ = input("Vilka roller söker du?").lower().split()

        användare["jobb"].extend(alternativ) # Jag väljer att använda extend istället för append för att allt ska hamna inom samma lista. Om användaren tex skriver X y sparar och sedan vill välja fler jobb så hamnar det i samma lista.

        #historik_jobb_plats.append(förvalda_jobb)
        # Sparar användarens valda jobb i historiken.

        fortsätt = input("vill du söka fler roller y/n ").lower()

        if fortsätt == "y":

            continue
            # Användaren kan fortsätta lägga till fler jobbroller.

        elif fortsätt == "n":

            print(f"Du har valt: \n {användare['jobb']}")

            break
            # Avslutar inmatningen när användaren är klar.

        else:

            print(f"Svara endast med y eller n")
            # Kontrollerar att användaren svarar med ett giltigt alternativ.


#==========================================================================

def inmatning_plats(användare):
# Användaren anger vilka orter personen vill söka jobb i.

    print("\n")
    print("=" * 40)
    print(f"Nästa fråga")
    print("=" * 40)
    while True:

        alternativ = input("I vilken ort vill du söka? ").lower().split()

        
        användare["plats"].extend(alternativ)
        # Sparar användarens valda platser i listan.

        #historik_jobb_plats.extend(förvald_plats)
        # Sparar användarens valda platser i historiken.

        fortsätt = input("vill du välja fler orter y/n ")

        if fortsätt == "y":

            continue
            # Användaren kan fortsätta lägga till fler orter.

        elif fortsätt == "n":

            print(f"Din Historik Visar: \n {användare["plats"]}")

            break
            # Avslutar inmatningen när användaren är klar.

        else:

            print(f"Svara endast med y eller n")
            # Kontrollerar att användaren svarar med ett giltigt alternativ.

#==========================================================================

def inmatning_erfarenhet(användare):
#Låter användare berätta hur många års erfarenhet som han har.

    print("\n")
    print("=" * 40)
    print(f"Nästa fråga")
    print("=" * 40)

    for jobb in användare["jobb"]:
        svar = int(input(f"Hur många års erfarenhet har du av {jobb}? \n"))
        användare["erfarenhet"][jobb] = svar
        print(f"{användare["erfarenhet"]}")

    #print(f"Du har valt följande {jobb}{erfarenhet}")




#========================================
#       Validering
#========================================

# VALIDERING
# Här ska informationen från jobbannonserna kontrolleras.
# Exempelvis erfarenhet, lön, plats, tekniker, dubbletter
# och saknade värden ska kontrolleras innan matchningen.


user_ui()
# Startar programmet genom att köra huvudfunktionen.