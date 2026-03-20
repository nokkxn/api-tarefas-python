from sqlalchemy.orm import Session
import models
import schemas


def criar_tarefa(db: Session, tarefa: schemas.TarefaCreate):

    nova_tarefa = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao
    )

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return nova_tarefa


def listar_tarefas(db: Session):

    return db.query(models.Tarefa).all()


def deletar_tarefa(db, tarefa_id):

    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()

    if tarefa:
        db.delete(tarefa)
        db.commit()
        return {"msg": "Tarefa deletada"}

    return {"erro": "Tarefa não encontrada"}

def atualizar_tarefa(db, tarefa_id, dados):

    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()

    if tarefa:

        tarefa.titulo = dados.titulo
        tarefa.descricao = dados.descricao
        tarefa.concluida = dados.concluida

        db.commit()
        db.refresh(tarefa)

        return tarefa

    return {"erro": "Tarefa não encontrada"}

from security import hash_senha

def criar_usuario(db, usuario):

    nova_senha = hash_senha(usuario.senha)

    novo = models.Usuario(
        username=usuario.username,
        senha=nova_senha
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


from security import verificar_senha, criar_token

def login_usuario(db, dados):

    usuario = db.query(models.Usuario).filter(
        models.Usuario.username == dados.username
    ).first()

    if not usuario:
        return {"erro": "Usuário não existe"}

    if not verificar_senha(dados.senha, usuario.senha):
        return {"erro": "Senha incorreta"}

    token = criar_token({"sub": usuario.username})

    return {"access_token": token, "token_type": "bearer"}
