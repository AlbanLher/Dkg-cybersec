
### 1. Où et comment sont définis les Domaines ?

Le Domaine est un **méta-concept ontologique** (une propriété de catégorification de haut niveau, comme `dcterms:subject` ou une classe `dkg:Domain`).

- **Dans l'Ontologie (Le Cœur) :** Chaque classe d'entité ou type de relation est rattaché à un domaine principal.
    
    - _Exemple :_ La classe `Host` et la relation `CONNECTED_TO` sont marquées avec `domain: Network`.
        
- **Dans le Lexique (L'Héritage) :** Lorsqu'un terme du lexique est défini (ex: _Adresse IP_), il est annoté avec le domaine correspondant (`Domaine: Network`). Cela permet de filtrer le dictionnaire métier par secteur d'activité.
    

### 2. Qui définit les Domaines ?

Puisque les domaines découpent la gouvernance globale du DKG, ils sont sous la responsabilité conjointe de **deux rôles clés** :

- **L'Architecte de Données / Connaissances (Data/Ontology Architect) :** Il définit les grands domaines directeurs du système (ex: `IAM`, `Network`, `Threat Intel`, `Compliance`, `Assets`). C'est le gardien de la cohérence de la grille de lecture globale.
    
- **Le RSSI / Lead Expert Métier :** Il valide le périmètre de chaque domaine et décide si un domaine est à sensibilité **Publique** (ex: _Threat Intel / MITRE_) ou **Privée** (ex: _Topology_SI_Interne_).
    

### 3. Comment évolue la liste des Domaines ?

L'ajout ou la modification d'un domaine est une **évolution majeure (breaking change)** du schéma, car elle réorganise la restitution et les contrôles de sécurité. Elle ne suit donc pas le simple formulaire quotidien, mais un processus structuré :

**Étape 1 : Demande de création de Domaine (PR dédiée)** Un expert soumet une Pull Request créant le domaine dans le fichier structurant des domaines (ex: `Ontologies/input-interne/prive/DOMAINES_STRUCTURES.md` ou `.ttl`).

**Étape 2 : Validation par l'Architecte & RSSI** L'Agent Guard vérifie :

- Que le domaine ne fait pas doublon avec un domaine existant (ex: éviter de créer `Reseau` si `Network` existe).
    
- La politique d'accès associée (Qui peut voir ce domaine ? Public ou Privé ?).
    

**Étape 3 : Propagation automatique par l'Agent Guard** Une fois la PR validée :

- L'Agent ajoute le nouveau domaine dans le registre `app-referential-vault/`.
    
- Il génère le nouveau fichier de restitution Markdown associé : `exposition-md/Ontologies/par-domaines/DOMAINE_[NOM].md`.
    
- Les utilisateurs peuvent désormais classifier leurs nouveaux termes ou entités dans ce domaine via le template d'évolution standard.


#### 4. Exemples d'utilisation des Domaine

- Les représentation d'ontologies .md lisible sans être surchargées


### 5. Domaines initiaux de la Phase 0

Les domaines initiaux sont formalisés dans l'ontologie de base. Ils servent de filtre pour la restructuration documentaire et peuvent être étendus par le RSSI/Architecte.

- **`Domain:ThreatIntel`** _(Public / Externe & Interne)_ : Menaces, campagnes, acteurs, règles IoC, TAXII/MISP, CVE.
    
- **`Domain:Infrastructure`** _(Privé / Interne)_ : Assets physiques/virtuels, serveurs, IP, réseaux, topologies Nmap.
    
- **`Domain:IAM_Security`** _(Privé / Interne)_ : Identités, rôles, privilèges, accès, politiques de sécurité.
    
- **`Domain:Vulnerability`** _(Public / Interne)_ : Vulnérabilités, patchs, scores CVSS, vecteurs d'attaque.
    
- **`Domain:Governance`** _(Public / Interne)_ : Politiques, normes (ISO, NIST), règles de conformité.