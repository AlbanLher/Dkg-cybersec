Ce projet est aussi une occasion d'apprendre a travailler avec les LLM. Il faut veiller a un langage efficace (TSV, YML) qui permet d'optimiser l'attention (jetons) et minimiser le bruit. 
Par ailleur il faut combiner vue d'ensemble et de détail par des prompt permanent et prompt de context.
Il ne faut pas hésiter a ouvrir une nouvelle discussion pour s'affranchir de bruit généré par un volume d'échange sur un sujet trés spécifique.

voici quelques éléments résultant du retour d'expérience

## 1 - les Prompts
point d'entrée les prompt.

### 2 - Les kits d'Amorçage

Les Kit d'amorçage, sont des documents générés en fin de phase, ayant l'objectif de faire une synthèse cumulative permettant à une nouvelle discussion , d'apporter le contexte nécessaire au travail des phases suivantes.
Il rappel en outre la vision stratégique





### 3 - La spec condensée format TSV  _( Tab-Separated Values )_
En tant que projt spec driven, il est pertinent de s'assurer que les spec sont prise en compte par le LLM lors des échanges.
copier l'ensemble des md SPEC serait d'une part trop consommateur en token et d'autre part trop bruité par de la synthaxe inutile.
Une solution consiste a utiliser les capacité d'obsidian pour agglomérer les spec en fournissant un mapping et une liste d'exigence, cela dans un format minimal. le TSV _Tab-Separated Values_. Le gain est estimé à prés de 70%
 les deux tables TSV sont a intégrer au prompt lors d'une nouvelle discussion  