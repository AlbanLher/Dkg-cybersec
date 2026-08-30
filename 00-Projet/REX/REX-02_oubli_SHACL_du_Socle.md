C'est la prise de conscience fondamentale en architecture de données sémantiques : **la TBox/RBox seule est un modèle de sens, pas un modèle d'intégrité.**

Pour avoir des fondations complètes et prêtes pour la production, le DKG repose sur un triptyque indissociable :

```
┌────────────────────────────────────────────────────────┐
│               SOCLE DE CONNAISSANCE DKG                │
├────────────────────┬──────────────────┬────────────────┤
│    TBox (OWL)      │    RBox (OWL)    │ SHACL (Shapes) │
│     Concepts       │    Relations     │   Validation   │
│  "Ce que c'est"    │ "Comment c'est   │ "Ce qui est    │
│                    │    lié"          │   exigé"       │
└────────────────────┴──────────────────┴────────────────┘
```




### 📚 La division des rôles au niveau des fondations

|Composant|Rôle architectural|Type de logique|Question à laquelle il répond|
|---|---|---|---|
|**TBox** _(Terminological Box)_|Dictionnaire de classes & typage d'attributs|**Expressive / Déductive** _(OWA)_|_"C'est quoi un Asset ? C'est quoi une Vulnérabilité ?"_|
|**RBox** _(Role Box)_|Caractéristiques des propriétés _(transitivité, symétrie, inversibilité)_|**Inférentielle** _(OWA)_|_"Si le Composant A est installé sur Asset 1, alors Asset 1 contient le Composant A."_|
|**SHACL** _(Shapes Constraint)_|Contraintes d'intégrité, formats, cardinalités et règles métier|**Impérative / Validation** _(CWA)_|_"Est-ce que l'IP est valide ? Le score CVSS est-il bien renseigné et entre 0 et 10 ?"_|

### 💡 Pourquoi SHACL fait partie intégrante du Master Transversal

Sans le SHACL, une ontologie OWL autorise « par défaut » n'importe quel graphe incomplet ou incohérent à exister (car en OWL, tout ce qui n'est pas explicitement impossible est considéré comme possible ailleurs).

C'est précisément pour cela que le placement de `shapes_abox.ttl` dans **`12-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`** fait sens :

1. **Intégrité indissociable** : Modifier la TBox (ex: ajouter la classe `Patch`) implique **immédiatement** de mettre à jour la Shape SHACL associée (ex: `PatchShape` imposant la présence d'un identifiant KB/PatchID).
    
2. **Contrat de Qualité** : C'est le SHACL qui définit le contrat d'interface pour l'ingestion de données (Phase 3) avant leur chargement final dans le Graph Store / Neo4j (Phase 3b).

#  Rappels principes RDF/OWL et SHACL
C'est une question fondamentale en ingénierie ontologique W3C (RDF/OWL vs SHACL). La raison principale est que **l'ontologie (OWL/TBox) et le système de validation (SHACL) ont des objectifs et des logiques mathématiques complètement différents**.

### 1. La différence de philosophie (OWA vs CWA)

|**Critère**|**OWL / TBox (DKG_TBox_Master.ttl)**|**SHACL (shapes_abox.ttl)**|
|---|---|---|
|**Philosophie**|**OWA** (_Open World Assumption_ — Hypothèse du monde ouvert)|**CWA** (_Closed World Assumption_ — Hypothèse du monde fermé)|
|**Rôle principal**|**Inférence & Déduction** (exprimer ce que les choses _signifient_)|**Validation & Contrôle qualité** (vérifier que la donnée est _conforme_)|
|**Comportement sur donnée manquante**|_"La donnée n'est pas présente, mais elle existe peut-être ailleurs dans le monde."_|_"Le champ est obligatoire. S'il n'est pas là, c'est une erreur."_|

### 2. Pourquoi OWL (TBox) ne peut pas valider les données

Dans OWL, les contraintes ne servent pas à rejeter une donnée incorrecte, mais à **déduire de nouvelles informations**.

#### Exemple concret : L'adresse IP d'un `Asset`

Supposons qu'en métier, on veuille imposer la règle : _"Tout Asset doit avoir au moins une adresse IP (`ipAddress`)"_.

- **Si on le définit dans l'ontologie OWL :**
    
    Si tu soumets un Asset `dkg:Server01` sans adresse IP, l'analyseur OWL (Raisonneur) ne génère **aucune erreur**. Il conclut simplement :
    
    > _"Server01 est un Asset, donc il possède une IP quelque part dans l'univers, même si elle n'est pas encore écrite dans ma base RDF."_
    
- **Si on le définit dans la Shape SHACL :**
    
    Le moteur SHACL valide la base sous l'hypothèse du monde fermé (CWA). Il vérifie l'existence effective du triplet sur le nœud et déclenche immédiatement une **violation de conformité** :
    
    > `Violation: Node dkg:Server01 does not have required property dkg:ipAddress (minCount 1).`
    

### 3. Les contrôles avancés que seul SHACL sait faire

L'ontologie OWL décrit la structure sémantique globale, mais ne propose pas les outils de contrôle qualité indispensables pour une base de données de production :

1. **Validation de formats et Regex** : Vérifier qu'une chaîne de caractères respecte le format d'une IP (`^([0-9]{1,3}\.){3}[0-9]{1,3}$`) ou le pattern d'un identifiant CVE (`^CVE-\d{4}-\d+$`). OWL en est incapable.
    
2. **Cardinalités et bornes numériques** : Imposer qu'un score CVSS v3 soit une valeur numérique strictement comprise entre `0.0` et `10.0`.
    
3. **Contraintes contextuelles dynamiques** : Valider des règles complexes (ex: _"Si un composant logiciel a une vulnérabilité CRITICAL, l'Asset parent doit avoir un marquage TLP supérieur ou égal à AMBER"_).
    

### En résumé

- **`DKG_TBox_Master.ttl` (OWL)** sert de **dictionnaire et de modèle de connaissance** (pour que Neo4j, les requêtes SPARQL et les raisonneurs comprennent les types, les héritages et les relations).
    
- **`shapes_abox.ttl` (SHACL)** sert de **garde-fou / compilateur de validation** (pour garantir la qualité des données entrantes et rejeter les anomalies avant consolidation).