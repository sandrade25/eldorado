import typer
from app.database import DatabaseUtils

def main(db_code:str, message:str):
    DatabaseUtils.create_revision(db_code=db_code, message=message)



if __name__ == "__main__": 
    typer.run(main)