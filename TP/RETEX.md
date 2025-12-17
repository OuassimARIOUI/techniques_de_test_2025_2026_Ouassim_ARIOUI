# Retour d'experience sur le projet - Arioui Mohamed Achraf Ouassim

## Ce qui a bien marchée 

J’ai réussi à faire passer tous les tests (unitaires, d’intégration et de performance). Les tests sont fiables et rapides.

J’ai configuré et exécuté ruff pour la vérification du style et corrigé la majorité des problèmes détectés.

J’ai implémenté les fonctions manquantes (sérialisation des PointSet, parsing, encodage des triangles, triangulation simple), ce qui a rendu le code pleinement fonctionnel.

J’ai généré la documentation du projet avec pdoc3.

## Ce qui as mal marchée

Je n’ai pas toujours respecté l’approche test first : certains comportements ont été implémentés avant les tests, ce qui a entraîné des ajustements a posteriori et des incohérences entre tests et implémentation.

La gestion des dépendances et de l’intégration n’a pas été optimale : l’URL du PointSetManager est restée hardcodée, la dépendance requests a été ajoutée tardivement et les tests d’intégration ne reposent pas sur un mock réellement représentatif.

La granularité des commits et la documentation technique pourraient être améliorées afin de faciliter la maintenance, la relecture et l’évolution du projet.

## ce que j'aurait du faire 
J’aurais dû appliquer strictement l’approche test first, en écrivant les tests avant l’implémentation afin de guider la conception et 
d’éviter les ajustements a posteriori.

J’aurais dû paramétrer l’URL du PointSetManager et mettre en place un mock ou serveur simulé pour les tests d’intégration, 
afin de garantir des tests reproductibles et indépendants de l’environnement.

J’aurais dû effectuer des commits plus petits et plus fréquents, 
chacun portant une modification cohérente et clairement justifiée.

## Explication de la structure du projet

### Organisation des fichiers

Le dossier TP/tests/ contient l’ensemble des tests du projet, répartis en tests unitaires, tests d’intégration, tests API et tests de performance :

test_triangulator_unit.py : tests unitaires de la logique de triangulation.

test_triangulator_integration.py : tests d’intégration validant l’enchaînement PointSetManager → Triangulator → API Flask.

test_triangulator_perf.py : tests de performance permettant d’évaluer le comportement du système sur des jeux de données plus volumineux.

Le fichier TP/models.py définit les modèles de données utilisés dans le projet, notamment PointSet et Triangles.

Le fichier TP/Triangulator.py contient la classe Triangulator, qui regroupe plusieurs responsabilités :

get_pointset / get_PointSet : récupération d’un PointSet depuis le PointSetManager,

parse_pointset(data: bytes) : décodage d’un PointSet à partir de données binaires,

triangulate(point_set_id) : calcul de la triangulation à partir d’un identifiant de PointSet,

encode_triangles(triangles: Triangles) : encodage des triangles au format binaire,

create_app(triangulator) : création de l’application Flask exposant l’endpoint /triangulate/<point_set_id> retournant les triangles encodés en binaire.
