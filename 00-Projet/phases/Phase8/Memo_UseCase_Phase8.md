# Memo_UseCase_Phase8.md — Gouvernance & Orchestration MCP (Scope : Actifs, Vulnérabilités et Menaces)


**Objectif Phase 8 :** Orchestration MCP de la gestion des menaces et des actifs (Groupe 1) appliquée à un environnement étendu (DMZ/Pare-feu/Postes) et pilotée par le simulateur d'empreinte pour tracer les abaques de performance _Green-by-Design_.


## 📖 1. L'Histoire Métier

Le SOC résidentiel pilote la gestion des menaces et des vulnérabilités via une architecture multi-agents collaborative et souveraine, circonscrite au **Groupe 1** :

1. **L'Agent Explorateur (Références Externes) :** Capture et filtre de manière frugale les flux de menaces publics et catalogues de référence (MITRE ATT&CK, CVE / _Les Communs_) sous forme de deltas minimes en **`TLP:CLEAR`**.
    
2. **Le Gardien de la TBox :** Analyse l'écart ontologique entre le dictionnaire de référence et les catalogues externes pour formuler une **proposition formelle d'enrichissement de la TBox**.
    
3. **L'Analyste (Human-in-the-Middle - HitM) :** Valide, amende ou rejette cette proposition d'alignement sémantique via le Dashboard Front-End.
    
4. **Confrontation ABox & Simulateur :** Une fois la TBox enrichie, le moteur de rapprochement croise ces menaces avec la cartographie réelle des actifs du foyer (**`TLP:RED`**), tandis que le simulateur évalue la charge et recherche les limites de performance (_Green-by-Design_).
    

## 🔄 2. Diagramme de Flux et des Artefacts (Mermaid)



```mermaid
sequenceDiagram
    autonumber
    actor Analyste as Analyste (HitM)
    participant MCP as mcp_server.py (MCP)
    participant Frugal as frugal_engine.py (Ext. Data)
    participant Guardian as tbox_guardian.py (Gardien TBox)
    participant MITM as mitm_engine.py (Rapprochement)
    participant Sim as simulator.py (Green-by-Design)

    Note over Analyste, Sim: Phase 8 - Scope Groupe 1 (Actifs, Vulnérabilités & Menaces)

    MCP->>Frugal: Déclenche la capture des sources publiques ("Les Communs")
    Frugal-->>MCP: Retourne le subset frugal (TLP:CLEAR)
    
    MCP->>Guardian: Soumet le subset pour analyse d'écart ontologique
    Guardian-->>MCP: Formule une proposition formelle d'enrichissement TBox
    
    MCP->>Analyste: Expose la proposition sur le Dashboard HitM
    Analyste->>MCP: Valide ou amende la proposition d'alignement
    
    MCP->>MITM: Lance le rapprochement sémantique (TBox enrichie vs ABox TLP:RED)
    MITM-->>MCP: Confirme l'alignement des menaces sur les actifs du foyer
    
    MCP->>Sim: Exécute le benchmark de charge (Green-by-Design)
    Sim-->>Analyste: Restitue les abaques de performance et le statut d'exécution
```
