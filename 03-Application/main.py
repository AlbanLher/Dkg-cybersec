"""
03-Application/main.py
Point d'entrée principal de l'API FastAPI et distribution de l'IHM.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from core import config
from api.routes_phase8 import router as phase8_router

app = FastAPI(
    title="DKG-CyberSec API",
    description="Backend de démonstration SOC_1 & Green-by-Design (Phase 8)",
    version="1.0.0"
)

# Résolution et création automatique du dossier statique
STATIC_DIR = config.DIR_APP / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Déclaration des routes API
app.include_router(phase8_router)

# Service des ressources statiques (app.js, styles, etc.)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Route racine pour distribuer l'IHM
@app.get("/", response_class=FileResponse)
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return FileResponse(STATIC_DIR / "index.html", status_code=404)
    return FileResponse(index_file)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.API_GATEWAY_HOST,
        port=config.API_GATEWAY_PORT,
        reload=True
    )
