from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    senha = Column(String)

    # relação com tarefas
    tarefas = relationship("Tarefa", back_populates="usuario")


class Tarefa(Base):

    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String)
    concluida = Column(Boolean, default=False)

    # chave estrangeira (liga com Usuario)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # relação com usuario
    usuario = relationship("Usuario", back_populates="tarefas")