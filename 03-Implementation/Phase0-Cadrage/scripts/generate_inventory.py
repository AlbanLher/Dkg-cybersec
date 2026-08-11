#!/usr/bin/env python3
"""
Génère un inventaire fictif de devices/logiciels pour le DKG.
Usage: python generate_inventory.py > inventory.json
"""
import json
from faker import Faker
import random

fake = Faker()

DEVICES = ["PC", "Laptop", "Router", "Server"]
SOFTWARES = {
    "OpenSSL": ["1.0.2", "1.1.1", "3.0.8"],
    "Apache": ["2.4.54", "2.4.57"],
    "Python": ["3.8.10", "3.9.16"]
}

def generate_inventory(num_devices=3):
    inventory = {
        "devices": [],
        "timestamp": fake.iso8601()
    }
    for _ in range(num_devices):
        device_type = random.choice(DEVICES)
        device_id = f"{device_type}-{fake.uuid4()[:8]}"
        software_list = [
            {"name": sw, "version": random.choice(versions)}
            for sw, versions in random.sample(list(SOFTWARES.items()), 2)
        ]
        inventory["devices"].append({
            "id": device_id,
            "type": device_type,
            "software": software_list,
            "ip": fake.ipv4_private()
        })
    return inventory

if __name__ == "__main__":
    print(json.dumps(generate_inventory(), indent=2))
