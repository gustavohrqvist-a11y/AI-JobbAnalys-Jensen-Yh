## AI-JobbAnalys-Jensen-Yh
## Mål
Matcha användarens profil mot jobbannonser och visa vilka jobb som passar bäst.

## Metod
Hämta in rådata från användaren för att skapa en profil.

Anropa JobTech API och hämta jobbannonser.

API-informationen sparas sedan i jobbdata.json.

Jämför användarens indata med jobbannonserna och bestäm ifall någon data matchar.

För varje matchning per matchningskriterium (jobb, plats, kompetens) tilldelas poäng.

Matchningarna rangordnas sedan och visar vilket jobb som är den bästa matchningen.

Matchningarna sparas sedan i historik.json med datum och tid.

## Resultat
Resultatet av mitt arbete är ett grundprogram. Användaren får skapa en profil där hen lägger in olika kriterier för vad och var hen vill jobba. Användaren kan också skriva in kompetenser som hen har. Programmet anropar sedan JobTech API för att kontrollera vilka jobbannonser som finns. Programmet jämför sedan de befintliga jobbannonserna med användarens indata. För varje matchning tilldelas poäng. Programmet returnerar sedan matchningarna med en länk till jobbannonsen.

## Analys
Resultatet visar att mitt program kan matcha användaren med jobbannonser. Detta sker genom att programmet jämför API:t med användarens indata. Genom att använda yrkesroll, plats och kompetens har jag lyckats skapa ett matchningssystem som visar liknande jobb även på andra orter. Om titeln (yrkesrollen) däremot inte matchar kommer jobbet att exkluderas. Jag har valt att använda detta upplägg eftersom många är benägna att flytta dit jobben finns. Man kan också utöka eller utveckla sin egen kompetens. Det är dock svårt att påverka ett företags geografiska placering.

En begränsning jag har identifierat är att programmet använder specifika sökord för att hitta matchningar. Det innebär att man inte kan skriva med fritext, till exempel "Jag har varit lärare i 20 år". Detta gör att programmet kan missa en matchning på grund av att annonsen är formulerad på ett annat sätt.

## Certifikat
Mitt program uppfyller inte kraven för att få något certifikat. Programmet är dock på god väg för följande certifieringar.

PCEP – Certified Entry-Level Python Programmer:
PCEP fokuserar mycket på grundläggande Python-programmering med objektorienterad programmering, användning av API, datahantering med JSON, filhantering och felhantering med try/except.

PCAP – Certified Associate Python Programmer:
PCAP syftar mer på OOP och att använda Python mer avancerat än grundläggande variabler, loopar och if-satser.

PCEI – Certified Entry-Level AI Specialist with Python:
PCEI handlar om AI. Mitt program använder sig inte av AI, men arbetsflödet liknar arbetsflödet för AI. Datainsamling → requests.get() (hämtar information från API i JSON-format) → databearbetning (normalisering) och så vidare.

GDPR - General Data Protection Regulation:
GDPR finns i förstahand för att skydda privatpersoners personliga information. Mitt program uppfyller ej kraven för gdpr eftersom jag blandannat sparar historiken föralltid, detta är något jag hade velat vidareutveckla i framtiden. 

## Reflektion
Under arbetet med mitt projekt har jag fått en större förståelse för Python, men också för hur annorlunda man använder Python i näringslivet. Jag har lärt mig att använda OOP och API. Med hjälp av OOP har jag använt klasser och arv för att återanvända kod och inte behöva skriva samma sak flera gånger. Med API kan jag hämta in riktiga jobbannonser och använda dem för att matcha en användare med olika annonser.

Jag har även fått en större förståelse för felhantering genom try/except. När programmet kommunicerar med API kan problem uppstå som programmet inte har någon kontroll över, till exempel timeout (tar för lång tid för API:t att svara). Jag har valt att skapa ett enkelt, poängbaserat matchningssystem. Detta system kan inte läsa fritext utan använder sig av sökord för att hitta matchningar. Jag hade velat utveckla en mer avancerad lösning som hade kunnat läsa fritext och på så sätt inte gå miste om matchningar.

## GitHub-länk
https://github.com/gustavohrqvist-a11y/AI-JobbAnalys-Jensen-Yh


#========================================
#       UTVECKLINGSPLAN
#========================================

# 1. Profil:
    Jobb, Plats, Kompetenser

# 2. API:
    Hämta aktuella jobbannonser

# 3. Matchning:
    Matcha jobb, plats, kompetenser

# 4. Resultat:
    Visa jobb och matchningspoäng

# 5. Förbättringar:
    Validering, Historik, Bättre UI

# 6. Testning:
    Testa och färdigställ programmet