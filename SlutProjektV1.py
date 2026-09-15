#========================================
#       VÄLKOMMEN TILL AI-JOBBANALYS
#========================================

#Mål: Förenkla och effektivisera moment för att hitta jobb som passar in på vissa kriterier och profiler.

#========================================
#       API & Förvaring av input.
#========================================

förvalda_jobb = [] #tom lista där användarens input sparas

förvald_plats = []#tom lista där användarens input sparas

historik_jobb_plats = [
]

arbetsmarknad = [ # Denna lista aggerar API tills jag har importerat Bilbliotek.
{"jobb": "pilot", "plats": "stockholm,", "erfarenhet": "2"},
{"jobb": "pilot", "plats": "göteborg", "erfarenhet": "2"},
{"jobb": "systemutvecklare", "plats": "stockholm", "erfarenhet": "60"},
{"jobb": "systemutvecklare", "plats": "malmö", "erfarenhet": "5"},
{"jobb": "djurskötare", "plats": "uppsala", "erfarenhet": "0"},
]


#========================================
#       HuvudFunktioner
#========================================

def user_ui():
# Programmets huvudmeny

    while True:

        print("\n")#--------------------------------------
        print("=" * 40)                                  #\
        print("       VÄLKOMMEN TILL AI-JOBBANALYS")      #\
        print("=" * 40)                                    #\
        print("1. Sök jobb")                                # Denna funktion är själva UI för användaren / Användar menyn.
        print("2. Kontrollera vad som efterfrågas")        #/
        print("3. Historik")                             #/
        print("4. Avsluta")                            #/
        print("=" * 40) #-------------------------------

        svar = input("Välj ett alternativ 1-4: ").strip()

        # Om användaren väljer 1 startas jobbsökningen
        if svar == "1":
            inmatning_jobb() 
            inmatning_plats()
            

        # Om användaren väljer 2 visas alla jobb i "API-källan"
        elif svar == "2":
            #visa_alla_jobben()
            print("underutveckling")

        # Om användaren väljer 3 visas historiken
        elif svar == "3":
            #visa_historik()
            print("underutveckling")
            print(f"Din Historik Visar: \n {historik_jobb_plats}")
        # Om användaren väljer 4 avslutas programmet
        elif svar == "4":
            print("\nTack för denna gång!")
            break

        # Om användaren skriver något annat än 1-4
        else:
            print("\nFelaktigt val.")
            print("Välj en siffra mellan 1 och 4.")

#========================================
#       Stödfunktioner
#========================================

def inmatning_jobb():
    print("\n")
    print("=" * 40)
    print(f"Svara på följande frågor")
    print("=" * 40)
    while True:
        alternativ = input("Vilka roller söker du?").lower().split()

        förvalda_jobb.extend(alternativ) # Jag väljer att använda extend istället för append för att allt ska hamna inom samma lista. Om användaren tex skriver X y sparar och sedan vill välja fler jobb så hamnar det i samma lista.

        historik_jobb_plats.append(förvalda_jobb)

        fortsätt = input("vill du söka fler roller y/n ").lower()

        if fortsätt == "y":

            continue

        elif fortsätt == "n":

            print(f"Okej du har valt följande \n {förvalda_jobb}")

            break
        else:

            print(f"Svara endast med y eller n")

#==========================================================================

def inmatning_plats():
    print("\n")
    print("=" * 40)
    print(f"Nästa fråga")
    print("=" * 40)
    while True:

        alternativ = input("I vilken ort vill du söka? ").lower().split()

        förvald_plats.extend(alternativ)

        historik_jobb_plats.append(förvald_plats)

        fortsätt = input("vill du välja fler orter y/n ")

        if fortsätt == "y":

            continue

        elif fortsätt == "n":

            print(f"Okej du har valt följande \n {förvald_plats}")

            break

        else:

            print(f"Svara endast med y eller n")




#========================================
#       Validering
#========================================

user_ui()
