# Des outils pour de l'analyse de données - en particulier des brevets portants sur les ultrasons 

* CreatePatents.py est un bot piwikimedia pour creer les articles sur le wiki

> python pwb.py CreatePatents

Il sert a créer tous les petites pages des brevets sur le wiki.
A voir sur http://echopen.org/index.php?title=Category:Patents 

* CreateInventors.py est un bot similaire, mais pour les inventeurs, leurs collaborateurs, et leurs travaux

> python pwb.py CreateInventors

Ils se trouvent listés sur http://echopen.org/index.php?title=Category:Inventors&action=edit&redlink=1

* display_patent.php est un petit script pour verifier ce qu'on a dans la DB.
A voir en action sur http://echopen.org/display_patent.php

* graph.py cree le graphe GDF des brevets (liens forward et backward)
A exploiter avec un outil comme Gephi

Avec un dump des données en JSON au cas où!
