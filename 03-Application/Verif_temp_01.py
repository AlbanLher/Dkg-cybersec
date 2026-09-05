from config import TBOX_MASTER_PATH, SHACL_MASTER_PATH
from rdflib import Graph, Namespace, RDF, OWL, SH

g_tbox = Graph().parse(str(TBOX_MASTER_PATH), format='ttl')
g_shacl = Graph().parse(str(SHACL_MASTER_PATH), format='ttl')

tbox_cls = set(g_tbox.subjects(RDF.type, OWL.Class))
shacl_targets = set(g_shacl.objects(None, SH.targetClass))

print('Classes TBox :', tbox_cls)
print('Cibles SHACL :', shacl_targets)
print('Intersection :', tbox_cls.intersection(shacl_targets))

