from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, SessionLocal

# JWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM

# criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🔹 conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 segurança JWT
security = HTTPBearer()


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# 🔹 rota inicial
@app.get("/")
def home():
    return {"msg": "API funcionando"}


# 🔹 criar usuário
@app.post("/usuarios")
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.criar_usuario(db, usuario)


# 🔹 login (gera token)
@app.post("/login")
def login(dados: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    return crud.login_usuario(db, dados)


# 🔹 criar tarefa (protegida)
@app.post("/tarefas")
def criar_tarefa(
    tarefa: schemas.TarefaCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):
    return crud.criar_tarefa(db, tarefa, usuario_id)


# 🔹 listar tarefas (protegida)
@app.get("/tarefas")
def listar_tarefas(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):
    return crud.listar_tarefas(db, usuario_id)


# 🔹 deletar tarefa (protegida)
@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):
    return crud.deletar_tarefa(db, tarefa_id, usuario_id)


# 🔹 atualizar tarefa (protegida)
@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(
    tarefa_id: int,
    dados: schemas.TarefaUpdate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):
    return crud.atualizar_tarefa(db, tarefa_id, dados, usuario_id)