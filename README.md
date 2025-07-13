# Lire-plus-dsfsft35

We are a team of three data science bootcamp students, and this is our final project.
More to come.

## Petit rappel pour collaborer avec Git

1. Créez une branche séparée pour votre addition au projet:

    ```bash
    git checkout -b "new branch name"   # Crée la nouvelle branche, lui donne un nom, et bouge le "curseur" vers elle.
                                        # Comme si on faisait un `cd` vers le dossier de la nouvelle branche après l'avoir créée.
    ```

2. Faites vos modifications normalement, vous êtes sur votre propre branche du projet:

    ```bash
    git add .                                      # Ajoute toutes ("." = "toutes") les modifications depuis le dernier "commit"
                                                   # à un panier de modifications à garder.
    git commit -m "descriptif des modifications"   # Donne un nom à ce panier et le prépare à être synchronisé avec la branche qui est en ligne.
    git push                                       # Synchronise les modifications choisies avec la branche en cours.
    ```

3. Si besoin, naviguez entre les différentes branches du projet et le tronc du projet:

    ```bash
    git checkout main                                               # Bouge le "curseur" vers la branche principale.
    # ou
    git checkout le-nom-de-la-branche-non-principale-à-aller-voir   # Pareil, mais vers une autre branche.
    ```

4. Vous avez terminé votre addition au projet, et vous voulez que votre branche fusionne avec la branche principale:

    ```bash
    git checkout main                       # Quitte la branche en cours et rejoint la branche principale.
    git merge le-nom-de-votre-branche       # Fusionne la branche nommée avec la branche principale!
    git branch -d le-nom-de-votre-branche   # Supprime la branche voulue, puisqu'on en n'a plus besoin.
    ```
