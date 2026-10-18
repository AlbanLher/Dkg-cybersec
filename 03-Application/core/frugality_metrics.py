# 03-Application/core/frugality_metrics.py
"""
ratio de frugalité, TOP entités par SPARQL. Lecture pure.
Extrait de api/routes_phase8.py lors du découpage v2 (logique inchangée).
Traçability: EXG-FWK-P8-AGE_2 GreenDev volumes chargés versus dispo, 
             EXG-TEC-P08-GR_1, + EXG-MET-P8-DEM_4c (exclusion .private/)
"""
import core.config as settings
from core.local_volumes import _read

def _generate_frugality_metrics(abox: str, cti: str) -> dict:
    """EXG-FWK-P8-AGE_2 — abaque Green-Dev : volumes chargés vs dispo.
    VOLUME CHARGÉ = ce que la session manipule réellement (workset TBox +
    ABox active + buffer CTI). VOLUME DISPONIBLE = l'intégralité du magasin
    de données (seeds + workset, .private/ exclu car TLP:RED). Le ratio
    démontre la frugalité : la démo charge une petite part du socle.
    TOP entités : les plus grosses instances du graphe actif, calculées
    par SPARQL (nb de triplets par sujet) — jamais de regex sur .ttl (GOU_22).
    """
    from rdflib import Graph, RDF, RDFS, Literal                        # AGE_2

    loaded = {
        "tbox_workset_bytes": len(_read(settings.WORKSET_TBOX_PATH).encode()),
        "abox_bytes": len(abox.encode()),
        "cti_bytes": len(cti.encode()),
        "rules_workset_bytes": len(_read(settings.WORKSET_RULES_PATH)
                                   .encode()) if settings.WORKSET_RULES_PATH.exists() else 0,
    }
    loaded_total = sum(loaded.values())

    # Volume disponible : magasin de données complet (seeds + workset),
    # fichiers .ttl uniquement (AGE_1) ; .private/ exclu (TLP:RED, DEM_4c).
    # Robustesse GOU_5 : AUCUN attribut de répertoire inventé — on dérive
    # les répertoires des chemins de FICHIERS garantis par la config, et
    # on déduplique (résolu) pour ne pas compter deux fois un même .ttl.
    _file_attrs = (                                                  # AGE_1
        "WORKSET_TBOX_PATH", "WORKSET_RULES_PATH",
        "WORKSET_CTI_BUFFER_PATH",
        "SEED_TBOX_PATH", "SEED_RULES_PATH",
        "SEED_ABOX_FOYER_PATH", "SEED_ABOX_HOTE_PATH",
    )
    seen, ttl_files = set(), []
    for attr in _file_attrs:
        p = getattr(settings, attr, None)
        if p is None or not getattr(p, "exists", lambda: False)():
            continue                       # attribut absent sur ce déploiement
        ttl_files.append(p)
        seen.add(p.resolve())
    for attr in _file_attrs:                                          # voisins .ttl
        p = getattr(settings, attr, None)
        if p is None or not p.exists():
            continue
        for f in p.parent.glob("*.ttl"):                             # même dossier
            if ".private" in f.parts:                                # DEM_4c
                continue
            if f.resolve() not in seen:
                seen.add(f.resolve())
                ttl_files.append(f)
    available_total = sum(f.stat().st_size for f in ttl_files)
    available_total = max(available_total, 1)

    # TOP entités : nb de triplets par sujet, graphe actif = ABox + CTI.
    g = Graph()
    parse_errors = []                                                 # AGE_2
    for src in (abox, cti):                                            # AGE_1
        if src.strip():
            try:
                g.parse(data=src, format="turtle")
            except Exception as exc:                                  # AGE_2
                parse_errors.append(str(exc)[:160])
    top = []
    for subj in set(g.subjects()):
        if isinstance(subj, Literal):  # v3.1 : URIRef/BNode SOUS-CLASSES de str !
            continue
        n = sum(1 for _ in g.predicate_objects(subj))
        label = g.value(subj, RDFS.label)
        name = str(label) if label else str(subj).split("#")[-1].split("/")[-1]
        top.append({"entity": name, "triplets": n})
    top.sort(key=lambda e: -e["triplets"])

    ratio = round(100.0 * loaded_total / available_total, 2)
    return {
        "loaded": loaded,                      # octets par volet
        "loaded_total_bytes": loaded_total,
        "available_total_bytes": available_total,
        "loaded_vs_available_pct": ratio,      # abaque Green-Dev (AGE_2)
        "top_entities": top[:5],               # fenêtre des cas conséquents
        "graph_parse_errors": parse_errors,    # AGE_2 — v3.1 : visibilité
        "graph_is_empty": len(g) == 0,          # AGE_2 — v3.1 : alarme didactique
    }
