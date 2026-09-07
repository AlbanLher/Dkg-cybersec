# Extrait Sémantique : DKG_Rules_Master.ttl
**Source** : `02-Donnees/Snapshots_Phases/Phase1_Socle/DKG_Rules_Master.ttl`  
**Nombre total de triplets** : `13`  

---
## 1. Classes déclarées
_Aucune classe explicitement déclarée._

## 2. Propriétés
_Aucune propriété explicitement déclarée._

## 3. Échantillon de Triplets (Top 20)
| Sujet | Prédicat | Objet |
| :--- | :--- | :--- |
| `RuleThreatCampaignPropagation` | `type` | `NodeShape` |
| `nd97c7de056dc4bd1a8bf5ec3688607f0b1` | `type` | `SPARQLRule` |
| `nd97c7de056dc4bd1a8bf5ec3688607f0b2` | `type` | `SPARQLRule` |
| `nd97c7de056dc4bd1a8bf5ec3688607f0b2` | `construct` | `>

            CONSTRUCT {
                $this dkg:targetsAsset ?asset .
            }
            WHERE {
                $this dkg:targetsComponent ?component .
                ?asset dkg:hostsComponent ?component .
            }
        ` |
| `RuleHighRiskAssetAssessment` | `type` | `NodeShape` |
| `RuleThreatCampaignPropagation` | `rule` | `nd97c7de056dc4bd1a8bf5ec3688607f0b2` |
| `nd97c7de056dc4bd1a8bf5ec3688607f0b1` | `construct` | `>

            CONSTRUCT {
                $this a dkg:HighRiskAsset ;
                      dkg:hasRiskScore "9.5"^^xsd:float .
            }
            WHERE {
                $this dkg:hasInstalledComponent ?component .
                ?component dkg:hasVulnerability ?cve .
                ?cve dkg:isCisaKev true .
            }
        ` |
| `RuleThreatCampaignPropagation` | `comment` | `Lie une campagne CTI externe à un actif interne hébergeant le composant visé.` |
| `RuleThreatCampaignPropagation` | `targetClass` | `ThreatCampaign` |
| `RuleHighRiskAssetAssessment` | `label` | `Règle R-01 : Évaluation Actif à Haut Risque (CISA KEV)` |
| `RuleThreatCampaignPropagation` | `label` | `Règle R-02 : Propagation Cible de Campagne de Menace` |
| `RuleHighRiskAssetAssessment` | `targetClass` | `Asset` |
| `RuleHighRiskAssetAssessment` | `rule` | `nd97c7de056dc4bd1a8bf5ec3688607f0b1` |