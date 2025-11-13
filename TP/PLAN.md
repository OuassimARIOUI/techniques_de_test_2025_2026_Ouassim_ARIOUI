
# PLAN DE TESTS – TRIANGULATOR

---
Auteur: "ARIOUI Mohamed Achraf Ouassim"
---


## 1. Objectif général

Ce plan définit la stratégie complète de validation du microservice **Triangulator**, développé dans le cadre du module *Techniques de Test 2025/2026*.  
Le but est de concevoir une approche de test réfléchie, progressive et mesurable avant même le développement du code, dans l’esprit du **Test-Driven Development (TDD)**.

L’objectif est de garantir :
- la **fiabilité mathématique** de l’algorithme de triangulation,  
- la **cohérence des échanges binaires** entre services,  
- la **stabilité** du système face aux erreurs et aux charges,  
- la **traçabilité et qualité** du code produit.

L’approche est centrée sur la **pertinence des tests**, pas sur la simple quantité.

---

## 2. Périmètre et approche de validation

Le périmètre couvre exclusivement le microservice **Triangulator**, en interaction avec un **PointSetManager** simulé.  
Les autres composants (base de données, client, PSM réel) seront émulés ou mockés pour isoler la logique du calcul.

L’approche de validation repose sur quatre axes :
1. **Vérification unitaire** des fonctions critiques (conversion binaire, géométrie, triangulation).  
2. **Validation d’intégration** entre API et modules Flask.  
3. **Mesure des performances et robustesse** sous différents volumes de données.  
4. **Contrôle de la qualité et documentation du code** via des outils automatisés.

Ces étapes suivent une logique progressive :  
concevoir, tester, ajuster, puis documenter.

---

## 3. Tests unitaires

Les tests unitaires sont le socle de la fiabilité du service.  
Ils seront implémentés avec **pytest** et couvriront chaque module isolément.

### A. Conversion binaire PointSet / Triangles
Ces tests visent à vérifier la conformité stricte au format spécifié.  
Ils garantissent que la communication inter-services reste compacte et interprétable.

**Pourquoi :** éviter toute perte d’information ou incohérence entre encodeurs/décodeurs.  
**Comment :**
- Tester la cohérence entre le nombre de points et la taille du flux binaire.  
- Vérifier la précision des coordonnées après désérialisation.  
- Détecter les flux tronqués, les NaN, les index hors borne.  
- Effectuer un test “aller-retour” (encode → decode → encode) pour prouver la symétrie de l’opération.

### B. Logique de triangulation
Ces tests vérifient la validité mathématique de la triangulation générée.  
L’objectif est de détecter les erreurs topologiques et géométriques dès les premiers cas simples.

**Pourquoi :** assurer que le calcul de surface respecte les propriétés de Delaunay et la cohérence spatiale.  
**Comment :**
- Cas simple : 3 points → 1 triangle.  
- Cas carré : 4 points → 2 triangles.  
- Cas généralisé : n points → n−2−h triangles (avec h = points du contour convexe).  
- Cas non valides : points colinéaires, doublons, ou ensemble vide.  
- Cas aléatoires : forme spiralée (“coquille d’escargot”) pour tester la stabilité.

### C. Gestion d’erreurs internes
Chaque exception doit être capturée, loguée et traduite en message clair pour le client.

**Pourquoi :** éviter les crashs silencieux et rendre les erreurs prédictibles.  
**Comment :**
- Forcer des erreurs de parsing et vérifier les logs.  
- S’assurer qu’un format JSON d’erreur standard est toujours retourné.  

---

## 4. Tests d’intégration et API

Ces tests valident le comportement global du service Flask et sa communication avec le PointSetManager.  
Ils simulent un environnement réel, sans dépendances physiques.

**Pourquoi :** s’assurer que le Triangulator réagit correctement aux scénarios réseau et aux données binaires issues du PSM.  
**Comment :**
- Lancer le serveur Flask en mode test (client Flask intégré).  
- Utiliser `requests_mock` pour simuler le PointSetManager.

### A. Cas nominal : requête valide
Le client envoie une requête GET `/triangulate/{pointSetId}`  
→ le service récupère le PointSet binaire auprès du PSM  
→ calcule la triangulation  
→ renvoie un flux binaire `Triangles` avec code 200.

### B. Cas d’erreurs contrôlées
- UUID invalide → 400 Bad Request.  
- PointSet inexistant → 404 Not Found.  
- PSM indisponible → 503 Service Unavailable.  
- Timeout ou corruption de données → 500 Internal Server Error.  
- Mauvaise méthode HTTP → 405 Method Not Allowed.  

### C. Schéma du flux complet



    Client->>Triangulator: GET /triangulate/{id}
    Triangulator->>PointSetManager: GET /pointset/{id}
    PointSetManager-->>Triangulator: Données binaires PointSet
    Triangulator-->>Client: Triangles (format binaire)
Ce diagramme illustre le flux logique testé dans les scénarios d’intégration.
```
## 5. Tests de performance

Les tests de performance évaluent la **vitesse**, la **scalabilité** et l’**efficacité mémoire** du service.  
Ils seront exécutés indépendamment grâce au marqueur `@pytest.mark.perf`.

**Pourquoi :** identifier les goulots d’étranglement de l’algorithme et valider la capacité du service à évoluer.  
**Comment :**

- Générer des *PointSets* de tailles variables (10, 100, 1 000, 10 000 points).  
- Mesurer le temps moyen d’exécution et le taux de croissance temporelle.  
- Évaluer la conversion binaire sur grands volumes.  
- Vérifier la consommation mémoire via **psutil**.

Les seuils seront ajustés **empiriquement** selon la complexité des jeux de données et la machine d’exécution.

---

## 6. Tests de robustesse et de sécurité

Ces tests garantissent la **résilience** du service face aux entrées anormales, erreurs système et attaques potentielles.

**Pourquoi :** prévenir les crashs, débordements mémoire et comportements indéterminés.  
**Comment :**

- Injecter des données binaires aléatoires ou tronquées.  
- Tester des flux contenant des valeurs infinies ou non numériques.  
- Simuler des requêtes malveillantes pour évaluer la résistance aux DoS légers.  
- Déconnecter le **PointSetManager** pour observer la gestion d’erreurs réseau.

Ces tests mesurent la **robustesse logicielle** et la **qualité de la gestion des exceptions**.

---

## 7. Tests de qualité et documentation

Cette phase vise à assurer la **maintenabilité** et la **conformité** du code.

**Pourquoi :** un code bien structuré et documenté se teste et évolue mieux.  
**Comment :**

- Vérifier la conformité stylistique avec **ruff** via `make lint`.  
- Générer un rapport de couverture via **coverage** (objectif : ≥ 90 %).  
- Créer la documentation automatique avec **pdoc3**.  
- S’assurer que chaque fonction contient une **docstring claire** (but, paramètres, retours).

## 8. Organisation du projet et structure des tests

```text
project/
├── triangulator/
│   ├── api.py
│   ├── core.py
│   ├── binary_utils.py
│   └── __init__.py
│
├── tests/
│   ├── unit/
│   │   ├── test_triangulation.py
│   │   ├── test_binary_encoding.py
│   │   └── test_errors.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   └── test_pointsetmanager_mock.py
│   ├── perf/
│   │   ├── test_perf_triangulation.py
│   │   └── test_perf_serialization.py
│   └── fixtures/
│       ├── triangle.pset
│       ├── square.pset
│       └── spiral.pset
│
├── Makefile
├── requirements.txt
├── dev_requirements.txt
└── PLAN.md
```

Les tests seront exécutés via le Makefile :
make test pour l’ensemble des tests,
make unit_test pour les tests rapides,
make perf_test pour les benchmarks,
make lint pour la qualité du code,
et make doc pour la documentation HTML.

