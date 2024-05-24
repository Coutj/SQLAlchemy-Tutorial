from sqlalchemy import (
    create_engine, text, MetaData, Table, Column, Integer, String, DateTime,ForeignKey,
    insert, select
)

from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional


"""
Base é uma classe base comumente utilizada na criação de mapeamentos objeto-relacionais. 
Ela atua como um contêiner para a definição de classes que representam tabelas do banco de dados. 
As classes de modelo são derivadas da Base, 
o que facilita a organização e a criação dos mapeamentos entre objetos Python e estruturas de dados do banco de dados.

"""

class Base(DeclarativeBase):
    data = mapped_column(DateTime) #Exemplo de parametro que pode ser herdado em outras classes