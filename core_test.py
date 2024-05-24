# from orm_base import *
from sqlalchemy import create_engine, text


"""
A biblioteca Core no SQLAlchemy fornece uma camada de abstração de nível mais baixo para interagir diretamente com o banco de dados,
permitindo criar consultas SQL de forma mais granular e controlada, sem a necessidade de um mapeamento objeto-relacional completo. 
Em resumo, ela oferece ferramentas para construir e executar consultas SQL de maneira mais direta e eficiente.

"""

def main():

    # interface que fornece conectividade com um banco de dados
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    with engine.connect() as conn:
           
        #Criando tabela
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        
        # A clausula insert foi executada 2x. Uma para cada dicionário passado como argumento
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )

        # Realizando update
        conn.execute(
            text("UPDATE some_table SET x = :x WHERE y = :y"),
            {'x': 5, 'y': 4}
        )

        result = conn.execute(text("SELECT * FROM some_table"))
        
        # print(result.all())
        for row in result:
            print(f"{row.x} - {row.y}")
        
        # conn.commit() As operações nao são commitadas automaticamente no fechamento do with

if __name__ == '__main__':
    main()