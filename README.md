<<<<<<< Updated upstream
# AI-JobbAnalys-Jensen-Yh
=======
# AI-JobbAnalys-Jensen-Yh


## Mål
Matcha användarens profil mot jobbannonser och visa vilka jobb som passar bäst.

## Metod
1. Hämta in rådata från användaren för att skapa en profil.
2. Anroppa Jobbtech Api och hämta jobbannonser.
3. Api informationen sparas sedan i jobbdata.json.
4. Jämnför användarens input data med jobbannonserna och bestäm ifall någon data matchar.
5. För varje match per matchningskreterie (Jobb, Plats, Kompetens) så tilldelas poäng. 
6. Matchningarna rangordnas sedan och visar vilket jobb som är den bästa matchningen.
7. Matchningarna sparas sedan i historik.json med datum och tid.

## Resultat
  Resultatet av mitt arbete är ett grundprogram. Användare får skapa en profil där hen lägger in olika kriterier på vad och vart hen vill jobba med. Användare kan också skriva in kompetenser som hen har. Programmet anroppar sedan jobbtech API, för att kontrollera vad för jobb annonser som finns. Programet jämnför sedan dem befintliga jobb anonserna med användarens input för varje match tilldelas poäng Programmet returnerar sedan matchningar med länk till jobb annonsen. 


## Analys
Resultatet visar att mitt program kan matcha användaren med jobbannonser snabbare. Detta sker genom att programemt jämnför API med användarens input. Genom att använda yrkesroll plats och kompetens har jag lyckats att skapa ett matchnings system som visar liknande jobb fast i annan ort. Dock om titeln (Rollens namn) inte matchar så kommer det att exkluderas. Jag har valt att använda detta upplägg eftersom att många är benägna att flytta dit jobben finns. Man kan också utöka eller utveckla sin egen kompetens. Det är dock svårt att påverka ett företags geografiska placering. 

En Begränsning jag har identifierat är att programmet använder specefika sökord för att hitta matchningar, det innebär att man inte kan skriva med fritext tex(Jag har varit lärare i 20 år). Detta gör att programmet kan missa en matchning pga att annonsen är formulerad på ett annat sätt.

## Reflektion
Under arbetet med mitt projekt har jag fått en större förståelse för python men också hur annorlunda man anänder python i näringslivet. Jag har lärt mig att använda mig av OOP och API. Med hjälp av OOP har jag använt klasser och arv för att återanvädna kod och inte behöva skriva en sak flera gånger. Med API kan jag hämta in riktiga jobbannonser och använda dem för att matcha en användare med olika annonser. 

Jag har även fått en större förståelse för felhantering genom try / Except, när programmet kommunicerar med api kan problem uppstå som inte programmet han någon kontroll över tex timeout(tar för lång tid för api att svara). Jag har valt att skapa ett enkelt poängbaserad matchningssystem. Detat system kan ej läsa fritext utan anvädner sig av sökord för att hitta matchnignar. Jag hade velat utveckla en mer avancerad lösning som hade kunnat läsa fritext och på så sätt inte gå miste om matchningar.
## GitHub-länk
https://github.com/gustavohrqvist-a11y/AI-JobbAnalys-Jensen-Yh
>>>>>>> Stashed changes
