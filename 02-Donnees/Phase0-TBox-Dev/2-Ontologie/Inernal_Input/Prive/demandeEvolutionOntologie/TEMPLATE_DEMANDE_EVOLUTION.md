<!-- 
  ========================================================================
  FORMULAIRE DE DEMANDE D'ÉVOLUTION D'ONTOLOGIE / LEXIQUE (DKG)
  ========================================================================
  Consignes :
  - Remplissez les champs entre crochets [ ... ].
  - Ne modifiez pas la structure des titres pour permettre le traitement par l'Agent.
-->

# 📝 Demande d'évolution : [Nom court de l'évolution / du concept]

**Informations sur le demandeur**
* **Auteur :** [Prénom Nom]
* **Rôle / Métier :** [ex: Analyste SOC, RSSI, Expert Métier, Architecte]
* **Date :** [AAAA-MM-JJ]
* **Statut de la demande :** [ ] En attente de revue | [ ] Validé RSSI | [ ] Rejeté

---

## 1. Type de modification

> *Cochez la case correspondante avec un "X" : [X]*

* [ ] **Ajout** d'un nouveau terme ou d'une nouvelle entité
* [ ] **Modification** d'une définition ou d'une relation existante
* [ ] **Obsolescence / Suppresion** d'un concept

---

## 2. Description du Concept / de l'Entité

* **Nom du concept (Français) :** [ex: Vecteur d'Attaque]
* **Nom du concept (Anglais - Optionnel) :** [ex: Attack Vector]
* **Abreviation / Sigle :** [ex: VA]
* **Synonymes / Termes alternatifs :** [ex: Canal d'intrusion, Vecteur d'infection]

### Définition métier
> *Fournissez une définition claire et compréhensible par tous.*

[Inscrivez la définition détaillée ici...]

### Contexte & Justification
> *Pourquoi cette évolution est-elle nécessaire ? (ex: Nouvelle menace, alignement avec un standard, besoin d'analyse SOC)*

[Expliquez le contexte opérationnel ici...]

---

## 3. Positionnement dans le Graphe (Relations & Ontologie)

> *Renseignez les liens avec les concepts déjà existants dans le DKG.*

* **Catégorie / Domaine principal :** [ex: Menace / Technique / Asset / Vulnérabilité]
* **Est un sous-type de (Parent) :** [ex: Incident de Sécurité]
* **Est relié à (Autres concepts) :**
  * Est relié à : `[Nom d'un autre concept existant]` via la relation : `[ex: EXPLOITE / CIBLE / PROTEGE]`
  * Est relié à : `[Nom d'un autre concept existant]` via la relation : `[ex: APPARTIENT_A]`

---

## 4. Propriétés & Attributs requis (Optionnel)

> *Quelles informations clés doit-on pouvoir stocker sur ce concept ?*

* **Propriété 1 :** [ex: Niveau de sévérité (Élevé, Moyen, Faible)]
* **Propriété 2 :** [ex: Horodatage de première détection]
* **Propriété 3 :** [ex: Identifiant externe (CVE, MITRE ID)]

---

## 5. Espace de Validation & Registre (Réservé RSSI / Agent Guard)

<!-- Ne pas remplir cette section lors de la création de la demande -->

* **Analyse d'impact automatisée (Agent Guard) :**
  * *Conflit ou doublon détecté :* [Non / Oui - préciser]
  * *Fichiers TTL cibles impactés :* `[Chemin du fichier TTL]`

* **Avis du RSSI / DSI :**
  * [ ] Accepté tel quel
  * [ ] Accepté avec modifications
  * [ ] Refusé (Motif : [Indiquer la raison])

* **Signature / Approval :** [Nom du valideur] le [Date]