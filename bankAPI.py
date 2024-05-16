from sqlalchemy.orm import Session, declarative_base, relationship
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    ForeignKey,
    create_engine,
    inspect,
)

Base = declarative_base()


class Client(Base):
    __tablename__ = "bank_client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    cpf = Column(String(10))
    address = Column(String(60))

    account = relationship("Account", back_populates="client")

    def __repr__(self):
        return f"User --> user_id={self.id} | name={self.name} | fullname={self.cpf} | address={self.address}"


class Account(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_account = Column(String(50), nullable=False)
    agency = Column(String(12), nullable=False)
    num = Column(Integer)
    id_client = Column(Integer, ForeignKey("bank_client.id"), nullable=True)
    bank_balance = Column(Float, nullable=False)

    client = relationship("Client", back_populates="account")

    def __repr__(self):
        return f"Account --> id={self.id} | type_account={self.type_account} | agency={self.agency} | Number_Account={self.num} | bank balance={self.bank_balance}"


# Criando uma engine para se conectar ao banco de dados em um arquivo sqlite3 (.db)
engine = create_engine("sqlite:///bank_API.db")

Base.metadata.create_all(engine)

inspect_sql = inspect(engine)

# Imprimindo o nome das tabelas do banco de dados
print(inspect_sql.get_table_names())
# Verificando se a tabela "user_account" existe
print(inspect_sql.has_table("user_account"))
# Imprimindo o nome do esquema padrão
print(inspect_sql.default_schema_name)

# Obtendo informações sobre as colunas da tabela "user_account"
columns = inspect_sql.get_columns("user_account")
print("\ntable -> bank_client:")
for column in columns:
    print(column)

# Obtendo informações sobre as colunas da tabela "address"
columns = inspect_sql.get_columns("bank_client")
print("\ntable -> user_account:")
for column in columns:
    print(column)

with Session(engine) as session:
    Pablo = Client(
        name="Pablo Troli Nascimento",
        cpf="2349808769",
        address="Rua sei oque lá - nº134",
        account=[Account(type_account="PJ", agency="0001", num=111, bank_balance=300)],
    )
    Gabriela = Client(
        name="Gabriela Silva",
        cpf="978465201",
        address="Rua onde Liberdade Cantou - nº290",
        account=[
            Account(type_account="Poupança", agency="0002", num=222, bank_balance=2450)
        ],
    )
    Jean = Client(
        name="Jean Lucca",
        cpf="23456780912",
        address="Rua naosei onde - nº600",
        account=[
            Account(type_account="Corrente", agency="0003", num=333, bank_balance=10000)
        ],
    )

    session.add_all([Pablo, Gabriela, Jean])
    session.commit()
