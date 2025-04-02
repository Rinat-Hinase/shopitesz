from fastapi import APIRouter

router = APIRouter(prefix="/usuarios",tags=["Usuarios"])

@router.get("/login")
async def login():
    return {"mensaje":"validando credenciales del usuario"}

