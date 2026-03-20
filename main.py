from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.post("/tarefas")
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db)):

    return crud.criar_tarefa(db, tarefa)


@app.get("/tarefas")
def listar_tarefas(
    db: Session = Depends(get_db),
    usuario: str = Depends(verificar_token)
):
    return crud.listar_tarefas(db)

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):

    return crud.deletar_tarefa(db, tarefa_id)


@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, dados: schemas.TarefaUpdate, db: Session = Depends(get_db)):

    return crud.atualizar_tarefa(db, tarefa_id, dados)

@app.get("/")
def home():
    return {"msg": "API funcionando"}

@app.post("/usuarios")
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):

    return crud.criar_usuario(db, usuario)


@app.post("/login")
def login(dados: schemas.UsuarioLogin, db: Session = Depends(get_db)):

    return crud.login_usuario(db, dados)
