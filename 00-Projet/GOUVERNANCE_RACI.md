**Rôles identifiés :**

- **RSSI / Responsable Métier :** Valideur ultime des concepts métiers, des accès et des arbitrages de sécurité.
    
- **Architecte Ontologie / Data :** Garant de la structure logique, du nommage des Domaines et des schémas de données.
    
- **Agent Guard (IA / Pipeline CI) :** Contrôleur automatisé (parsing, détection de doublons, validation SHACL, compilation TTL/MD).
    
- **Contributeur (Analyste SOC / Dev / SecOps) :** Saisit les besoins d'évolution via Git Direct.
    

**Matrice RACI des opérations :**

| **Opération / Livrable**              | **Contributeur** | **Architecte** | **Agent Guard** | **RSSI / Lead** |
| ------------------------------------- | :--------------: | :------------: | :-------------: | :-------------: |
| **Proposition de terme/concept (MD)** |      **R**       |       I        |        A        |        C        |
| **Parsing & Contrôle de cohérence**   |        I         |       C        |    **R / A**    |        I        |
| **Validation / Merge de PR**          |        I         |       C        |        I        |    **R / A**    |
| **Création / Modif d'un Domaine**     |        C         |     **R**      |        A        |      **A**      |
| **Compilation du Vault TTL**          |        I         |       I        |    **R / A**    |        I        |
| **Régénération des MD d'exposition**  |        I         |       I        |    **R / A**    |        I        |

_(R = Realizes / Exécute, A = Approves / Valide, C = Consulted / Consulté, I = Informed / Informé)_