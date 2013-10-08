#permet de traiter les donnees sur le voyage des vehicules via le fichier maptripinfoWO.out.xml
#Sans reroutage:
echo Resultats sans reroutage
ipython -i summaryWO.py
#permet de traiter les donnees sur le voyage des vehicules via le fichier maptripinfo.out.xml
#Avec reroutage:
echo Resultats avec reroutage ponctuel
ipython -i summary.py

