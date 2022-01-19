from sqlalchemy import create_engine, text, Table, Column, String, MetaData, inspect, insert
from sqlalchemy_utils import database_exists, create_database
from dotenv import dotenv_values

config = dotenv_values(".env")

def init_db():
    engine = create_engine('postgresql://postgres:'+config['ZOE_POSTGRES_PASSWORD']+'@localhost:5432/dev_tip_bot_db')

    if not database_exists(engine.url):
        create_database(engine.url)

    meta = MetaData()

    secrets = Table(
                'Secrets', meta, 
                Column('user_id', String, primary_key = True), 
                Column('private_key', String), 
              )

    if not inspect(engine).has_table("Secrets"):
        meta.create_all(engine)
    return engine

def add_user_db(discord_id, private_key, db):
    with db.connect() as connection:
        #https://code-maven.com/slides/python/sqlalchemy-engine-insert
        connection.execute(
            text("INSERT INTO Secrets (user_id, private_key) VALUES (:user_id, :private_key)"),
            [{"user_id": str(discord_id), "private_key": str(private_key)}]
        )
def get_user_db(discord_id, db):
    with db.connect() as connection:
        results = connection.execute(
                    text("SELECT * FROM Secrets where user_id = :user_id" ),
                    [{"user_id": str(discord_id)}]
                  )

    return results.all()

def delete_user_db(discord_id, db):
    with db.connect() as connection:
        connection.execute(
            text("DELETE FROM Secrets where user_id = :user_id" ),
            [{"user_id": str(discord_id)}]
        )

db = init_db()
# add_user_db(423205229723516948, config['0x61178E17Fac681a16eF47ed4B3527B95357b7D09'], db) already added
userInfo = get_user_db(423205229723516948, db)
print(userInfo)