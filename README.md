# Readme - OC-Projet-4 - ChessTournamentManager
Ce programme permet de gérer la mise en place de plusieurs tournois d'échec. La mécanique d'apparaige est basée sur le système suisse. Les données sont stockées au format JSON grâce à TinyDB.


### Ce que fait l'application : 
	- Les différentes possibilités :

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
		4. Quitter le programme 



### Comment naviguer dans l'application : 
Pour sélectionner un des multiples choix il suffit d'entrer l'index du choix voulu.
Dans certaine situation, il est possible de revenir en arrière. Il suffit d'appuyer sur ''ENTRER''.



### La structure - Modèle MVC :
Nous avons développé l'application en utilisant le dessign pattern MVC. Ainsi nous avons trois documents.


**_Controllers_** : 
Il est composé de 4 controllers principaux. Le controller Menu redirige les requêtes vers le controller souhaité ( tournament, player, report)
Cependant nous faisont appel à deux autres controllers annexes. Il y en a un pour gérer les conversions et il y en a un autre pour gérer la gestion des données.


**_Views_** : 
Nous retrouvons un fichier view pour chacun des controllers clés ( menu, tournament, player, report ).
Cependant le fichier view propre aux tournois à été divisé en deux. La première partie gère la gestion des tournois, tandis que l'autre s'occupe du déroulé d'un tournoi.


**_Models_** :
Il existe 4 grands modèles : Joueur, Tournoi, Round et Match. 
Le Tournoi à besoin du rang des Joeurs afin d'organiser l'apparaige des Matchs. Il fournis à l'object Round une liste de match afin que l'object Round puisse créer ces Matchs. 



### Mise en garde : 
Si l'application est coupée la sauvegarde échoue. En effet la sauvegarde du programme s'effectue lorsque l'utilisateur quitte le programme.
Les tournois ou les joueurs sont véritablement supprimés de la base de données lorsque l'utilisateur quitte le programme.
