from PyQt5 import uic,QtWidgets
import mysql.connector

num_id = 0

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "cadastro_produtos"
)
def editar_dados():
    global num_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    num_id = valor_id
    
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))

def salvar_dados_editados():
    #pega o numero do ID
    global num_id
    #Valor digitado no lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    #Atualiza os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format(codigo, descricao, preco, categoria, num_id))
    #Atualiza as janelas
    tela_editar.close()
    segunda_tela.close()    
    chama_segunda_tela()   
    banco.commit() 

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
    banco.commit()

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = "" 

    if formulario.radioButton.isChecked():
        print("Categoria Informatica foi selecionado")
        categoria = "Informatica"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Alimentos foi selecionado")
        categoria = "Alimentos"
    else:
        print("Categoria Eletronicos foi selecionado")
        categoria = "Eletronicos"
    
    print("Codigo:", linha1)
    print("Descricao:", linha2)
    print("Preco:", linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos(codigo, descricao, preco, categoria)VALUES(%s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def pesquisar_dados():
    termo_pesquisa = segunda_tela.lineEdit.text()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos WHERE descricao LIKE %s OR codigo LIKE %s OR categoria LIKE %s"
    cursor.execute(comando_SQL, ('%' + termo_pesquisa + '%', '%' + termo_pesquisa + '%', '%' + termo_pesquisa + '%'))
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(len(dados_lidos)):
        for j in range(5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app = QtWidgets.QApplication([])
formulario = uic.loadUi("C:/Users/evand/Desktop/Trabalho - Banco de Dados/projeto_formulario/formulario.ui")
segunda_tela = uic.loadUi("C:/Users/evand/Desktop/Trabalho - Banco de Dados/projeto_formulario/listar_dados.ui")
tela_editar = uic.loadUi("C:/Users/evand/Desktop/Trabalho - Banco de Dados/projeto_formulario/menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(editar_dados)
segunda_tela.lineEdit.textChanged.connect(pesquisar_dados)
tela_editar.pushButton_2.clicked.connect(salvar_dados_editados)


formulario.show()
app.exec()

