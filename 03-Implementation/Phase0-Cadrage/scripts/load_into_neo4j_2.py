import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Acad26DKG!")

def load_inventory(driver, file_path="/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage/data/inventory.json"):
    with open(file_path, "r") as f:
        inventory = json.load(f)

    # Si le fichier contient directement une clé "devices"
    devices_data = inventory.get("devices", inventory)

    with driver.session() as session:
        # 1. Nettoyage (Optionnel)
        session.run("MATCH (n:Device) DETACH DELETE n")
        session.run("MATCH (s:Software) DETACH DELETE s")

        # 2. Ingestion optimisée en 1 seule requête Cypher
        query = """
        UNWIND $devices AS device
        MERGE (d:Device {id: device.id})
        SET d.type = device.type,
            d.ip = device.ip

        WITH d, device.software AS softwares
        UNWIND softwares AS sw
        MERGE (s:Software {name: sw.name, version: sw.version})
        MERGE (d)-[:HAS_SOFTWARE]->(s)
        """
        
        session.run(query, devices=devices_data)
        print("Importation réussie !")

# Utilisation
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    load_inventory(driver)
