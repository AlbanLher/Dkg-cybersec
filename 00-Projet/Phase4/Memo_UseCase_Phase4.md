# 📘 Cas d'Usage Pédagogique — Phase 4 : Ingestion CTI Non Structurée via NER

> **Classification** : `TLP:CLEAR`  
> **Périmètre** : Renseignement Menace Externe / Analyste SOC & CTI  
> **Statut** : 🟢 Validé

---

## 🎯 1. Le Contexte Métier

Un bulletin d'alerte de sécurité sous forme de texte brut est publié par le **CERT-FR** concernant des cyberattaques en cours ciblées sur des infrastructures critiques. 

Au lieu de demander à un analyste SOC d'extraire et de saisir manuellement les éléments d'intérêt dans une base de données, le module **NER (Named Entity Recognition)** du DKG lit le bulletin textuel, identifie automatiquement les entités cyber clés et les intègre sous forme de graphe de connaissances exploitables.

---

## 📄 2. Le Document Source (Bulletin Brut)

> *"Le CERT-FR a observé une campagne d'attaque d'envergure ciblant les serveurs d'entreprises. L'acteur de menace **APT29** (aussi connu sous le nom Cozy Bear) exploite activement la vulnérabilité **CVE-2024-21887**. Les attaquants utilisent principalement la technique de **Spearphishing Link (T1566.002)** pour obtenir un accès initial."*

---

## 🤖 3. Ce que le Moteur NER a Compris & Structuré

Le pipeline NLP analyse le texte brut, attribue un **score de confiance (≥ 0.85)** à chaque détection, et traduit le récit en concepts formels pour le SOC :

* **Acteur de Menace (Threat Actor)** :  
  * *Entité* : `APT29` (Cozy Bear)  
  * *Confiance* : `0.98` (98%)  

* **Vulnérabilité Exploité (Vulnerability)** :  
  * *Entité* : `CVE-2024-21887`  
  * *Confiance* : `0.99` (99%)  

* **Technique d'Attaque (MITRE ATT&CK Pattern)** :  
  * *Entité* : `Spearphishing Link (T1566.002)`  
  * *Confiance* : `0.92` (92%)  

* **Relations Déduites** :  
  * `APT29` ➔ *exploite* ➔ `CVE-2024-21887`  
  * `APT29` ➔ *utilise la technique* ➔ `Spearphishing Link (T1566.002)`

---

## 🛡️ 4. Valeur Ajoutée pour le SOC & Prochaine Étape (Vague 3)

1. **Automatisation CTI** : Le graphe de menaces externes (`TLP:CLEAR`) est désormais enrichi instantanément sans intervention humaine.
2. **Préparation du Raisonnement (Phase 5)** : Le DKG sait maintenant que la vulnérabilité `CVE-2024-21887` est activement exploitée par `APT29`. Dès la Phase 5, le moteur de raisonnement croisera cette donnée externe avec l'inventaire interne (`TLP:RED`) pour alerter immédiatement le SOC si un équipement de l'entreprise utilise un composant vulnérable à cette CVE !