# Author: Clinton Daniel, University of South Florida
# Date: 4/4/2023
# Description: This is a Flask App that uses SQLite3 to
# execute (C)reate, (R)ead, (U)pdate, (D)elete operations

from flask import Flask
from flask import render_template
from flask import request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

# Route to form used to add a new student to the database
@app.route("/enternew")
def enternew():
    return render_template("cliente.html")

# Route to add a new record (INSERT) student data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            nmCria = request.form['nmCri']
            dtNasc = request.form['dtNasc']
            nmCli = request.form['nmCli']
            addr = request.form['add']
            venda = request.form['venda']                     
            cores = request.form['cores']
            data = request.form['data'] 
            inicio= request.form['party-date-inicio']
            termino= request.form['party-date-termino']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO clientes (nameCriança, dataNasc, nameCliente, addr, venda, cores, data, inicio, termino) VALUES (?,?,?,?,?,?,?,?,?)",(nmCria, dtNasc, nmCli, addr, venda, cores, data, inicio, termino))

                con.commit()
                msg = "Inserido com Sucesso"
        except:
            con.rollback()
            msg = "Erro ao inserir"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

#função para calcular o tempo gasto nas confecções
def get_clientes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT rowid,nameCriança, dataNasc, nameCliente, addr, venda, cores, data, inicio, termino FROM clientes")
    registros=cursor.fetchall()
    dados = []
    for row in registros:
        rowid, nameCriança, dataNasc,nameCliente,addr,venda,cores,data,inicio,termino = row
        try:
            entrada = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
            saida = datetime.strptime(termino, "%Y-%m-%d %H:%M:%S")
            duracao = saida - entrada
            dias=duracao.days
            horas=duracao.seconds//3600
            minutos=(duracao.seconds % 3600) // 60
            
        except Exception:
            duracao = "Formato incorreto"

        try:
            dados.append({
                'rowid': rowid,
                'nameCriança': nameCriança,
                'dataNasc': dataNasc,
                'nameCliente': nameCliente,
                'addr': addr,
                'venda': venda,
                'cores': cores,
                'data': data,
                'inicio': inicio,
                'termino': termino,
                'duracao': "foi'{dias}' dias,{horas} horas e {minutos} minutos"
            })
        except Exception:
            duracao = "erro na conversao"

    conn.close()
    return dados

@app.route('/list')
def list():
    clientes = get_clientes()
    return render_template('list.html', clientes=clientes)

# Route to SELECT all data from the database and display in a table      
# @app.route('/list')
# def list():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the clientes table.
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row

#     cur = con.cursor()
#     cur.execute("SELECT rowid, * FROM clientes")

#     rows = cur.fetchall()
#     con.close()
#     # Send the results of the SELECT to the list.html page
#    # eventos = get_eventos()
#     return render_template("list.html",rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM clientes WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            nmCria = request.form['nmCri']
            dtNasc = request.form['dtNasc']
            nmCli = request.form['nmCli']
            addr = request.form['add']
            venda = request.form['venda']                     
            cores = request.form['cores']
            data = request.form['data']
            inicio= request.form['party-date-inicio']
            termino= request.form['party-date-termino'] 

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE clientes SET nameCriança='"+nmCria+"', dataNasc='"+dtNasc+"', nameCliente='"+nmCli+"', addr='"+addr+"', venda='"+venda+"', cores='"+cores+"', data='"+data+"', inicio='"+inicio+"', termino='"+termino+"'  WHERE rowid="+rowid)

                con.commit()
                msg = "Alterado com sucesso"
        except:
            con.rollback()
            msg = "Erro ao editar: UPDATE clientes SET nameCriança="+nmCria+", nameCliente="+nmCli+", addr="+addr+", venda="+venda+", data="+data+", dataNasc="+data+", cores="+cores+", data="+data+", inicio="+inicio+", termino="+termino+"  WHERE rowid="+rowid

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM clientes WHERE rowid="+rowid)

                    con.commit()
                    msg = "Excluido com sucesso"
        except:
            con.rollback()
            msg = "Erro ao excluir"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)