---
type: phase
phase_num: <%* let pNum = await tp.system.prompt("Numéro de Phase (ex: 06) :"); tR += pNum; %>
phase_nom: <%* let pNom = await tp.system.prompt("Nom de la Phase :"); tR += pNom; %>
statut: En cours
date_debut: <% tp.file.creation_date("YYYY-MM-DD") %>
date_cloture: 
vague: <%* let pVague = await tp.system.prompt("Numéro de Vague (ex: V3) :"); tR += pVague; %>
---
# 📋 Phase <% pNum %> : <% pNom %>

> **Statut** : 🟡 En cours  
> **Date de début** : <% tp.file.creation_date("DD/MM/YYYY") %>  
> **Date de clôture** : [JJ/MM/AAAA]  

---

## 🎯 1. Objectifs & Périmètre
* **But principal** : 
* **Livrables attendus** : 

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécification associée** : `SPEC-<% pNum %>.md`
* **Exigences couvertes** : 

### B. Instanciation & Use Case Pédagogique (Lisible Humain)
* **Document d'illustration** : [`Human_UseCase.md`](./Human_UseCase.md)

### C. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : `Master_Transversal/`
* **Artefacts Snapshot** : `Snapshot_Phase_<% pNum %>/`

---

## 🏁 3. Synthèse de Clôture & Ressources

### Matrice Récapitulative des Livrables
| Brique        | Composant / Fichier  | Description                            |
| :------------ | :------------------- | :------------------------------------- |
| **Framework** | `SPEC-<% pNum %>.md` | Spécification des contraintes & règles |
| **Data**      | `Graphe_Master.ttl`  | Fichiers RDF / Turtle générés          |
