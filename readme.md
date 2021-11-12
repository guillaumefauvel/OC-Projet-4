# Readme - OC-Projet-4 - ChessTournamentManager
Ce programme permet de gérer la mise en place de plusieurs tournois d'échec. La mécanique d'apparaige est basée sur le système suisse. Les données sont stockées au format JSON grâce à TinyDB.



### Lancement du programme :
Afin de lancer le programme, assurez-vous d'avoir préalablement créé et activé un environnement virtuel. Installez-les 
requirements à l'aide d'un `pip install requirements.txt`. Lancez le programme en entrant `python main.py`.  
Pour lancer un diagnosic flake8 lancez `flake8 code --max-line-length 119 --format=html --htmldir=flake-report` dans le 
terminal. Accèdez au résulat en entrant `flake-report/index.html`.

### Arborescence : 

		1. Gestion des tournois
			1. Lancer un nouveau tournoi 
			2. Reprendre un tournoi en cours 
			3. Supprimer un tournoi
		2. Gestion des joueurs 
			1. Ajouter un nouveau joueur
			2. Supprimer un joueur 
			3. Rechercher les informations d'un joueur
		3. Gestion des rapports
			1. Une liste de tous les joueurs classée par ordre alphabétique
			2. Une liste de tous les joueurs classée par classement
			3. Une liste de tous les joueurs d'un tournoi classée par ordre alphabétique
			4. Une liste de tous les joueurs d'un tournoi classée par classement
			5. Une liste de tous les tournois
			6. Le tableau des scores d'un tournoi
			7. Le récapitulatif d'un tournoi
			8. Le tableau des scores
		4. Sauvegarder l'état du programme
		5. Quitter le programme en sauvegardant
		6. Quitter le programme sans sauvegarder 

##
### Navigation : 

Pour sélectionner une action il suffit d'entrer l'index du choix voulu.
Dans certaine situation, il est possible de revenir en arrière, il suffit d'appuyer sur entrée.


##
### La structure - Modèle MVC :
Nous avons développé l'application en utilisant le dessign pattern MVC. Ainsi nous avons trois documents.


**_Controllers_** : 
Il est composé de 4 controllers principaux. Le controller Menu redirige les requêtes vers le controller souhaité (tournament, player, report)
Cependant nous faisont appel à deux autres controllers annexes. Le premier s'occupe des conversions et le second gère la gestion des données.


**_Views_** : 
Nous retrouvons un fichier view pour chacun des controllers clés (menu, tournament, player, report).
Cependant le fichier view propre aux tournois a été divisé en deux. La première partie gère la gestion des tournois, tandis que l'autre s'occupe du bon déroulement d'un tournoi.


**_Models_** :
Il existe 4 grands modèles : Joueur, Tournoi, Round et Match. 
Le Tournoi à besoin du rang des Joueurs afin d'organiser l'apparaige des Matchs. Il fournit à l'object Round une liste de match afin que l'object Round puisse créer ces Matchs. 


##
### Mise en garde : 
Si l'application est interrompue en cours de fonctionnement, les dernières modifications risquent de pas avoir intégré la base de données.
Les tournois ou les joueurs supprimés sont ôtés de la base de données lorsque l'utilisateur quitte le programme (avec sauvegarde)
où lorsqu'il décide de sauvegarder.