# AI-JobbAnalys-Jensen-Yh


## Mål
Matcha en användare med ett jobb för att underlätta att hitta jobb som man är behörig till.

## Metod
1. Hämta in rådata från användaren för att skapa en profil.
2. Anroppa Jobbtech Api och hämta jobbannonser.
3. Api informationen sparas sedan i jobbdata.json.
4. Jämnför användarens input data med jobbannonserna och bestäm ifall någon data matchar.
5. För varje match per matchningskreterie (Jobb, Plats, Kompetens) så tilldelas poäng. 
6. Matchningarna rangordnas sedan och visar vilket jobb som är den bästa matchningen.
7. Matchningarna sparas sedan i historik.json med datum och tid.

## Resultat
  Resultatet av mitt arbete är ett grundprogram. Användare får skapa en profil där hen lägger in olika kriterier på vad och vart hen vill jobba med. Användare kan också skriva in kompetenser som hen har.

   Programmet anroppar sedan jobbtech API, för att kontrollera vad för jobb annonser som finns. Programet jämnför sedan dem befintliga jobb anonserna med användarens input för varje match tilldelas poäng Programmet returnerar sedan matchningar med länk till jobb annonsen. 


## Analys


## Reflektion
Det svåraste var att hantera API:ns rate limits. Nästa gång skulle jag lägga till caching för att minska antalet anrop.

## GitHub-länk
https://github.com/gustavohrqvist-a11y/AI-JobbAnalys-Jensen-Yh