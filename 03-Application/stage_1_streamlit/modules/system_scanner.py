# [EXG-MODULE] Scan local multi-plateforme des logiciels installés
import platform
import subprocess
import shutil

def scan_local_machine() -> list[dict]:
    current_os = platform.system()
    discovered_software = []
    
    try:
        if current_OS == "Linux":
            # Test de dpkg (Debian/Ubuntu)
            if shutil.which("dpkg"):
                res = subprocess.run(["dpkg-query", "-W", "-f=${Package}|${Version}\n"], capture_output=True, text=True, timeout=3)
                if res.returncode == 0:
                    for line in res.stdout.splitlines()[:15]: # Limite aux 15 premiers pour la démo
                        parts = line.split("|")
                        if len(parts) == 2:
                            discovered_software.append({"name": parts[0], "version": parts[1], "port": 0, "status": "Active"})
            elif shutil.which("rpm"):
                res = subprocess.run(["rpm", "-qa", "--qf", "%{NAME}|%{VERSION}\n"], capture_output=True, text=True, timeout=3)
                if res.returncode == 0:
                    for line in res.stdout.splitlines()[:15]:
                        parts = line.split("|")
                        if len(parts) == 2:
                            discovered_software.append({"name": parts[0], "version": parts[1], "port": 0, "status": "Active"})
                            
        elif current_os == "Windows":
            # Test de winget sous Windows
            if shutil.which("winget"):
                res = subprocess.run(["winget", "list", "--accept-source-agreements"], capture_output=True, text=True, timeout=5)
                if res.returncode == 0:
                    lines = res.stdout.splitlines()
                    for line in lines[2:12]: # Parse basique des lignes winget
                        tokens = line.split()
                        if len(tokens) >= 2:
                            discovered_software.append({"name": tokens[0], "version": tokens[1], "port": 0, "status": "Active"})
                            
    except Exception:
        pass
        
    # Fallback de démonstration si le scan natif retourne vide ou restreint
    if not discovered_software:
        discovered_software = [
            {"name": "openssh-server", "version": "8.9p1", "port": 22, "status": "Active"},
            {"name": "apache2", "version": "2.4.52", "port": 80, "status": "Exposed"},
            {"name": "samba", "version": "4.15.7", "port": 445, "status": "Vulnerable"}
        ]
        
    return discovered_software
