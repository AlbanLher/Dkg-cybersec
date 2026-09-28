"""
03-Application/core/simulator.py
Moteur de simulation évolutif et de banc d'essai (Phase 10 & Transversal).
Mesure l'empreinte matérielle et alimente les abaques de performance sous contrainte Green-by-Design.
"""

import time
import psutil
import os
from pathlib import Path
from typing import Dict, Any
from rdflib import Graph, Literal, RDF, URIRef
from core.config import DKG_TBOX, DKG_DATA, DIR_SNAPSHOT_P6

class DKGSimulator:
    """
    Banc d'essai automatisé pour tester la montée en charge progressive 
    du stockage RDF/W3C et mesurer l'impact sur un poste local contraint (16 Go RAM).
    """
    def __init__(self, output_dir: Path = DIR_SNAPSHOT_P6):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.process = psutil.Process(os.getpid())

    def generate_synthetic_workload(self, scale_factor: int = 1000) -> Graph:
        """
        Génère un volume procédural de triplets RDF simulant des logs SOC ou des actifs.
        """
        g = Graph()
        g.bind("dkg", DKG_TBOX)
        g.bind("data", DKG_DATA)

        for i in range(scale_factor):
            asset_uri = URIRef(f"{DKG_DATA}SimulatedHost_{i}")
            g.add((asset_uri, RDF.type, DKG_TBOX.Host))
            g.add((asset_uri, DKG_TBOX.hasVulnerability, Literal(f"CVE-2026-{1000 + i}")))
            g.add((asset_uri, DKG_TBOX.hasRiskScore, Literal(float(i % 10) / 10.0)))

        return g

    def benchmark_execution(self, scale_factor: int = 1000) -> Dict[str, Any]:
        """
        Exécute le test de charge, mesure la RAM et le temps de traitement, 
        et produit les métriques pour les abaques.
        """
        print(f"\n[Simulator] Lancement du banc d'essai (Volume cible : {scale_factor} entités)...")
        
        # Mesure initiale RAM
        mem_before = self.process.memory_info().rss / (1024 * 1024)
        start_time = time.time()

        # 1. Génération de la charge
        g = self.generate_synthetic_workload(scale_factor)
        triple_count = len(g)

        # 2. Simulation de sérialisation / traitement local
        temp_path = self.output_dir / f"sim_workload_{scale_factor}.ttl"
        g.serialize(destination=str(temp_path), format="turtle")

        # 3. Mesure finale
        end_time = time.time()
        mem_after = self.process.memory_info().rss / (1024 * 1024)
        
        duration_ms = (end_time - start_time) * 1000
        mem_diff_mb = mem_after - mem_before

        metrics = {
            "scale_factor": scale_factor,
            "triple_count": triple_count,
            "execution_time_ms": round(duration_ms, 2),
            "memory_before_mb": round(mem_before, 2),
            "memory_after_mb": round(mem_after, 2),
            "memory_delta_mb": round(mem_diff_mb, 2),
            "status": "SUCCESS"
        }

        print(f"[Simulator] Terminé : {triple_count} triplets traités en {metrics['execution_time_ms']} ms (Delta RAM : {metrics['memory_delta_mb']} MB)")
        return metrics

if __name__ == "__main__":
    sim = DKGSimulator()
    # Test progressif pour alimenter les abaques
    for factor in [1000, 5000, 10000]:
        sim.benchmark_execution(factor)
