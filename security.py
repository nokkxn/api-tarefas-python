from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# 🔐 configuração do hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 segredo do token
SECRET_KEY = "segredo_super_secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# 🔹 gerar hash da senha
def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)


# 🔹 verificar senha
def verificar_senha(senha: str, hash: str):
    return pwd_context.verify(senha, hash)


# 🔹 criar token JWT
def criar_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token