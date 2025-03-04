# Design 2025

## Présentation du projet

Ce projet à été créé par **Loïc Duhamel** et **Sam Félix Desjardins** dans le cadre du projet Design 2025 de Secondaire 3 PEI à l'École Secondaire Ozias Leduc. Il consiste en un site internet complet (backend et frontend) créé dans le but de tester si il est préférable pour un adolescent d'étudier sur un ordinateur ou sur un téléphone intelligent. Il a été créé dans un but académique et aucuns résultat en venant ne devrait être utilisé dans un cadre professionel. Il est aussi à noter que ce projet à été réalisé dans une fenêtre de temps réduite dans le but de satisfaire les délais imposé par les enseignants responsable de l'évaluation du travail.
Le contenu de ce projet (code source et autres) ne possède **aucune** license ni garantie que ce soit. Il en revient donc à l'utillisateur la responsabilité de l'utilisation et de la vérification du bon fonctionnement du programme.

## Mode d'emploi

### 1. Télécharger le code source: 

#### Avec git (recommandé):

1. Ovrir un terminal de votre choix dans un emplacement vide
3. Exécutez la commande `git clone https://github.com/Astroloico/design-2025.git`

#### Sans git (non-recommandé):

1. Appuyer sur le bouton vert (qui dit Code), puis sur Download zip
2. Extraire les contenus dans un emplacement de votre choix (ex: ~/Documents)

### 2. Lancer le serveur :

#### 1. Installer python (si non-installé) :

> [!IMPORTANT]
> Pour Windows seulement :
>  1. Ouvrir le Terminal
>  2. Entrer la commande `winget install Python.Python.3.9`
> *Note : Sur Linux et MacOS, python vient pré-installé*

#### 2. Installer flask :

1. Ouvrir un terminal
2. Entrer la commande `pip install flask`
> [!NOTE]
> Sur Linux, dépendamment de votre distribution et de votre configuration, vous pourriez avoir besoin de rajouter `--break-system-packages` à la fin de la commande précédente

#### 3. Lancer l'application :

> [!CAUTION]
> À partir de maintenant, la fermture ou le redémmarage du programme éxécutant le programme du serveur et/ou de son environnement d'éxécution **et/ou le chagement de réseau local (LAN) sur lequel le dit appareil est connecté** résulteras possiblement et probablement en le besoin de recommencer depuis la dite étape ainsi que la perte irréversible de toutes données non-téléchargéee*

1. Ouvrir un terminal dans l'emplacement dans lequel vous avez téléchargé le code source (le dossier dans lequel se trouve le fichier `run.py`)
2. Entrer la commande `python run.py`
> [!TIP]
> Si vous recevez un message d'erreur vous disant que la commande `python` n'existe pas, essayez avec `python3` ou avec `python2`*

#### 4. Création de l'objet de recherche

1. Dans le résultat de la dernière commande, il y a un lien. Ouvrez-le dans un naviateur internet.
2. Cliquer sur "Créer un recherche"
3. Remplir les champs demandés
4. Cliquer sur le lien en bas de page

### 3. Préparation de l'équipement

1. Connecter un ordinateur portable et un téléphone intelligent aur le même réseau local (LAN) que l'ordinateur qui sert de serveur
2. Sur les deux appareils, naviguer au même URL que dans l'étape 2.4.1.

### 4. Pendant la recherche

#### Pour chaque étudiant qui viens participer

3. Régler le contenu de du champ "id" sur l'identifiant indiqué dans la page ouverte sur l'ordinateur qui sert de serveur
4. Demander a l'étudiant de s'asseoir devant soit l'ordinateur, soit le téléphone intelligent (lui donner) en assurant une distribution du nombre de résultats entre les appareils de 50/50 environ pour des résultats optimaux
5. Expliquer à l'étudiant le sujet de la recherche et que quand il/elle appuira sur le bouton  ** [START] ** , ils auront deux minutes pour memoriser 50 items (das le cas présent, des comptés de la Californie), puis devrons en réécrire le plus possible.
> [!TIP]
> Ce temps peut être adjuster à la ligne 106 de static/script.js (remplacer `120000` par le temps voulu en millisecondes)
> Per contre, il est à noter que certaines valeures pourrais causer des problèmes d'affichage

7. Après que le temps soit écoulé, la page sur l'appareil de l'élève vas changer, révélant une zone de réponse et un boutton. Dire à l'élève d'écrire touts les élément dont il/elle se souvient. De plus, mentionner à l'élève que l'orthographe des mots n'est pas important, tout comme les majuscules et/ou espaces.
> [!WARNING]
> Il est nécessaire que l'élève écrive un seul élément par ligne. Si cette règle n'est pas réspectée, le système d'évaluation de réponse automatique ne fonctionnera pas correctement. Il est donc très important de le mentionner à l'élève et de s'assurer que cette règle est respectée

8. Une fois que l'élève à finit, lui demander d'appuyer sur le bouton en bas de page.
> [!IMPORTANT]
> Sur certains appareils (notament sur iPhone), le navigateur envoie un message disant que le transfer d'information n'est pas sécuritaire et demandant si-il doit poursuivre avec la transmission (cliquer sur cette option). Ceci est dû au fait que le site utillise le protocole HTTP au lieu de HTTPS. Dans ce cas-ci, il n'est pas sensé d'utillisé HTTPS car le site est conçu pour être disponible seulement sur un réseau local (LAN). Par contre, dans le cas ou le chercheur veut utilliser le site sur l'internet, il est très fortement suggèré de mettre en place un serveur HTTPS/WSGI pour des raisons de sécurité.

#### À la fin de la recherche

1. Appuyer sur le bouton/lien "Télécharger les résultats" sur le panneau de contrôle. Cela vas télécharger localement un fachier HTML qui contient toutes les données receuillies. Ce fichier peut être ouvert avec un navigateur web sans accès à l'internet.
> [!CAUTION]
> Verifier si le fichier est bel et bien présent et fonctionnel **avant** de poursuivre, car il ne seras plus possible de revenir en arrière.

2. Fermer touts les logiciels associés au site (terminal du serveur, fenêtres de navigateurs ouvertes sur le site, ect.).

### Résolution de problèmes

Il existe plusieurs problèmes qui peuvent survenir lors de la mise en place du système.

#### 1. Les navigateurs des appareils utilisés pour la collection de donnés ne peuvent pas atteindre le site

Dans ce cas, vérifier si touts les trois appareils sonts connectés sur le même réseau local. Si non, essayer un autre réseau. Pour en créer un temporaire, un méthode (non-optimale mais fonctionelle) est d'activer le partage de connection de données cellulaires sur le téléphone intelligent, puis de connecter les deux ordinateurs sur le réseau nouvellement créé.
