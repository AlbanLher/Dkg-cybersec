le fichier ./03-Application/config.py  reproduit une partie de cette architecture pour optimiser l'attention du medèle LLM qui assiste le développement. Ref [./03-Application/README.md](README_03-.md)


Suite au déplacement de script dans la /Phase/ qui avait été oublié le config n'était plus trouvé ! 
Pour le récupérer : 
```
# Import des constantes SSOT
import sys
from pathlib import Path

# Ajoute le dossier parent '03-Application' au sys.path
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Import propre depuis config.py
from config import (
    TBOX_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    RULES_MASTER_PATH,
    ABOX_INFERED_PATH,
    MODELS_DIR,
    EMBEDDING_MODEL_DIR,
    MITM_SIMILARITY_THRESHOLD,
    DKG,
    RDFS,
    DOC_INFERED_MD_PATH
)
```

