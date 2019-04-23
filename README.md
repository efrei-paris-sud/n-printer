# n-printer

Contributors :

BAHNIS Mehdi mehdi.bahnis@efrei.net 
BALLAM Clément clement.ballam@efrei.net 
BELAIDI Sonia sonia.belaidi@efrei.net 
BOUKHEMKHAM Mohamed mohamed.boukhemkham@efrei.net MohamedBkhm
BURIN Julien julien.burin@efrei.net Julio9777


Description :
« N-Printer » : Aujourd'hui avec le développement des smartphones et des objets connectés, le consommateur lambda est noyé par la data. En effet, celui-ci est submergé par des publicités, des notifications ou des fakes news. Dans ce contexte de désinformation, notre équipe de chercheur a mis au point une solution : "N-Printer". L'objet connecté qui n'imprime que les informations dont vous avez besoin ! 
"N-Printer" est une imprimante connectée éco-responsable. A l’aide de papier thermique, elle peut imprimer des informations provenant d’une ressource internet prédéfini par l’utilisateur. Ce choix se fait grâce aux API. Dans notre cas, nous allons nous servir de Twitter, réseau très apprécié par les journalistes et politiciens. Pour davantage contrôler le flux, les impressions peuvent être réalisés de manière cyclique. L’utilisateur peut alors recevoir un bulletin d’impression à intervalle régulier.
A noter qu’en France, il y a 41 millions d’utilisateurs de smartphones. Notre marché touche donc près des 2/3 de la population française.  De plus, l’INSEE a déclaré qu’en 2018, un adulte moyen passe près de 3 :42 derrière un écran. Conscient que ce chiffre est important, nous voulons offrir aux français une alternative pour s’informer efficacement.

Voici les fonctions finales du produit.

Nous avons sur notre planche 3 boutons poussoir et 1 bouton supplémentaire mis à l'écart. Ce dernier va permettre de mettre la machine en fonctionnement, sur le raspberry, la mise en fonctionnement se fait en reliant le GPIO3 a une masse. Nous avons donc réalisé ce montage.

Ensuite nous avons 2 états pour le système :

  -Le premier état est un état dit "sleep" ou le programme principal n'est pas lancé. Le Raspberry est bien booté mais il ne se passe       rien. Cet etat s'illustre en gardant la led verte allumée.
    Il permet de ne pas effectuer les action automatique de l'imprimante et de ne rien imprimer pour l'instant. Il permet aussi de            modifier le code et une fois enregistré, on peut lancer directement la nouvelle version sans debrancher le tout.
   
   -Le deuxième etat lui est l'état 

Components needed :
Rasberry-Pi Modèle B

Nous avons décidé d'utiliser un Raspeberry Model B car il convenait a une utilisation autonome de l'objet connecté. Il permet de configurer un bouton de mise sous tension qui va ensuite automatiquement lancer un script qui va executer le programme sans aucune intervention de l'utilisateur ni de quelquonque autre composant informatique.
Les modification du code qui sont tres importante pour l'utilisateur et facilités par notre equipe peuvent être fait directement sur le raspberry et il suffit juste de reboot la machine a l'aide du bouton que nous avons configuré pour appliquer ses modifications.
Ces aspects sont tres important pour notre projet car un de ses but principal est de pouvoir moduler les fonctions à la guise de l'utilisateur. Et additionellement, nous souhaitons commercialiser le produit de maniere a ce qu'il soit pret à utiliser, il faut donc qu'on ait un systeme fiable simple d'utilisation et autonome.

Une imprimante thermique
Des rouleaux de papier thermique
Une alimentation de 5V
Adaptateur femelle (pour la connection)
Un pack de LED
Bouton poussoir
Une carte SD
Cable avec des connecteurs mâles et femelles

