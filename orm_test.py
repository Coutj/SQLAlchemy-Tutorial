from orm_base import *
from mapped_classes import User, Address
from datetime import datetime

def exec_statement(engine, stmt):
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()


def using_tables(engine):

    # MetaData - serve como um contêiner para todas as informações relacionadas ao esquema de um banco de dados no SQLAlchemy
    # permitindo que você defina, reflita e manipule a estrutura do banco de dados de forma pythonica
    
    metadata_obj = MetaData()

    # Criando Tabelas

    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )


    # Inserindo Usuarios
    insert_stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
    print(insert_stmt)

    select_stmt = select(user_table).where(user_table.c.name == "spongebob")
    print(select_stmt)

    # Criando objetos definidos em metadata no banco
    metadata_obj.create_all(engine)

    with engine.connect() as conn:

        result = conn.execute(insert_stmt)
        print(result)

        print('\n\nSELECT RESULT:')
        for row in conn.execute(select_stmt):
            print(row)


#Utilizando Mapped classes para realizar as operações 
def using_mapped_classes(engine):
    
    Base.metadata.create_all(engine)

    session = Session(engine)
    
    squidward = User(name="squidward", fullname="Squidward Tentacles")
    krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

    session.add(squidward)
    session.add(krabs)

    session.flush()
    session.commit()

    # select_stmt = select(User).where(User.name == "squidward")
    select_stmt = select(User)
    
    select_result = session.scalars(select(User)) #Utilize scalars para retornar os objetos
    print('\n\nTESTE SELECT FORMATO ORM:')
    print(select_result.all(), '\n\n')


    # Usando Reflection - Obtendo objeto através de schema/dados gravados no bd
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    users_table_from_db = metadata_obj.tables["user_account"]

    print([col.name for col in users_table_from_db.columns])

    add_user = users_table_from_db.insert().values(name='sandy', fullname='Sandy Cheeks', data=datetime.now())
    session.execute(add_user)

    session.flush() 

    select_stmt = (select(User)
                   .where(User.name.like('s%'))
                   .order_by(User.id))

    select_result = session.scalars(select_stmt)

    print([row for row in select_result.all()])

    #Alterando nome sandy para upper case - Operacao Update

    sandy = session.execute(
        select(User)
        .where(User.name == 'sandy' )
    ).scalar_one()

    sandy.name = sandy.name.upper()
    
    session.flush()

    select_result = session.execute(select(users_table_from_db))
    print([row.name for row in select_result])

    session.close()


if __name__ == '__main__':

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    
    """
        Execute os métodos abaixo individualmente
        para entender a utilizacao do ORM no SQLAlchemy
    """
    
    # using_tables(engine)
    using_mapped_classes(engine)