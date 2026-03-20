from sqlalchemy.orm import Session
import models
import schemas


# 🔹 CRIAR USUÁRIO
from security import gerar_hash_senha

def criar_usuario(db: Session, usuario):

    senha_hash = gerar_hash_senha(usuario.senha)

    novo = models.Usuario(
        username=usuario.username,
        senha=senha_hash
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# 🔹 LOGIN (já com token)
from security import verificar_senha, criar_token

def login_usuario(db: Session, dados):

    usuario = db.query(models.Usuario).filter(
        models.Usuario.username == dados.username
    ).first()

    if not usuario:
        return {"erro": "Usuário não existe"}

    if not verificar_senha(dados.senha, usuario.senha):
        return {"erro": "Senha incorreta"}

    token = criar_token({"sub": usuario.id})  # 🔥 agora usamos ID

    return {"access_token": token, "token_type": "bearer"}


# 🔹 CRIAR TAREFA (agora vinculada ao usuário)
def criar_tarefa(db: Session, tarefa, usuario_id):

    nova = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        usuario_id=usuario_id
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


# 🔹 LISTAR TAREFAS (SÓ DO USUÁRIO)
def listar_tarefas(db: Session, usuario_id):

    return db.query(models.Tarefa).filter(
        models.Tarefa.usuario_id == usuario_id
    ).all()


# 🔹 DELETAR TAREFA (SÓ SE FOR DO USUÁRIO)
def deletar_tarefa(db: Session, tarefa_id, usuario_id):

    tarefa = db.query(models.Tarefa).filter(
        models.Tarefa.id == tarefa_id,
        models.Tarefa.usuario_id == usuario_id
    ).first()

    if tarefa:
        db.delete(tarefa)
        db.commit()
        return {"msg": "Tarefa deletada"}

    return {"erro": "Tarefa não encontrada ou não pertence ao usuário"}


# 🔹 ATUALIZAR TAREFA (SÓ SE FOR DO USUÁRIO)
def atualizar_tarefa(db: Session, tarefa_id, dados, usuario_id):

    tarefa = db.query(models.Tarefa).filter(
        models.Tarefa.id == tarefa_id,
        models.Tarefa.usuario_id == usuario_id
    ).first()

    if tarefa:

        tarefa.titulo = dados.titulo
        tarefa.descricao = dados.descricao
        tarefa.concluida = dados.concluida

        db.commit()
        db.refresh(tarefa)

        return tarefa

    return {"erro": "Tarefa não encontrada ou não pertence ao usuário"}