from pydantic import BaseModel

class TarefaCreate(BaseModel):

    titulo: str
    descricao: str


class Tarefa(BaseModel):

    id: int
    titulo: str
    descricao: str
    concluida: bool

    class Config:
        orm_mode = True

class TarefaUpdate(BaseModel):

    titulo: str
    descricao: str
    concluida: bool

class UsuarioCreate(BaseModel):
    username: str
    senha: str


class UsuarioLogin(BaseModel):
    username: str
    senha: str


