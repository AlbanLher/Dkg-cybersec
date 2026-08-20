
**Pourquoi RDF/OWL est un Atout pour le NLP ?**

| Problème Classique en NLP    | Solution avec RDF/OWL                                                                      | Exemple                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Ambiguïté des termes**     | Les URIs uniques (`:Device`, `:Vulnerability`) **éliminent les ambiguïtés**.               | "Server" = `:InternalDevice` ou `:ExternalDevice` ? → L’ontologie le précise. |
| **Manque de contexte**       | Les **propriétés** (`:hasSoftware`, `:inContext`) **capturent les relations**.             | "CVSS 9.8" est lié à une `Vulnerability` → pas à un `Device`.                 |
| **Règles métier implicites** | Les **contraintes OWL** (`rdfs:subClassOf`, `owl:Restriction`) **explicitent les règles**. | "Un `InternalDevice` doit avoir un `cvssScore` ≤ 5."                          |
| **Évolution du domaine**     | Les **versions de l’ontologie** (Phase 0 → 1 → 2) **suivent l’évolution**.                 | Ajout de `:Context` en Phase 2 pour résoudre les contradictions.              |

---

### **📌 Méthode 1 : Utiliser l’Ontologie pour Guider la Vectorisation**

**Objectif** : **Enrichir les embeddings** (vecteurs) avec la **structure de l’ontologie**.

#### **🔧 Étapes avec Python (RDFLib + Sentence-Transformers)**

python

Copier

```
from rdflib import Graph
from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Chargez l'ontologie
g = Graph()
g.parse("03-Implementation/Phase1-Infrastructure/ONTOLOGIE/ontologie.ttl", format="turtle")

# 2. Extrayez les classes et propriétés
classes = [str(cls) for cls in g.subjects(RDF.type, OWL.Class)]
properties = [str(prop) for prop in g.subjects(RDF.type, OWL.ObjectProperty)]

# 3. Utilisez un modèle de vectorisation (ex: all-MiniLM-L6-v2)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 4. Vectorisez les classes/propriétés avec leur description
vectors = {}
for cls in classes:
    label = str(g.value(cls, RDFS.label)) or cls
    desc = str(g.value(cls, RDFS.comment)) or ""
    text = f"{label}: {desc}"
    vectors[cls] = model.encode(text)

# 5. Utilisez ces vecteurs pour enrichir vos données
# Exemple : Vectorisation d'une CVE avec son contexte ontologique
cve_text = "CVE-2023-1234: Vulnérabilité critique dans OpenSSL 1.0.2 (CVSS 9.8)"
cve_vector = model.encode(cve_text)

# Enrichissement avec les classes liées
linked_classes = [":Vulnerability", ":Software", ":InternalDevice"]
for cls in linked_classes:
    cve_vector += vectors[cls] * 0.1  # Pondération par la relation

# 6. Normalisez le vecteur final
cve_vector = cve_vector / np.linalg.norm(cve_vector)
```

**➡️ Résultat** :

- Les embeddings **intègrent la sémantique** de l’ontologie (ex: une CVE est liée à `Vulnerability`, `Software`, etc.).
- **Moins de faux positifs** : "OpenSSL" vectorisé avec `:Software` ≠ "OpenSSL" vectorisé avec `:Vulnerability`.

---

### **📌 Méthode 2 : Utiliser l’Ontologie pour le NER (Named Entity Recognition)**

**Objectif** : **Extraire des entités** (ex: `Device`, `Vulnerability`) depuis des textes **en utilisant l’ontologie comme référence**.

#### **🔧 Étapes avec spaCy + RDFLib**

python

Copier

```
import spacy
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, OWL, RDFS

# 1. Chargez l'ontologie
g = Graph()
g.parse("ontologie.ttl", format="turtle")

# 2. Extrayez les labels des classes
class_labels = {}
for cls in g.subjects(RDF.type, OWL.Class):
    label = g.value(cls, RDFS.label)
    if label:
        class_labels[str(label)] = str(cls)

# 3. Chargez un modèle spaCy (ex: fr_core_news_sm)
nlp = spacy.load("en_core_web_sm")

# 4. Ajoutez des règles de NER basées sur l'ontologie
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = []
for label, uri in class_labels.items():
    # Exemple : "OpenSSL" -> Software, "CVE-2023-1234" -> Vulnerability
    patterns.append({"label": label, "pattern": [{"TEXT": label}]})
ruler.add_patterns(patterns)

# 5. Appliquez le NER sur un texte
text = "Le device PC-Alban a une vulnérabilité CVE-2023-1234 avec OpenSSL 1.0.2."
doc = nlp(text)

# 6. Extrayez les entités avec leur type (basé sur l'ontologie)
for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_} (URI: {class_labels.get(ent.label_, 'Unknown')})")
    # Exemple : "CVE-2023-1234" -> "Vulnerability" (URI: :Vulnerability)
```

**➡️ Résultat** :

- Le NER **reconnaît automatiquement** les entités **liées à votre domaine** (ex: `Device`, `Vulnerability`).
- **Pas besoin de réentraîner** le modèle : l’ontologie **guide** le NER.

---

### **📌 Méthode 3 : Générer des Données d’Entraînement pour le NER**

**Objectif** : **Créer un jeu de données étiqueté** pour entraîner un modèle de NER **spécifique à votre domaine**.

#### **🔧 Script pour Générer des Exemples depuis l’Ontologie**

python

Copier

```
from rdflib import Graph
import json

g = Graph()
g.parse("ontologie.ttl", format="turtle")

# 1. Extrayez les classes et leurs labels
classes = {}
for cls in g.subjects(RDF.type, OWL.Class):
    label = g.value(cls, RDFS.label)
    if label:
        classes[str(cls)] = str(label)

# 2. Générez des exemples de phrases étiquetées
examples = []
for cls_uri, cls_label in classes.items():
    # Exemple 1 : "Le [Device] PC-Alban..."
    examples.append({
        "text": f"Le {cls_label} PC-Alban est vulnérable.",
        "entities": [[3, 3 + len(cls_label), cls_label]]
    })
    # Exemple 2 : "[Vulnerability] CVE-2023-1234..."
    examples.append({
        "text": f"{cls_label} CVE-2023-1234 a un score CVSS élevé.",
        "entities": [[0, len(cls_label), cls_label]]
    })

# 3. Sauvegardez au format spaCy
with open("ner_training_data.json", "w") as f:
    json.dump({"train": examples}, f)
```

**➡️ Résultat** :

- Un **jeu de données étiqueté** pour entraîner un modèle de NER **spécifique à la cybersécurité**.
- Le modèle **apprendra** à reconnaître `Device`, `Vulnerability`, etc., **dans leur contexte**.

---

### **📌 Méthode 4 : Utiliser l’Ontologie pour la Classification de Textes**

**Objectif** : **Classer automatiquement des textes** (ex: emails, logs) selon les **classes de l’ontologie**.

#### **🔧 Étapes avec HuggingFace + RDFLib**

python

Copier

```
from transformers import pipeline
from rdflib import Graph

# 1. Chargez l'ontologie
g = Graph()
g.parse("ontologie.ttl", format="turtle")

# 2. Extrayez les descriptions des classes
class_descriptions = {}
for cls in g.subjects(RDF.type, OWL.Class):
    label = g.value(cls, RDFS.label)
    desc = g.value(cls, RDFS.comment) or ""
    if label:
        class_descriptions[str(label)] = str(desc)

# 3. Chargez un modèle de classification (ex: zero-shot)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 4. Classez un texte selon les classes de l'ontologie
text = "Une faille critique a été détectée dans le serveur de production."
candidate_labels = list(class_descriptions.keys())  # ["Device", "Vulnerability", ...]

result = classifier(text, candidate_labels)
print(result)
# Exemple de sortie :
# {
#   'labels': ['Vulnerability', 'Device', 'Threat'],
#   'scores': [0.95, 0.87, 0.82]
# }
```

**➡️ Résultat** :

- Le texte est **classé automatiquement** dans les catégories de votre ontologie.
- **Pas besoin de réentraîner** : le modèle **générique** (BART) utilise les **descriptions de l’ontologie** pour classer.




### synthese

| **Votre Question**                       | **Réponse**                                                                                           | **Exemple Concret**                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Comment améliorer la vectorisation ?** | Utilisez l’ontologie pour **enrichir les embeddings** (ajoutez la sémantique des classes/propriétés). | Vectorisez "CVE-2023-1234" avec les vecteurs de `:Vulnerability`, `:Software`, etc. |
| **Comment améliorer le NER ?**           | Utilisez l’ontologie comme **référence** pour étiqueter les entités (ex: `Device`, `Vulnerability`).  | spaCy + règles basées sur les labels de l’ontologie.                                |
