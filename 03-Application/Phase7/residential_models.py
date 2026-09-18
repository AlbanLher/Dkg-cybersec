# [EXG-TE-01] Immutabilité Payloads via Pydantic V2 (frozen=True) avec adaptateur JSON
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator

class LocalService(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    name: str = Field(..., description="Nom du service ou protocole")
    version: str = Field(default="1.0.0", description="Version exacte du logiciel")
    port: int = Field(default=0, description="Port réseau associé")
    status: str = Field(default="active", description="Statut opérationnel ou exposition")
    associated_cve: Optional[str] = Field(None, description="CVE associée si connue")

class AssetModel(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    host_id: str = Field(..., description="Identifiant unique de l'actif")
    os: str = Field(..., description="Système d'exploitation ou firmware")
    ip_address: str = Field(..., description="Adresse IP locale sur le LAN")
    local_services: List[LocalService] = Field(default_factory=list, description="Services actifs sur l'hôte")
    name: Optional[str] = Field(None, description="Nom lisible de l'actif")
    zone: Optional[str] = Field("LAN", description="Zone réseau")

    @model_validator(mode="before")
    @classmethod
    def transform_exposed_services(cls, data: Any) -> Any:
        """Adapte dynamiquement le format JSON brut (asset_id -> host_id, exposed_services -> local_services)."""
        if isinstance(data, dict):
            if "asset_id" in data and "host_id" not in data:
                data["host_id"] = data["asset_id"]
            
            if "exposed_services" in data and "local_services" not in data:
                services = []
                for srv_name in data["exposed_services"]:
                    port_map = {"SMB": 445, "Plex Media Server": 32400, "Telnet": 23, "HTTP API Unauthenticated": 80}
                    services.append({
                        "name": srv_name,
                        "version": "unknown",
                        "port": port_map.get(srv_name, 8080),
                        "status": "Exposed" if srv_name in ["Telnet", "HTTP API Unauthenticated"] else "Active",
                        "associated_cve": None
                    })
                data["local_services"] = services
        return data

class NetworkEnvironmentModel(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    gateway_name: str = Field(default="Box_FAI_Default", description="Nom de la Box FAI")
    wan_exposure_risk: bool = Field(default=True, description="Présence d'une exposition WAN")
    exposed_service: Optional[str] = Field(default="Plex Media Server", description="Service exposé vers l'extérieur")
    wifi_shared_access: bool = Field(default=False, description="Présence d'un accès Wi-Fi invité ou partagé")

class ResidentialFamilyEnvironment(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    network_environment: NetworkEnvironmentModel
    assets: List[AssetModel]

    @model_validator(mode="before")
    @classmethod
    def transform_household_assets(cls, data: Any) -> Any:
        """Assure la correspondance entre household_assets et network_environment."""
        if isinstance(data, dict):
            if "household_assets" in data and "assets" not in data:
                data["assets"] = data["household_assets"]
            if "network_environment" not in data:
                data["network_environment"] = {
                    "gateway_name": "Box_FAI_Livebox",
                    "wan_exposure_risk": True,
                    "exposed_service": "Plex Media Server",
                    "wifi_shared_access": False
                }
        return data
