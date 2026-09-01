**Cas d'Usage & Scénario d'Attaque : Le "Fil Rouge" DKG-CyberSec**

## 🎯 Objectif Pédagogique & Opérationnel
Servir de **fil rouge narratif** pour tester, valider et démontrer les capacités de l'Agent IA SOC à chaque étape du projet (TBox, ABox, Superposition CTI, Inférence et GraphRAG).

---

## 🎭 L'Histoire : Attaque "Silent Cascade" sur l'Infrastructure Métier

### 🏢 Le Contexte (`TLP:RED` - Cartographie Interne)
L'entreprise opère un serveur critique nommé **`Serv-Prod-01`**, hébergeant l'application de transaction financière de l'entreprise. Ce serveur tourne sous un serveur Web **`Apache HTTP Server 2.4.49`**.

### ⚠️ L'Événement & La Menace (`TLP:CLEAR` - CTI Externe)
1. Le centre de veille (CTI) identifie une vulnérabilité critique publique : **`CVE-2021-41773`** touchant exactement la version Apache 2.4.49.
2. Cette faille repose sur un défaut de neutralisation de chemin (**`CWE-22` : Path Traversal**).
3. Le catalogue d'attaques recense le schéma d'exploitation associatif (**`CAPEC-126` : Directory Traversal**).
4. La base **CISA KEV** (Known Exploited Vulnerabilities) classe cette CVE comme **activement exploitée dans la nature** par des groupes criminels.

---

## 🧬 Alignement des Données avec l'Histoire (Graphe de Faits)

Cette histoire s'incarne directement dans les instances du Knowledge Graph par la chaîne de liaisons sémantiques suivante :

```mermaid
graph TD
    subgraph Infrastructure_Interne [TLP:RED - Seuil Confidentiel]
        Asset["dkg-data:Serv-Prod-01<br/>(Asset)"] -->|hasInstalledComponent| Comp["dkg-data:Apache-2.4.49<br/>(SoftwareComponent)"]
    end

    subgraph CTI_Mondiale [TLP:CLEAR - Référentiels Publics]
        Comp -->|hasVulnerability| CVE["dkg-data:CVE-2021-41773<br/>(Vulnerability)"]
        CVE -->|exploitsWeakness| CWE["dkg-data:CWE-22<br/>(Weakness)"]
        CWE -->|hasThreatPattern| CAPEC["dkg-data:CAPEC-126<br/>(ThreatPattern)"]
    end

    subgraph Inférence_Raisonnement [TLP:AMBER - Déductions Agent]
        CVE -.->|CISA KEV Active| Risk["dkg:HighRiskAsset<br/>(Tag Inferred)"]
        Risk -.-> Asset
    end

    style Infrastructure_Interne fill:#ffebee,stroke:#c62828
    style CTI_Mondiale fill:#e8f5e9,stroke:#2e7d32
    style Inférence_Raisonnement fill:#fff3e0,stroke:#ef6c00
````

## 🤖 Rôle du Scénario selon les Vagues de la Roadmap

| **Vague Projet**                 | **Comportement de l'Agent IA SOC sur ce Scénario**                                                                                                                                                                                                       |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vague 1 (Base ABox)**          | L'Agent sait que `Serv-Prod-01` héberge `Apache 2.4.49` et que ce dernier porte `CVE-2021-41773`.                                                                                                                                                        |
| **Vague 2 (Superposition CTI)**  | L'Agent croise `CVE-2021-41773` avec les bulletins externes et découvre qu'elle est listée dans **CISA KEV** et liée au **CAPEC-126**.                                                                                                                   |
| **Vague 3 (Raisonnement)**       | Le moteur de règles déduit automatiquement que `Serv-Prod-01` devient un **`HighRiskAsset`** (Calcul d'impact automatique).                                                                                                                              |
| **Vague 4 (GraphRAG / Copilot)** | L'analyste demande : _"Quel est le risque sur Serv-Prod-01 ?"_--> L'Agent répond : _"Serv-Prod-01 est à HAUT RISQUE. Son composant Apache 2.4.49 souffre de la CVE-2021-41773 (Path Traversal CWE-22 / CAPEC-126), activement exploitée selon la CISA."_ |
| **Vague 5 (SOAR / Autonomie)**   | L'Agent génère une règle Sigma de détection de traversée de répertoire (`/icons/..%2f`) et propose d'isoler le flux Web de `Serv-Prod-01`.                                                                                                               |
