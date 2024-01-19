# KingDomino 

Premier prototype d'un programme jouant à KingDomino disponible, mais limité:

```bash
python3 src/main.py
```

Ce programme simule une partie d'un sous-jeu de KingDomino:
- 1 seul joueur
- Pas de système de choix dans la pioche (les dominos arrivent un par un et sans connaissance du prochain)
- Pas de règles avancées tel que "Empire du Milieu" ou "Harmonie"
- Algorithme glouton visant à réduire minimiser le nombre de domaine dans le plateau

## Setup conda env

```bash 
conda env create -f requirement.yml
```
