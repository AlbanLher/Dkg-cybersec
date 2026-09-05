

Une rupture de cohérence sémantique dans un projet Ontologie/Knowledge Graph est un facteur critique : si l'inférence ou l'agent NER génère des prédicats fantômes (`dkg:hostsComponent` au lieu de `dkg:hasInstalledComponent`, `dkg:Component` au lieu de `dkg:SoftwareComponent`, ou des URIs isolées dans des namespaces divergents comme `.../data/` vs `.../data#`), la valeur sémantique du graphe s'effondre.

Pour stopper cette dérive et garantir que **la TBox Master reste la source unique de vérité (Single Source of Truth)**, un audit rigoureux du décalage s'impose, suivi du verrouillage de la chaîne de validation.

### Audit des Écarts : TBox Socle vs Dérives Phase 5

|**Élément**|**Socle Canonique (DKG_TBox_Master.ttl)**|**Dérives Identifiées (Phase 5 / Rules / NER)**|**Impact**|
|---|---|---|---|
|**Classe Composant**|`dkg:SoftwareComponent`|`dkg:Component`|Inférence muette (TargetShape invalide)|
|**Prédicat Hôte**|`dkg:hasInstalledComponent`|`dkg:hostsComponent`|Rupture de la chaîne de jointure SPARQL|
|**Prédicat Inverse**|`dkg:isComponentOf`|`dkg:isInstalledComponentOf`|Duplication de prédicats non reconnus|
|**Propriété KEV**|`dkg:isCisaKev`|`dkg-cti:isCisaKevListed`|Échec du filtre SPARQL CONSTRUCT|
|**URI Namespace**|`[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)`|`.../schema#`, `.../data/`, `.../cti#`|Graphe fragmenté en sous-graphes orphelins|