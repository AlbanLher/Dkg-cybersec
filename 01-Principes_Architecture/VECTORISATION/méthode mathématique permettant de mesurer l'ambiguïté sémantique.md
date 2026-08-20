Explique la méthode mathématique permettant de mesurer l'ambiguïté sémantique entre deux résultats vectoriels pour déclencher une demande de clarification.

Pour détecter formellement si la recherche vectorielle est dans une **zone d'incertitude (ambiguïté sémantique)**, on ne se contente pas d'examiner le score du meilleur résultat : on analyse la **distribution statistique** des K meilleurs candidats retournés par l'index.

Deux méthodes complémentaires permettent de mesurer cette ambiguïté et de déclencher automatiquement une demande de clarification auprès de l'utilisateur : **la Marge Cosinus relative** et **l'Entropie de Softmax**.

### 1. La Marge Cosinus Relative (Δs)

Lorsqu'une requête utilisateur q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​ est comparée aux vecteurs des candidats c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​, l'index vectoriel calcule des scores de similarité cosinus si​∈[−1,1] :

si​=cos(q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​,c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​)=∥q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​∥∥c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​∥q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​⋅c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​​

On trie les résultats par ordre décroissant de score : s1​≥s2​≥⋯≥sK​.

#### Formule de la Marge Relative

L'ambiguïté se caractérise par une différence très faible entre le meilleur résultat (s1​) et le second résultat (s2​). Pour être indépendant de l'échelle absolue des scores, on calcule la marge relative :

Δsrel​=s1​s1​−s2​​

#### Règle de Décision

Plaintext

```
               ┌────────────────────────────────────────┐
               │         Calcul de Δs_rel               │
               └───────────────────┬────────────────────┘
                                   │
         ┌─────────────────────────┴────────────────────────┐
         ▼                                                  ▼
[ Δs_rel ≥ θ_marge ]                                [ Δs_rel < θ_marge ]
 (ex: θ_marge = 0.15)                                (ex: Δs_rel < 15%)
         │                                                  │
         ▼                                                  ▼
 🎯 CAS CLAIR                                        ⚠️ ZONE D'AMBIGUÏTÉ
 Le candidat c_1 est nettement                       c_1 et c_2 sont trop proches.
 au-dessus. Sélection automatique.                   Déclencher la CLARIFICATION.
```

- **Si Δsrel​≥θmarge​** (ex: s1​=0.88,s2​=0.65⟹Δsrel​=26%) : La réponse c1​ est discriminée avec certitude.
    
- **Si Δsrel​<θmarge​** (ex: s1​=0.88,s2​=0.86⟹Δsrel​=2.2%) : Le système hésite entre deux notions sémantiquement proches.
    

### 2. L'Entropie de Shannon de la Distribution Softmax (H)

Si la requête est vague, le système peut hésiter non pas entre 2, mais entre K candidats (ex: 4 équipements ou logiciels ayant des scores similaires). Pour mesurer l'incertitude globale sur un ensemble de K candidats, on utilise **l'entropie de Shannon**.

#### Étape A : Normalisation par Softmax

On convertit les scores cosinus (s1​,s2​,…,sK​) en une distribution de probabilité P=(p1​,p2​,…,pK​) via une fonction Softmax pondérée par une température τ :

pi​=∑j=1K​esj​/τesi​/τ​

_(La température τ≈0.1 accentue les écarts pour isoler les candidats pertinents)._

#### Étape B : Calcul de l'Entropie

L'entropie H(P) quantifie le désordre ou l'incertitude de la distribution :

H(P)=−i=1∑K​pi​log2​(pi​)

Pour pouvoir comparer l'entropie indépendamment du nombre de candidats K, on calcule l'**Entropie Normalisée** Hnorm​∈[0,1] :

Hnorm​(P)=log2​(K)H(P)​

#### Règle de Décision par Entropie

- **Hnorm​→0 (Incertitude faible) :** La distribution est concentrée sur une seule entité (p1​≈1,p2​≈0). Aucune ambiguïté.
    
- **Hnorm​→1 (Incertitude maximale) :** La distribution est uniforme (p1​≈p2​≈⋯≈pK​). L'intention de l'utilisateur est totalement diffuse.
    

### 3. Algorithme de Fusion & Déclenchement de la Clarification

En pratique, on combine le seuil de Marge Relative (θmarge​) et le seuil d'Entropie Normalisée (θentropie​) :

Python

```
def check_semantic_ambiguity(
    scores: list[float],
    theta_marge: float = 0.12,
    theta_entropy: float = 0.65,
    tau: float = 0.1,
) -> bool:
    """Renvoie True si une demande de clarification doit être déclenchée."""
    if len(scores) < 2:
        return False

    # 1. Calcul de la marge relative
    s1, s2 = scores[0], scores[1]
    marge_rel = (s1 - s2) / s1 if s1 > 0 else 0

    # 2. Calcul de l'entropie normalisée
    exp_scores = [np.exp(s / tau) for s in scores]
    sum_exp = sum(exp_scores)
    probs = [p / sum_exp for p in exp_scores]

    h = -sum(p * np.log2(p) for p in probs if p > 0)
    h_norm = h / np.log2(len(scores))

    # 3. Déclenchement si l'une des conditions d'ambiguïté est remplie
    is_ambiguous = (marge_rel < theta_marge) or (h_norm > theta_entropy)

    return is_ambiguous
```

### Traitement en aval en cas d'ambiguïté

Lorsque `is_ambiguous == True`, le système stoppe la génération directe du RAG et construit la réponse de clarification en interrogeant le Graphe d'Ontologie :

1. Extraction des K nœuds candidats issus de la recherche vectorielle (`Tomcat-App`, `Tomcat-Service`).
    
2. Récupération de leurs propriétés discriminantes via Cypher (`labels()`, `environment`, `hostedOn`).
    
3. Génération dynamique de la question à l'utilisateur :
    
    > _"Votre requête correspond à 2 éléments distincts : **Apache Tomcat (Logiciel)** et **Tomcat-Admin (Service sur SRV-WEB-01)**. Lequel souhaitez-vous analyser ?"_
    

Explique la méthode mathématique permettant de mesurer l'ambiguïté sémantique entre deux résultats vectoriels pour déclencher une demande de clarification.

Pour mesurer formellement l'**ambiguïté sémantique** entre plusieurs résultats vectoriels (embeddings) et décider s'il faut déclencher une demande de clarification, on analyse la **distribution des scores de similarité** obtenus lors de la recherche vectorielle.

L'objectif est de dépasser la simple valeur absolue du meilleur score pour évaluer la **distance relative** et l'**incertitude globale** de la recherche. Deux méthodes complémentaires permettent de modéliser cette décision mathématique : **la Marge Cosinus Relative** (Δsrel​) et **l'Entropie Normalisée de Shannon** (Hnorm​).

### 1. La Marge Cosinus Relative (Δsrel​)

Lorsqu'une requête vectorisée q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​ est comparée aux vecteurs des entités de la base c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​, l'index (HNSW ou Flat) calcule des scores de similarité cosinus si​∈[−1,1] :

si​=cos(q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​,c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​)=∥q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​∥∥c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​∥q![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)​⋅c![](data:image/svg+xml;utf8,<svg%20xmlns="http://www.w3.org/2000/svg"%20width="0.471em"%20height="0.714em"%20style="width:0.471em"%20viewBox="0%200%20471%20714"%20preserveAspectRatio="xMinYMin"><path%20d="M377%2020c0-5.333%201.833-10%205.5-14S391%200%20397%200c4.667%200%208.667%201.667%2012%205%0A3.333%202.667%206.667%209%2010%2019%206.667%2024.667%2020.333%2043.667%2041%2057%207.333%204.667%2011%0A10.667%2011%2018%200%206-1%2010-3%2012s-6.667%205-14%209c-28.667%2014.667-53.667%2035.667-75%2063%0A-1.333%201.333-3.167%203.5-5.5%206.5s-4%204.833-5%205.5c-1%20.667-2.5%201.333-4.5%202s-4.333%201%0A-7%201c-4.667%200-9.167-1.833-13.5-5.5S337%20184%20337%20178c0-12.667%2015.667-32.333%2047-59%0AH213l-171-1c-8.667-6-13-12.333-13-19%200-4.667%204.333-11.333%2013-20h359%0Ac-16-25.333-24-45-24-59z"></path></svg>)i​​

Les résultats sont classés par ordre décroissant : s1​≥s2​≥⋯≥sK​.

#### Formule

L'ambiguïté directe entre le premier résultat (s1​) et le second (s2​) est mesurée par leur écart relatif :

Δsrel​=s1​s1​−s2​​

#### Règle de Décision

- **Si Δsrel​≥θmarge​** (ex: s1​=0.88,s2​=0.65⟹Δsrel​=26%) : Le candidat c1​ se détache nettement. L'intention est claire → **Pas de clarification**.
    
- **Si Δsrel​<θmarge​** (ex: s1​=0.88,s2​=0.86⟹Δsrel​=2.2%) : Les deux concepts sont géométriquement indifférenciables → **Déclenchement de la clarification**.
    

### 2. L'Entropie Normalisée de Shannon (Hnorm​)

Lorsque l'ambiguïté concerne non pas 2, mais K candidats (ex: 4 équipements réseau ou versions de logiciels ayant des vecteurs très proches), la marge relative ne suffit plus. On calcule l'**entropie** de la distribution pour mesurer l'incertitude globale de la réponse.

#### Étape A : Transformation Softmax

On transforme les K meilleurs scores cosinus (s1​,s2​,…,sK​) en une distribution de probabilité P=(p1​,p2​,…,pK​) via une fonction Softmax pondérée par un paramètre de température τ (généralement τ∈[0.05,0.2] pour accentuer le signal) :

pi​=∑j=1K​esj​/τesi​/τ​

#### Étape B : Calcul de l'Entropie Normalisée

L'entropie de Shannon quantifie le "désordre" de la distribution. On la divise par son maximum théorique (log2​(K)) pour obtenir une valeur Hnorm​∈[0,1] :

Hnorm​(P)=log2​(K)−∑i=1K​pi​log2​(pi​)​

#### Règle de Décision

- **Hnorm​→0 (Incertitude très faible) :** La probabilité est concentrée sur un seul nœud (p1​≈1).
    
- **Hnorm​→1 (Incertitude maximale / Équiprobabilité) :** Tous les candidats sont jugés équivalents par l'index vectoriel.
    
- **Si Hnorm​≥θentropie​** (ex: θentropie​=0.65), la recherche est considérée comme diffuse → **Déclenchement de la clarification**.
    

### 3. Implémentation Algorithmique (Python)

Ce bloc de contrôle intercepte les résultats vectoriels avant la génération de réponse par le LLM :

Python

```
import numpy as np

def evaluate_semantic_ambiguity(
    scores: list[float], 
    theta_marge: float = 0.12,   # 12% d'écart min requis entre top 1 et top 2
    theta_entropy: float = 0.65, # Seuil d'incertitude globale (0.0 à 1.0)
    tau: float = 0.1             # Température Softmax
) -> tuple[bool, dict]:
    """
    Évalue si la recherche vectorielle contient une ambiguïté sémantique.
    Retourne (is_ambiguous, métriques).
    """
    if len(scores) < 2:
        return False, {"reason": "Résultat unique"}

    s1, s2 = scores[0], scores[1]
    
    # 1. Calcul de la Marge Relative
    marge_rel = (s1 - s2) / s1 if s1 > 0 else 0.0

    # 2. Calcul du Softmax et de l'Entropie Normalisée
    exp_scores = np.exp(np.array(scores) / tau)
    probs = exp_scores / np.sum(exp_scores)
    
    # Entropie de Shannon
    entropy = -np.sum([p * np.log2(p) for p in probs if p > 0])
    max_entropy = np.log2(len(scores))
    h_norm = entropy / max_entropy if max_entropy > 0 else 0.0

    # 3. Decision
    is_ambiguous = (marge_rel < theta_marge) or (h_norm > theta_entropy)

    metrics = {
        "s1": s1,
        "s2": s2,
        "marge_relative": round(marge_rel, 4),
        "entropie_normalisee": round(h_norm, 4),
        "is_ambiguous": is_ambiguous
    }

    return is_ambiguous, metrics
```

### 4. Conjonction Vectoriel + Cypher pour la Clarification

Lorsque `is_ambiguous` vaut `True`, la chaîne RAG ne transmet pas un contexte tronqué au LLM. Elle exécute une requête Cypher ciblée sur les K candidats indifférenciés pour extraire leurs **propriétés discriminantes dans le graphe** (`environment`, `type`, `version`) afin de construire une question à choix multiple :

> **Exemple de sortie générée :**
> 
> _"Votre question concerne **Tomcat**, mais deux entités très proches ont été identifiées dans le graphe d'ontologie :_
> 
> 1. **Apache Tomcat (Software)** – Composant applicatif installé sur `SRV-WEB-01`.
>     
> 2. **Tomcat-Service (Service)** – Service système en DMZ.
>     
> 
> _Lequel de ces éléments souhaitez-vous analyser ?"_