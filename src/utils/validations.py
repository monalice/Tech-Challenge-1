from fastapi import HTTPException

def validate_sql_injection(value: str, field_name: str = "campo"):
  sql_keywords = ["select", "insert", "update", "delete", "drop", "--", ";", " or ", " and "]
  lowered = value.lower()
  if any(keyword in lowered for keyword in sql_keywords):
    raise HTTPException(status_code=400, detail=f"{field_name} contém conteúdo potencialmente malicioso")

def validate_username(username: str):
  if not username.isalnum():
    raise HTTPException(status_code=400, detail="O nome de usuário deve conter apenas caracteres alfanuméricos")
  validate_sql_injection(username, "nome de usuário")

def validate_password(password: str, confirm_password: str):
  validate_sql_injection(password, "password")
  if password != confirm_password:
    raise HTTPException(status_code=400, detail="Senhas não coincidem")
  if len(password) < 8:
    raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres")

def validate_fullname(fullname: str):
  validate_sql_injection(fullname, "nome completo")
  if not fullname.replace(" ", "").isalpha():
      raise HTTPException(status_code=400, detail="O nome completo deve conter apenas letras")

def validate_cellphone(cellphone: str):
  validate_sql_injection(cellphone, "celular")
  if not cellphone.isdigit() or len(cellphone) != 11:
      raise HTTPException(status_code=400, detail="O celular deve conter apenas números e ter 11 dígitos")

def validate_login_input(username: str, password: str):
  validate_username(username)
  validate_sql_injection(password, "password")
  if not password or len(password) < 8:
      raise HTTPException(status_code=400, detail="Senha inválida")