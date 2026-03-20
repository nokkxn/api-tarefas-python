from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha, hash):
    return pwd_context.verify(senha, hash)

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = 30


def criar_token(dados: dict):

    dados_copia = dados.copy()

    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRACAO_MINUTOS)

    dados_copia.update({"exp": expiracao})

    token = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

    return token