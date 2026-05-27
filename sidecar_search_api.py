#!/usr/bin/env python3
"""
Microserviço sidecar para o EduTrack AI.
Expõe a lógica de scripts/subject_search.py via HTTP (FastAPI + uvicorn)
para que o Xano possa chamar como external.request.

Executar:
    .venv\\Scripts\\python sidecar_search_api.py
    (roda em http://localhost:8787)
"""

import sys
import os

# Garante que scripts/ está no path de importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from subject_search import search_subjects, load_json_data  # noqa: E402

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print(
        "Dependências ausentes. Execute:\n"
        "  .venv\\Scripts\\pip install fastapi uvicorn\n",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Schema de entrada
# ---------------------------------------------------------------------------

class SearchRequest(BaseModel):
    subjects: list = Field(..., description="Lista de disciplinas (JSON)")
    tasks: list = Field(..., description="Lista de tarefas acadêmicas (JSON)")
    query: str = Field(default="", description="Termo de busca parcial")
    include_overdue: bool = Field(default=False, description="Incluir disciplinas com tarefas atrasadas")
    current_date: str = Field(default="", description="Data de referência (ISO 8601); usa 'agora' se vazio")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="EduTrack Subject Search Sidecar",
    description="Microserviço interno que filtra disciplinas por nome ou tarefas atrasadas.",
    version="1.0.0",
)


@app.post("/search")
async def search(req: SearchRequest):
    try:
        result = search_subjects(
            subjects=req.subjects,
            tasks=req.tasks,
            query=req.query,
            include_overdue=req.include_overdue,
            current_date_str=req.current_date,
        )
        return JSONResponse(content=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "subject-search-sidecar"}


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8787, reload=False)
