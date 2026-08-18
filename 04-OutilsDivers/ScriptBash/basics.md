podman exec neo4j ls -la /var/lib/neo4j/import/current

**Vérifiez les volumes montés**
podman inspect neo4j | grep -A 10 "Mounts"


**Testez l’accès aux fichiers**
podman exec neo4j cat /var/lib/neo4j/ontologies/ontologie.ttl | head -5