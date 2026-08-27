# Use Case  l'histoire de l'assistant Cyber

Ce cas d'usage doit permettre d'illustrer les enjeux d'un Assistant IA basé sur le Dynamic Knowledge Graph

Dynamique :
- on commence petit : usage local personnel et peu de fonctions cyber, puis on évolue jusqu'à une micro-entreprise avec un petit SOC (Securoty Operation Center)
- Les enjeux de la connaissance sont dans le détail de la sémantique et du context.  La notion de TBox "Terminology" Box qui évolue et sur laquels se basent les Agents

> *"Comment une simple règle de sécurité peut devenir un casse-tête...
> et comment une ontologie bien conçue permet de le résoudre."*

---

## 🎭 Personnages et Éléments Clés

| **Élément**          | **Rôle** | **Description**                                        | **Exemple**        |
| -------------------- | -------- | ------------------------------------------------------ | ------------------ |
| **Alban**            | Individu | Dispose d'un PC sur lequel est installé un server web. | -                  |
| **Server Web**       | Device   | Serveur Web                                            | `id: "srv-web-01"` |
| **NGINX web Server** | Logiciel | Version vulnérable (CVE-2021-23017).                   | `id: "sginx 1201"` |
|                      |          |                                                        |                    |

---

## 🌱 **Phase 1 : TBox  – "Un PC, Une Règle Simple"**
**Contexte** :

A ce stade on ne s'intéresse qu'au premiers conept :
- Assets  { materiel}
- SoftwareComponent {}
- Vulnerability {}
- Weakness {}

A mettre dans un referentiel Lexique, semantique et ontologique

**l'instanciation suivante ** :
1. Il **modélise son environnement** :
   - 1 PC (`PC-Alban-POC`) et 1 routeur (`Router-POC`).
   - 2 logiciels : OpenSSL 1.0.2 et Apache 2.4.57.
   - 1 vulnérabilité : CVE-2023-1234 (CVSS 9.8) liée à OpenSSL 1.0.2.
   - 1 règle : *"Mettre à jour OpenSSL vers 3.0.8"*.

2. Il **visualise les liens** :
   - `PC-Alban-POC` **→ hasSoftware →** `OpenSSL 1.0.2`
   - `OpenSSL 1.0.2` **→ affectedBy →** `CVE-2023-1234`
   - `CVE-2023-1234` **→ requiresAction →** *"Mettre à jour OpenSSL"*

**Résultat** :
✅ Alban comprend **immédiatement** que son PC est vulnérable.
✅ Il sait **quelle action prendre** (mettre à jour OpenSSL).

**Limites** :
❌ **Pas de différenciation** entre les devices (tout est traité de la même façon).
❌ **Pas de règles complexes** (seulement des actions correctives basiques).


---

## 🏢 **Phase 2 : La ABox initiale 

**Contexte** : A ce stade on instancie les concepts avec des premiere données (instances)
- Assets  { srv-web-01}
- SoftwareComponent {sw-nginw-1202, CVE-2021-23017 }
- Vulnerability {}
- Weakness {}



---
## 🧩 **illustration des enjeux de l’Ontologie**
### 🔴 **Sans Ontologie (Approche "En Vrac")**
```mermaid
graph TD
    A[Server-Prod] -->|a| B[OpenSSL 1.0.2]
    B -->|affecté par| C[CVE-2023-1234]
    C -->|CVSS 9.8| D[❌ PROBLÈME : Règle violée !]
    A -->|doit respecter| E[Règle: CVSS ≤ 5]

```
→ Résultat :

On ajoute une exception manuelle dans un fichier Excel.
Personne ne sait pourquoi Server-Prod est une exception.
Impossible de reproduire la logique pour un nouveau serveur.

🟢 Avec Ontologie (Votre Approche)
```mermaid
graph TD
    A[Server-Prod] -->|a| B[OpenSSL 1.0.2]
    B -->|affecté par| C[CVE-2023-1234]
    C -->|CVSS 9.8| D[Vulnérabilité]
    A -->|est dans le contexte| E[Production]
    A -->|a une dérogation| F[WAIVER-001]
    F -->|justifiée par| G["Migration vers OpenSSL 3.0.8"]
    E -->|applique la règle| H[Règle: CVSS ≤ 5]
    D -->|viole| H
    F -->|résout| H
```
→ Résultat :

Tout est structuré : On sait pourquoi Server-Prod est une exception.
Reproductible : La même logique s’applique à un nouveau serveur.
Évolutif : On peut ajouter de nouveaux contextes (ex: "Test") sans tout recoder.

🎯 Leçons Apprises

L’ontologie doit évoluer pour capturer les nuances du réel.
Les contradictions sont normales : Elles révèlent des limites du modèle.
La résolution passe par :

L’enrichissement (ajout de classes/propriétés comme :Context, :Waiver).
La structuration (hiérarchies, relations).
La documentation (justifications, exceptions).

.






