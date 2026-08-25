import re
from rdflib import Graph, Literal, Namespace, RDF, RDFS

EX = Namespace("http://example.org/dkg/ontology#")
INST = Namespace("http://example.org/dkg/instance#")

class RegexEntityExtractor:
    """Extractions déterministes basées sur des expressions régulières strictes."""
    
    PATTERNS = {
        "CVE": r'CVE-\d{4}-\d{4,7}',
        "IP_Address": r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
        "MAC_Address": r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b',
        "Port": r'\bport\s+(\d{1,5})\b'
    }

    def extract_from_text(self, text: str, source_id: str, graph: Graph) -> Graph:
        doc_uri = INST[f"Doc_{source_id}"]
        graph.add((doc_uri, RDF.type, EX.Document))
        
        # 1. Extraction CVEs
        cves = set(re.findall(self.PATTERNS["CVE"], text, re.IGNORECASE))
        for cve in cves:
            cve_upper = cve.upper()
            cve_uri = INST[f"CVE_{cve_upper.replace('-', '_')}"]
            graph.add((cve_uri, RDF.type, EX.Vulnerability))
            graph.add((cve_uri, RDFS.label, Literal(cve_upper)))
            graph.add((doc_uri, EX.mentionsVulnerability, cve_uri))

        # 2. Extraction IPs
        ips = set(re.findall(self.PATTERNS["IP_Address"], text))
        for ip in ips:
            ip_clean = ip.replace('.', '_')
            ip_uri = INST[f"IP_{ip_clean}"]
            graph.add((ip_uri, RDF.type, EX.IPAddress))
            graph.add((ip_uri, RDFS.label, Literal(ip)))
            graph.add((doc_uri, EX.mentionsIP, ip_uri))

        # 3. Extraction MAC
        macs = set(re.findall(self.PATTERNS["MAC_Address"], text))
        for mac in macs:
            mac_clean = re.sub(r'[:-]', '_', mac)
            mac_uri = INST[f"MAC_{mac_clean}"]
            graph.add((mac_uri, RDF.type, EX.MACAddress))
            graph.add((mac_uri, RDFS.label, Literal(mac)))

        return graph
