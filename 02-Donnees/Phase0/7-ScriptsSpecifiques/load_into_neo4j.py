#!/usr/bin/env python3
"""
Charge les données de l'inventaire et des CVE dans Neo4j.
Usage: python load_into_neo4j.py
"""
from neo4j import GraphDatabase
import json
import os

# Configuration Neo4j
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Acad26DKG!")

def load_inventory(driver, file_path="/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage/data/inventory.json"):
    with open(file_path, "r") as f:
        inventory = json.load(f)

    with driver.session() as session:
        # Supprimer les anciens nœuds (optionnel)
        session.run("MATCH (n:Device) DETACH DELETE n")
        session.run("MATCH (n:Software) DETACH DELETE n")

        for device in inventory["devices"]:
            # Créer le device
            session.run(
                "CREATE (d:Device {id: $id, type: $type, ip: $ip})",
                id=device["id"], type=device["type"], ip=device["ip"]
            )
            # Créer les logiciels et les lier
            for sw in device["software"]:
                session.run(
                    """
                    MERGE (s:Software {name: $name, version: $version})
                    MATCH (d:Device {id: $device_id})
                    CREATE (d)-[:HAS_SOFTWARE]->(s)
                    """,
                    name=sw["name"], version=sw["version"], device_id=device["id"]
                )

def load_cves(driver, file_path="cve_data.ttl"):
    # Parsez le fichier TTL (simplifié)
    # Ici, on suppose que vous avez déjà converti le TTL en JSON
    with open("cve_data.json", "r") as f:  # À générer depuis cve_data.ttl
        cves = json.load(f)

    with driver.session() as session:
        session.run("MATCH (n:Vulnerability) DETACH DELETE n")
        for cve in cves:
            session.run(
                """
                CREATE (v:Vulnerability {id: $id, name: $name, cvssScore: $cvss, description: $desc})
                """,
                id=cve["id"], name=cve["name"], cvss=cve["cvssScore"], desc=cve["description"]
            )

if __name__ == "__main__":
    driver = GraphDatabase.driver(URI, auth=AUTH)
    load_inventory(driver, "/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage/data/inventory.json")
    load_cves(driver, "cve_data.ttl")
    driver.close()
    print("Données chargées dans Neo4j !")
