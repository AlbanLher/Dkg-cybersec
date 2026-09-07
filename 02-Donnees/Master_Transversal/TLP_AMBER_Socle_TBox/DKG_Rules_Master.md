# Extrait Sémantique : DKG_Rules_Master.ttl
**Source** : `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_Rules_Master.ttl`  
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
| `RuleHighRiskAssetAssessment` | `type` | `NodeShape` |
| `RuleHighRiskAssetAssessment` | `rule` | `n5ce66cc7568442f9b440a6566ac570f5b1` |
| `n5ce66cc7568442f9b440a6566ac570f5b2` | `type` | `SPARQLRule` |
| `n5ce66cc7568442f9b440a6566ac570f5b2` | `construct` | `>

            CONSTRUCT {
                $this dkg:targetsAsset ?asset .
            }
            WHERE {
                $this dkg:targetsComponent ?component .
                ?asset dkg:hostsComponent ?component .
            }
        ` |
| `RuleThreatCampaignPropagation` | `rule` | `n5ce66cc7568442f9b440a6566ac570f5b2` |
| `RuleThreatCampaignPropagation` | `comment` | `Lie une campagne CTI externe à un actif interne hébergeant le composant visé.` |
| `n5ce66cc7568442f9b440a6566ac570f5b1` | `construct` | `>

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
| `RuleThreatCampaignPropagation` | `targetClass` | `ThreatCampaign` |
| `RuleHighRiskAssetAssessment` | `label` | `Règle R-01 : Évaluation Actif à Haut Risque (CISA KEV)` |
| `n5ce66cc7568442f9b440a6566ac570f5b1` | `type` | `SPARQLRule` |
| `RuleThreatCampaignPropagation` | `label` | `Règle R-02 : Propagation Cible de Campagne de Menace` |
| `RuleHighRiskAssetAssessment` | `targetClass` | `Asset` |