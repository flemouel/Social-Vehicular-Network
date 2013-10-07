#permet de traiter les donnees sur le voyage des vehicules via le fichier maptripinfoWO.out.xml
#Sans reroutage:
echo Resultats sans reroutage
ipython -i summaryWO.py
#permet de traiter les donnees sur le voyage des vehicules via le fichier maptripinfo.out.xml
#Avec reroutage global:
echo Resultats avec reroutage global
ipython -i summary.py
#permet de traiter les donnees sur le voyage des vehicules via le fichier maptripinfoLocal.out.xml
#Avec reroutage global:
echo Resultats avec reroutage Local
ipython -i summaryLocal.py
