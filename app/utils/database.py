
# Functions related to DB control. As we build, this may become a service class.

def db_url(user: str, password:str, host:str, port:str):

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}"