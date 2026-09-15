#========================================
#       AI JOBBMATCHNING V5
#========================================
# Mål: Matcha användarens profil mot jobbannonser
# och visa vilka jobb som passar bäst.
#========================================


#========================================
#       KLASSER & Metoder
#========================================

class MatchningsData:
    def __init__(self):
        self.plats = []
        self.kompetenser = []



class Profil(MatchningsData):
    def __init__(self):
        super().__init__()
        self.jobb = []

    def input_jobb(self):
        print("\n")
        print("=" * 40)
        jobb_input = input("Vad hade du velat jobba som? ").strip().lower().split()
        self.jobb.extend(jobb_input)


    def input_plats(self):
        print("\n")
        print("=" * 40)
        plats_input = input("Vart hade du velat Jobba? ").strip().lower().split()
        self.plats.extend(plats_input)


    def input_kompetenser(self): #Metoden låter användaren skriva in kompetenser och sedan lägger dem i self.kompetenser
        print("\n")
        print("=" * 40)
        kompetens_input = input("Vad har du för kompetenser? ").strip().lower().split()
        self.kompetenser.extend(kompetens_input)



class Jobbannons(MatchningsData):
    def __init__(self, jobb, plats, kompetenser):
        super().__init__()
        self.jobb = jobb
        self.plats = plats
        self.kompetenser = kompetenser


arbetsmarknad = [
    Jobbannons("pilot", "stockholm", "pilot utbildning"),
    Jobbannons("pilot", "göteborg", "pilot utbildning"),
    Jobbannons("systemutvecklare", "stockholm", "python"),
    Jobbannons("systemutvecklare", "malmö", "python"),
    Jobbannons("djurskötare", "uppsala", "djursjukvård")
]


class Matchare:
    def __init__(self, profil):
        self.profil = profil

    def match(self):
        matchningar = []

        for jobb in arbetsmarknad:
            if jobb.jobb in self.profil.jobb and jobb.plats in self.profil.plats:
                matchningar.append(jobb)

        return matchningar











# Användarens profil



#========================================_
#       API & FÖRVARING AV DATA
#========================================

profil = Profil()


#========================================
#       HUVUDFUNKTIONER
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
        print("3. Kontrollera Matchningar")
        print("4. Historik")
        print("5. Avsluta")
        print("=" * 40)

        svar = input("Välj ett alternativ 1-5: ")

        # Användaren ställer in sin profil.
        if svar == "1":

            profil.input_jobb()
            profil.input_plats()
            profil.input_kompetenser()
            print("Profil ändrad")
            print (f" Din profil ser ut såhär, Jobb{profil.jobb} \n Plats/Ort: {profil.plats} \n Kompetenser {profil.kompetenser}")
        # Visar jobb som matchar profilen.

        elif svar == "2":

            matchare = Matchare(profil)

            matchningar = matchare.match()

            print("\nDina matchningar")

            for jobb in matchningar:

                print(f"- {jobb.jobb} i {jobb.plats}")



        # Kontroll av matchningar.
        elif svar == "3":
            print("Placeholder")

        # Visar tidigare sökningar.
        elif svar == "4":

            print("Placeholder")


        # Avslutar programmet.
        elif svar == "5":

            print("\nTack för denna gång!")
            break

        else:

            print("\nFelaktigt val.")
            print("Välj en siffra mellan 1 och 5.")


#========================================
#       STÖDFUNKTIONER
#========================================


#========================================


#========================================



#========================================
#       MATCHNING
#========================================





#========================================
#       STARTA PROGRAMMET
#========================================

# Startar programmet.

user_ui()



#1. Profil
 #  ├── input_jobb()
 #  ├── input_plats()
#   └── input_Kompetenser
#             ↓
#2. Testa att profilen sparar rätt information # det gör den
#             ↓
#3. Gör menyval 1 färdigt #färigt
#             ↓
#4. Skapa några enkla jobbannonser för test
#             ↓
#5. Bygg matchningen
#             ↓
#6. Visa matchningsresultatet
#             ↓
#7. Lägg till historik
#             ↓
#8. Validering
#             ↓
#9. API