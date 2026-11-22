import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Minha Primeira API Segura")

class Usuario(BaseModel):
    username: str
    senha: str
    email: str = ""

banco_usuarios = {}

# Função nova de segurança: transforma a senha em um hash SHA-256
def criptografar_senha(senha: str):
    return hashlib.sha256(senha.encode()).hexdigest()

@app.get("/")
def inicio():
    return {"mensagem": "Sistema de Seguranca v2.0 (Com Criptografia)!"}

@app.post("/cadastrar")
def cadastrar_usuario(user: Usuario):
    if user.username in banco_usuarios:
        raise HTTPException(status_code=400, detail="Usuario ja existe")
    
    # Agora salvamos a senha embaralhada (hash), nunca em texto puro!
    senha_segura = criptografar_senha(user.senha)
    banco_usuarios[user.username] = senha_segura
    
    return {
        "status": "Usuario criado com seguranca",
        "username": user.username,
        "hash_gerado": senha_segura  # Mostrando aqui apenas para você ver a criptografia funcionando!
    }

@app.post("/login")
def fazer_login(user: Usuario):
    senha_digitada_hash = criptografar_senha(user.senha)
    
    if user.username not in banco_usuarios or banco_usuarios[user.username] != senha_digitada_hash:
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")
    
    return {"mensagem": f"Bem-vindo, {user.username}! Acesso liberado."}
