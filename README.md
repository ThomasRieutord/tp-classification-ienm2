TRAVAUX PRATIQUES DE CLASSIFICATION NON-SUPERVISÉE
==================================================

Bienvenue dans le dépôt qui contient votre TP.
Pour commencer, suivez les instructions de ce README.

Lancement du TP
---------------

Ce dépôt est actuellement sur un serveur, accessible par internet. Il va falloir le récupérer chez vous.
Ouvrez un terminal (l'endroit importe peu) et exécutez les commandes suivantes :
```
git clone https://github.com/ThomasRieutord/tp-classification-ienm2.git
cd tp-classification-ienm2
conda env create -f tpclassif.yml
conda activate tpclassif
cd notebooks
jupyter-notebook sujet.ipynb
```

Déverouillage de la correction
------------------------------
Une fois le TP terminé, la correction se déverrouille avec la commande suivante :
```
gpg correction.ipynb.gpg
```
Il vous sera demandé un mot de passe. Il s'agit du contenu indiqué dans les dernières cellules de votre notebook (si vous avez tout fait correctement...).

About
------
This repository contains the tutorship that is part of the *Unsupervised classification* course given to the French National School of Meteorology ([ENM](http://www.enm-toulouse.fr/)).
The corresponding course is freely available on HAL, following this [link](https://hal-meteofrance.archives-ouvertes.fr/meteo-02465143v1).
The data used in this tutorship is extracted from [MeteoNet](https://meteonet.umr-cnrm.fr/).
The procedure to download and prepare the data is available in the folder `meteonet`.
Feel free to reuse, to improve and to contact me if any question arise.

Contact : Thomas Rieutord (thomas.rieutord@meteo.fr)
