import sqlite3

conn = sqlite3.connect('database.db')
print("Conexão com o Banco feito com sucesso")

conn.execute('CREATE TABLE clientes (nameCriança TEXT, dataNasc TEXT, nameCliente TEXT, addr TEXT, venda TEXT, cores TEXT, data TEXT, inicio TEXT, termino TEXT)')
print("Criação tabela com sucesso!")

conn.close()

