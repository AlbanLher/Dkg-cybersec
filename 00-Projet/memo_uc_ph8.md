Mémoire Use Case (Phase 8)

    Intitulé du Cas d'Usage : Audit de conformité réglementaire et analyse de menaces incrémentaux en mode Air-Gapped.

    Scénario Métier :

        Un flux réglementaire massif (ex: exigences de l'Article 32 du RGPD) ou un flux de menaces CTI (TLP:CLEAR) arrive de l'extérieur.

        Au lieu de saturer le système ou de charger l'intégralité de la base, l'Agent Explorateur Externe applique un filtrage frugal (via le pipeline NER local) pour extraire uniquement le delta pertinent.

        L'Orchestrateur SOC fragmente la requête et interroge séquentiellement les sous-graphes internes correspondants (TLP:RED des actifs du foyer ou de l'entreprise) sans jamais saturer la mémoire vive (16 Go RAM).

        L'analyse croisée met en évidence une non-conformité ou un risque de rebond. L'Agent Gardien formule une proposition de modification ontologique ou une alerte.

        Contrôle HitM (Human-in-the-Middle) : L'analyste humain valide ou rejette la modification via une interface souveraine avant toute écriture définitive dans le graphe validé par contraintes SHACL.