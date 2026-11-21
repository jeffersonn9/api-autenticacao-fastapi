from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Minha Primeira API Segura")

class Usuario(BaseModel):
    username: str
    senha: str
    email: str = ""

banco_usuarios = {}

@app.get("/")
def inicio():
    return {"mensagem": "Sistema de Seguranca v1.0 rodando!"}

@app.post("/cadastrar")
def cadastrar_usuario(user: Usuario):
    if user.username in banco_usuarios:
        raise HTTPException(status_code=400, detail="Usuario ja existe")
    
    banco_usuarios[user.username] = user.senha
    return {"status": "Usuario criado", "username": user.username, "email": user.email}

@app.post("/login")
def fazer_login(user: Usuario):
    if user.username not in banco_usuarios or banco_usuarios[user.username] != user.senha:
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")
    
    return {"mensagem": f"Bem-vindo, {user.username}! Acesso liberado."}
