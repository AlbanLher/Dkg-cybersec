# 03-Application/core/mermaid_views.py
"""
Générateurs des vues Mermaid (EXG-MET-P8-DEM_4b) : classDiagram TBox
(promotion des classes du delta HITL), classDiagram ABox, superposition
verticale TLP:RED/TLP:CLEAR par alerte. Présentation PURE — aucun état,
aucune écriture (DEM_3). Extrait de api/routes_phase8.py (v2, inchangé).
Traçability: EXG-MET-P8-DEM_4b, EXG-MET-P8-DEM_4a (vue graphique)
"""
import re

import core.config as settings
from core.local_volumes import _load_abox_by_mode, _read
from core.hitm_gateway import ensure_workset_initialized

def _sanitize(s) -> str:
    """Assainit pour injection dans un classDiagram Mermaid (labels + erreurs)."""
    return (str(s).replace('"', "'").replace(":", " ").replace("\n", " ")
            .replace("\r", " ").replace("{", "(").replace("}", ")").strip()[:200])


def tbox_graph_mermaid() -> dict:
    """Vue classDiagram de la TBox workset — corps de /tbox/graph."""
    from rdflib import Graph, RDF, OWL, RDFS
    ensure_workset_initialized()
    try:
        g = Graph()
        g.parse(settings.WORKSET_TBOX_PATH, format="turtle")
    except Exception as e:
        return {"mermaid": 'classDiagram\n    class ERREUR_PARSE_TBOX\n'
                f'    ERREUR_PARSE_TBOX : +cause "{_sanitize(e)}"'}
    def localname(u):
        s = str(u)
        return s.split("#")[-1].split("/")[-1] if "#" in s or "/" in s else s
    classes, members, relations = set(), [], []
    for c in g.subjects(RDF.type, OWL.Class):
        n = localname(c)
        if n and n[0].isupper():
            classes.add(n)
    for p in g.subjects(RDF.type, OWL.DatatypeProperty):
        dom, rng = g.value(p, RDFS.domain), g.value(p, RDFS.range)
        if dom is not None and rng is not None:
            members.append(f"    {localname(dom)} : +{localname(p)} "
                           f"{localname(rng).replace('XMLSchema#','xsd:')}")
    for p in g.subjects(RDF.type, OWL.ObjectProperty):
        dom, rng = g.value(p, RDFS.domain), g.value(p, RDFS.range)
        if dom is not None and rng is not None:
            # GOU_22 (pédagogie du recallage) : les classes du delta HITL
            # (ex. ThreatActor/DeviceCategory amenées par targetsDevice)
            # n'existent que comme domain/range — on les PROMEUT en classes
            # du diagramme, sinon le recallage validé resterait invisible.
            d, r = localname(dom), localname(rng)
            classes.add(d)
            classes.add(r)
            relations.append(f'    {d} "*" --> "1" {r} : {localname(p)}')
    body = "\n".join([f"    class {c}" for c in sorted(classes)] + members + relations)
    return {"mermaid": "classDiagram\n" + body + "\n"}



def abox_graph_mermaid(mode: str) -> dict:
    """Vue classDiagram de l'ABox du terrain — corps de /abox/graph."""
    from rdflib import Graph, RDF, RDFS
    abox_ttl = _load_abox_by_mode(mode)
    if abox_ttl.startswith("# File not found") or not abox_ttl.strip():
        return {"mermaid": 'classDiagram\n    class ABOX_INTROUVABLE\n'
                f'    ABOX_INTROUVABLE : +mode "{mode}"'}
    try:
        g = Graph()
        g.parse(data=abox_ttl, format="turtle")
    except Exception as e:
        cause = _sanitize(e)
        return {"mermaid": "classDiagram\n    class ERREUR_PARSE_ABOX\n"
                f"    ERREUR_PARSE_ABOX : +cause \"{cause}\"\n"
                "    note for ERREUR_PARSE_ABOX \"Corriger le prefixe manquant dans le ttl\""}
    def ln(u):
        s = str(u); return s.split("#")[-1].split("/")[-1]
    instances, seen = [], set()
    for cls in sorted(set(g.objects(None, RDF.type)), key=str):
        cn = ln(cls)
        if not cn or not cn[0].isupper():
            continue
        if cn not in seen:
            seen.add(cn)
            instances.append(f"    class {cn}")
        for inst in sorted(set(g.subjects(RDF.type, cls)), key=str):
            label = g.value(inst, RDFS.label)
            name = _sanitize(label) if label else _sanitize(ln(inst))
            instances.append(f'    {cn} : +"{name}"')
    return {"mermaid": "classDiagram\n" + "\n".join(instances) + "\n"}



def _generate_superposition_mermaid(abox: str, cti: str, equipment: str) -> str:
    """EXG-MET-P8-DEM_4b : chaîne de raisonnement VERTICALE de l'alerte :
    Asset (TLP:RED) -> composant -> vulnérabilité -> faiblesse, reliée au
    fonds CTI externe (TLP:CLEAR) via skos:exactMatch. Tout est SPARQL sur
    graphe (EXG-FWK-P8-AGE_1) ; un lien CTI non déclaré en TBox porte ⚠️
    (EXG-FWK-P1-GOU_22) — la rupture de raisonnement d'un rejet y est visible.
    EXG-CONF_1 : l'ABox reçue contient déjà les findings de CONFRONTATION_1
    (produits par _load_abox_by_mode quand le CTI est coché) : la chaîne
    rouge -> vert s'affiche nativement, sans code dédié ici."""
    from rdflib import Graph, RDF, RDFS, Namespace
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

    def ln(u):
        s = str(u)
        return s.split("#")[-1].split("/")[-1]

    g = Graph()                                                        # AGE_1
    try:
        g.parse(data=abox, format="turtle")                            # AGE_1
    except Exception as e:
        return 'flowchart TD\n    ERR["⚠️ ABox non parsable — ' + _sanitize(e) + '"]'

    # 1. Actif ciblé : label exact, puis localname, puis repli approché (AGE_1)
    asset = None
    for s in g.subjects(RDF.type, DKG.Asset):
        label = str(g.value(s, RDFS.label) or "")
        if label == equipment or ln(s) == equipment:
            asset = s
            break
    if asset is None:
        for s in g.subjects(RDF.type, DKG.Asset):
            label = str(g.value(s, RDFS.label) or ln(s))
            if equipment and equipment.lower() in label.lower():
                asset = s
                break
    if asset is None:
        return ('flowchart TD\n    NF["Aucun actif trouvé pour : '
                + _sanitize(equipment)
                + ' — cliquez [Vue superposition] depuis une carte du bilan."]')

    # 2. Vocabulaire déclaré dans la TBox de référence (workset) — GOU_22
    tbox_ref = _read(settings.WORKSET_TBOX_PATH)                      # GOU_22
    declared = set(re.findall(r"^dkg:([a-z]\w+)\s+a\s+owl:(?:Object|Datatype)Property",
                              tbox_ref, flags=re.M))                  # GOU_22

    # 3. Fonds CTI coché (buffer workset) — TLP:CLEAR                 # AGE_1
    g_cti = Graph()
    if cti.strip():
        try:
            g_cti.parse(data=cti, format="turtle")                    # AGE_1
        except Exception:
            g_cti = Graph()

    # 4. Construction des nœuds/arêtes : internes = rouge, CTI = vert (DEM_4b)
    nodes, edges = [], []  # (id, texte, classe) / (src, label, dst, pointillé)
    a_label = _sanitize(g.value(asset, RDFS.label) or ln(asset))
    nodes.append(("A0", f"🖥️ TLP:RED · Asset<br/>{a_label}", "intern"))
    for svc in sorted(set(g.objects(asset, DKG.exposesService)), key=str):
        sid = f"S{len(nodes)}"
        nodes.append((sid, f"🖥️ TLP:RED · Service exposé<br/>{_sanitize(svc)}", "intern"))
        edges.append(("A0", "exposesService", sid, False))
    for comp in sorted(set(g.objects(asset, DKG.hasInstalledComponent)), key=str):
        cid = f"C{len(nodes)}"
        cname = _sanitize(g.value(comp, RDFS.label) or ln(comp))
        cver = _sanitize(g.value(comp, DKG.version) or "")
        nodes.append((cid, f"🖥️ TLP:RED · Composant<br/>{cname} {cver}".strip(), "intern"))
        edges.append(("A0", "hasInstalledComponent", cid, False))
        for vuln in sorted(set(g.objects(comp, DKG.hasVulnerability)), key=str):
            vid = f"V{len(nodes)}"
            vname = _sanitize(g.value(vuln, RDFS.label) or ln(vuln))
            score = g.value(vuln, DKG.cvssScore)
            score_txt = f" — CVSS {score}" if score else ""
            nodes.append((vid, f"🖥️ TLP:RED · Vulnérabilité<br/>{vname}{score_txt}", "intern"))
            edges.append((cid, "hasVulnerability", vid, False))
            # Superposition : correspondant externe du fonds CTI (TLP:CLEAR)
            ext = None
            for m in g.objects(vuln, SKOS.exactMatch):
                ext = m
                break
            if ext is None:
                cve = g.value(vuln, DKG.cveId)
                if cve is not None:
                    for s2 in g_cti.subjects(DKG.cveId, None):
                        if str(g_cti.value(s2, DKG.cveId)) == str(cve):
                            ext = s2
                            break
            if ext is not None:
                xid = f"X{len(nodes)}"
                nodes.append((xid, f"🌐 TLP:CLEAR · CTI externe<br/>{_sanitize(ln(ext))}", "extern"))
                edges.append((vid, "skos:exactMatch", xid, True))
                for w in sorted(set(g_cti.objects(ext, DKG.exploitsWeakness)), key=str):
                    warn = "" if "exploitsWeakness" in declared \
                        else " ⚠️ non déclarée en TBox"                # GOU_22
                    yid = f"Y{len(nodes)}"
                    nodes.append((yid, f"🌐 TLP:CLEAR · Faiblesse CTI<br/>{_sanitize(ln(w))}", "extern"))
                    edges.append((xid, f"exploitsWeakness{warn}", yid, True))
            for w in sorted(set(g.objects(vuln, DKG.hasWeakness)), key=str):
                wid = f"W{len(nodes)}"
                nodes.append((wid, f"🖥️ TLP:RED · Faiblesse<br/>{_sanitize(ln(w))}", "intern"))
                edges.append((vid, "hasWeakness", wid, False))

    # 4b. Acteurs de menace du volume CTI (DEM_4b — maillon « qui nous veut »)
    #     ThreatActor --targetsDevice--> DeviceCategory, rapproché de l'actif
    #     local par rapprochement sémantique (catégorie/service exposé — la
    #     liaison formelle actif↔catégorie est une candidate Gardien ABox §37 :
    #     elle n'existe PAS encore dans le graphe, d'où le pointillé).
    for actor in sorted(set(g_cti.subjects(RDF.type, DKG.ThreatActor)), key=str):
        aname = _sanitize(g_cti.value(actor, RDFS.label) or ln(actor))
        aid = f"T{len(nodes)}"
        nodes.append((aid, f"🌐 TLP:CLEAR · Acteur de menace<br/>{aname}", "extern"))
        for dev in sorted(set(g_cti.objects(actor, DKG.targetsDevice)), key=str):
            warn = "" if "targetsDevice" in declared \
                else " ⚠️ non déclarée en TBox"                        # GOU_22
            did = f"D{len(nodes)}"
            dlabel = _sanitize(g_cti.value(dev, RDFS.label) or ln(dev))
            nodes.append((did, f"🌐 TLP:CLEAR · Catégorie visée<br/>{dlabel}", "extern"))
            edges.append((aid, f"targetsDevice{warn}", did, True))
        # Rapprochement sémantique menace <-> notre actif (implicite §37).
        # NOTE Mermaid : un label d'ARÊTE (entre pipes) ne tolère NI <br/>
        # NI parenthèses — texte plat uniquement.
        edges.append((aid, "rapprochement sémantique — service/catégorie exposés", "A0", True))

    # 5. Nature de la liaison (DEM_4 + §37.2) : formelle si le graphe relie
    # explicitement l'actif à une vulnérabilité (chain SPARQL) ; implicite
    # si la chaîne s'arrête au littéral exposesService (mot-clé).
    # GOU_22 (pédagogie du REJET) : si une arête CTI porte ⚠️ (prédicat non
    # validé en TBox), la liaison est PARTIELLE — le finding de confrontation
    # reste formel, mais l'intégration de la connaissance externe est
    # bloquée en attendant la gouvernance HITL. On ne déclare PAS « formelle »
    # une chaîne dont un maillon CTI est non raisonné.
    has_formal_vuln = any(nid.startswith("V") for nid, _, _ in nodes)
    has_rejected_link = any("⚠️" in lbl for _, lbl, _, _ in edges)
    lines = ["flowchart TD"]
    if has_formal_vuln and has_rejected_link:
        lines.append('    L0["⚠️ LIAISON PARTIELLE — finding de confrontation formel, '
                     'mais raisonnement CTI incomplet : prédicat(s) non validés en TBox '
                     '(GOU_22 — approuver le delta pour compléter la chaîne)"]:::implicit')
    elif has_formal_vuln:
        lines.append('    L0["✓ LIAISON FORMELLE — raisonnement SPARQL sur le graphe"]:::formal')
    else:
        lines.append('    L0["⚠️ LIAISON IMPLICITE — détection par mot-clé, lien ABox↔CTI non formalisé (candidate Gardien ABox §37)"]:::implicit')
    for nid, txt, cls in nodes:
        lines.append(f'    {nid}["{txt}"]:::{cls}')
    for src, lbl, dst, dashed in edges:
        arrow = "-.->" if dashed else "-->"
        lines.append(f"    {src} {arrow}|{lbl}| {dst}")
    lines.append("    classDef intern fill:#450a0a,stroke:#f43f5e,color:#ffe4e6")
    lines.append("    classDef extern fill:#052e16,stroke:#10b981,color:#d1fae5")
    lines.append("    classDef formal fill:#052e16,stroke:#34d399,color:#d1fae5")
    lines.append("    classDef implicit fill:#450a0a,stroke:#fb7185,color:#ffe4e6")
    return "\n".join(lines) + "\n"
