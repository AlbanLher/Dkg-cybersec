
## Nœuds

| Label           | Description               | Propriétés                       | Exemple                 |
| --------------- | ------------------------- | -------------------------------- | ----------------------- |
| `Device`        | Appareil physique/virtuel | `id`, `type`, `ip`               | `PC-Alban`              |
| `Software`      | Logiciel installé         | `name`, `version`                | `OpenSSL 1.0.2`         |
| `Vulnerability` | Vulnérabilité (CVE)       | `id`, `cvssScore`, `description` | `CVE-2023-1234`         |
| `Rule`          | Règle de sécurité         | `id`, `description`              | `Mettre à jour OpenSSL` |
| `User`          | Utilisateur               | `name`, `role`                   | `Alban`                 |
| `Action`        | Action corrective         | `id`, `description`              | `Redémarrer le serveur` |

## Relations

| Type                | Description              | Exemple                           |
| ------------------- | ------------------------ | --------------------------------- |
| `HAS_SOFTWARE`      | Device → Software        | `PC-Alban` → `OpenSSL 1.0.2`      |
| `HAS_VULNERABILITY` | Device → Vulnerability   | `PC-Alban` → `CVE-2023-1234`      |
| `AFFECTED_BY`       | Software → Vulnerability | `OpenSSL 1.0.2` → `CVE-2023-1234` |
| `REQUIRES_ACTION`   | Vulnerability → Action   | `CVE-2023-1234` → `Mettre à jour` |
| `APPLIES_TO`        | Rule → Device            | `RULE-001` → `PC-Alban`           |
