from sqlalchemy import create_engine, text, Table, Column, String, MetaData, inspect, insert
from sqlalchemy_utils import database_exists, create_database
from dotenv import dotenv_values

config = dotenv_values("../.env")

def init_db():
    engine = create_engine('postgresql://postgres:postgres@postgres:5432/dev_tip_bot_db')

    if not database_exists(engine.url):
        create_database(engine.url)

    meta = MetaData()

    secrets = Table(
                'secrets', meta, 
                Column('user_id', String, primary_key = True), 
                Column('private_key', String), 
              )
    
    secrets.create(engine, checkfirst=True)

    # print(engine.table_names())

    # if not inspect(engine).has_table("Secrets"):
    #     print("in if \n\n\n\n\n")
    #     meta.create_all(engine)
    return engine

def add_user_db(discord_id, private_key, db):
    with db.connect() as connection:
        #https://code-maven.com/slides/python/sqlalchemy-engine-insert
        connection.execute(
            text("INSERT INTO secrets (user_id, private_key) VALUES (:user_id, :private_key)"),
            [{"user_id": str(discord_id), "private_key": str(private_key)}]
        )
def get_user_db(discord_id, db):
    with db.connect() as connection:
        results = connection.execute(
                    text("SELECT * FROM secrets where user_id = :user_id" ),
                    [{"user_id": str(discord_id)}]
                  )

    return results.all()[0] #should only return one tuple in a list

def delete_user_db(discord_id, db):
    with db.connect() as connection:
        connection.execute(
            text("DELETE FROM secrets where user_id = :user_id" ),
            [{"user_id": str(discord_id)}]
        )

def get_all_user(db):
    with db.connect() as connection:
        results = connection.execute(
            text("SELECT * FROM secrets")
        )
    return results.all()

db = init_db()
#add_user_db(423205229723516948, config['0x61178E17Fac681a16eF47ed4B3527B95357b7D09'], db) already added
# add_user_db(423205229723516948, config['0x61178E17Fac681a16eF47ed4B3527B95357b7D09'], db)
# userInfo = get_user_db(423205229723516948, db)
# print(userInfo)
allUserInfo = get_all_user(db)
# print(allUserInfo)

for entry in allUserInfo:
    print(entry)