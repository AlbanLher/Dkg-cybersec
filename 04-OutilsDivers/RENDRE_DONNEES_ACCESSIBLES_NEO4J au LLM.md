_(Puisque je ne peux pas accéder directement à votre Neo4j)_

### **📌 Option 1 : Export en Cypher (Recommandé)**

1. Exportez le graphe en Cypher** :
```cypher
# Dans Neo4j Browser, exécutez :
CALL apoc.export.cypher.all("graphe-complet.cypher", {format: 'cypher-shell'})
```
   
   _(Le fichier sera généré dans `/var/lib/neo4j/import/graphe-complet.cypher`.)_
   
2. **Copiez le fichier dans votre dépôt** (temporairement pour le POC) :
   
```bash
cp /data/neo4j/import/graphe-complet.cypher 03-Implementation/Phase0-Cadrage/data/pseudo-private/
git add 03-Implementation/Phase0-Cadrage/data/pseudo-private/graphe-complet.cypher
git commit -m "data: Export du graphe Neo4j (POC)"
git push
```
    
3. **Partagez le lien** :
    - [Lien vers le fichier](https://github.com/AlbanLher/Dkg-cybersec/blob/main/03-Implementation/Phase0-Cadrage/data/pseudo-private/graphe-complet.cypher)

---

### **📌 Option 2 : Screenshot + Requêtes Exemples**

1. **Prenez un screenshot** de Neo4j Browser avec :
    
    - Le schéma du graphe (onglet "Graph").
    - Le résultat d’une requête (ex: `MATCH (n) RETURN n LIMIT 10`).
2. **Partagez les requêtes clés** :
    
    markdown
    
    Copier
    
    ````
    ### 🔍 Requêtes pour Vérifier le Graphe
    ```cypher
    // 1. Lister toutes les classes
    MATCH (n) WHERE n\:Device OR n\:Software OR n\:Vulnerability RETURN n
    
    // 2. Lister les devices avec leurs logiciels
    MATCH (d\:Device)-[\:HAS_SOFTWARE]->(s\:Software) RETURN d, s
    
    // 3. Lister les CVE critiques (CVSS > 7)
    MATCH (v\:Vulnerability) WHERE v.cvssScore > 7 RETURN v
    ````
    

---

### **📌 Option 3 : Fichier de Métadonnées**

_(Pour décrire ce qui est dans le graphe sans partager les données brutes)_

Créez un fichier `03-Implementation/Phase0-Cadrage/data/pseudo-private/GRAPHE_SOMMAIRE.md` :

# 📊 Sommaire du Graphe Neo4j (POC)

## 📌 Statistiques

| Type      | Compte | Exemples                                                     |
| --------- | ------ | ------------------------------------------------------------ |
| Nœuds     | 25     | PC-Alban-POC, OpenSSL_1.0.2, CVE-2026-1234                   |
| Relations | 15     | HAS_SOFTWARE, HAS_VULNERABILITY, APPLIES_RULE                |
| Classes   | 7      | Device, Software, Vulnerability, Rule, Action, User, Context |
## 🔗 Structure
```mermaid
graph TD
    Device -->|HAS_SOFTWARE| Software
    Device -->|HAS_VULNERABILITY| Vulnerability
    Software -->|AFFECTED_BY| Vulnerability
    Vulnerability -->|REQUIRES_ACTION| Action
    Rule -->|APPLIES_TO| Device
    Rule -->|ASSIGNED_TO| User
````

## 📄 Données Chargées

| Fichier                       | Nœuds Créés              | Relations Créées |
| ----------------------------- | ------------------------ | ---------------- |
| `ontologie-publique.ttl`      | 7 (classes)              | 6 (propriétés)   |
| `ontologie-pseudo-privee.ttl` | 3 (pseudo<br><br>, etc.) | 2                |
| `inventory.json`              | 3 (PC-Alban-POC, etc.)   | 6 (HAS_SOFTWARE) |
| `cve_data.ttl`                | 10 (CVE-2026-*)          | 0                |
| `internal_rules.ttl`          | 2 (pseudo<br><br>, etc.) | 1 (APPLIES_TO)   |