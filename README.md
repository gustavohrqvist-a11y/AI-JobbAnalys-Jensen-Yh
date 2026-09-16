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
De 5 vanligaste teknologierna var:


## Analys
Resultatet visar att Python är dominerande för AI-roller i Sverige. Molnkompetens (AWS) och containerisering (Docker) är också viktigt.

## Reflektion
Det svåraste var att hantera API:ns rate limits. Nästa gång skulle jag lägga till caching för att minska antalet anrop.

## GitHub-länk
https://github.com/mittanvandare/jobbannons-analys