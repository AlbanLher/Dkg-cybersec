"""
03-Application/hitm_gateway.py
Passerelle Human-in-the-Middle (HitM) souveraine (Phase 8).
"""

import os
from pathlib import Path

def request_human_validation(delta_path: Path) -> bool:
    """
    Soumet le delta généré à l'analyste humain pour validation souveraine.
    En mode test automatisé (variable d'environnement HITM_AUTO_APPROVE=1), l'approbation est automatique.
    """
    print(f"\n[HitM Gateway] === CONTRÔLE HUMAIN REQUIS ===")
    print(f"[HitM Gateway] Analyse du fichier de delta : {delta_path}")
    
    # Mode CI / Test automatique
    if os.getenv("HITM_AUTO_APPROVE") == "1":
        print("[HitM Gateway] Mode automatique activé (CI/Test) -> Validation accordée.")
        return True

    # Mode interactif CLI
    response = input("[HitM Gateway] Souhaitez-vous valider l'injection de ce delta dans le graphe sécurisé ? (oui/non) : ").strip().lower()
    if response in ["oui", "o", "yes", "y"]:
        print("[HitM Gateway] Validation accordée par l'analyste.")
        return True
    else:
        print("[HitM Gateway] Rejet de la modification par l'analyste.")
        return False