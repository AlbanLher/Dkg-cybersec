Ce repertoire rassemble les Spécifications considérées utiles pour le Framework mais aussi celles complétée pour la mise en application sur le cas d'usage Cyber SOC, respectivement dans les sous-répertoires : 
- **`./Specification_Framework/`**  et
- **`./Specification_UseCase/`**

A noter que les spécifications UseCase ne font que compléter les spécification UseCase.

📐 RÈGLE STRICTE DE NOMMAGE ET NUMÉROTATION DES SPÉCIFICATIONS (01-Principes_Spécifications/) :

1. ARBORESCENCE OBLIGATOIRE :
   - 01-Principes_Spécifications/TRANSVERSAL/ (Socles, TBox, SHACL, Règlements)
   - 01-Principes_Spécifications/USECASE_METIER/ (Vision fonctionnelle SOC / Métier)
   - 01-Principes_Spécifications/USECASE_TECHNIQUE/ (Implémentations, APIs, Agents)

2. RÈGLES DE NUMÉROTATION & MAPPING PHASE/UC :
   - Fichiers Transversaux : SPEC-SOCLE-XX_<Libellé>.md
   - Fichiers Métiers : SPEC-METIER-UCXX_<Libellé>.md (UC = Use Case Métier)
   - Fichiers Techniques de Phase : SPEC-TECH-PXX_<Libellé>.md (PXX = Numéro de Phase active)
   - En cas d'écart entre le numéro du Cas d'Usage Métier (UC) et le numéro de Phase (P), le prefixe 'PXX' prévaut pour identifier la Phase de livraison dans USECASE_TECHNIQUE/.

3. INTERDICTION : Aucun fichier markdown de spécification ne doit être créé à la racine de 01-Principes_Spécifications/.

