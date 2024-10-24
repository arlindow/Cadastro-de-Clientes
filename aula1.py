from tkinter import *
from tkinter import ttk
import sqlite3

"""--> resolver <erro01>
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import webbrowser
"""

root = Tk()

"""--> resolver <erro 01>
class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
        
    def geraRelatCliente(self):
        self.c = canvas.Canvas('cliente.pdf') 
        
        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.cpfRel = self.cpf_entry.get()
        self.ieRel = self.ie_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()
        self.ufRel = self.uf_entry.get()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(100, 790, 'Ficha do Cliente' )
        
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 780, 'codigo: ', self.codigoRel)
        self.c.drawString(50, 760, 'nome: ',self.nomeRel)
        self.c.drawString(50, 730, 'cpf/cnpj: ', self.cpfRel)
        self.c.drawString(50, 700, 'Inscrição Estadual: ', self.ieRel)
        self.c.drawString(50, 670, 'Telefone: ', self.telefoneRel)
        self.c.drawString(50, 640, 'Cidade: ', self.cidadeRel)
        self.c.drawString(50, 610, 'UF: ', self.ufRel)
        
        self.c.rect(20,550, 550, 5, filt=True, stroke=False)
        
        
        self.c.showPage()
        self.c.save()
        self.printCliente()
"""        
           
class Funcs():
    def limpa_tela(self):
        self.codigo_entry.config(state=NORMAL)  # Permitir edição antes de limpar
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.ie_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.uf_entry.delete(0, END)
        self.codigo_entry.config(state='readonly')  # Tornar o campo novamente não editável
        
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor(); print("conectado ao banco de dados")
    
    def desconecta_bd(self):
        self.conn.close(); print("desconectado do banco de dados")
    
    def montaTabelas(self):
        self.conecta_bd()
        
        ### Criar Tabela    
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                cpf_cnpj TEXT(15) NOT NULL,
                IE TEXT(15) NUll, 
                telefone INTEGER(20) NOT NULL,
                cidade CHAR(40) NOT NULL,
                uf CHAR(2) NOT NULL
                
                )""")
        
        self.conn.commit(); print("Banco de dados: clientes.db")
        self.desconecta_bd()
    
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.cpf = self.cpf_entry.get()
        self.ie = self.ie_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.uf = self.uf_entry.get()
    
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()
        
        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, cpf_cnpj, ie, telefone, cidade, uf)
                            VALUES (?, ?, ?, ?, ?, ?)""", (self.nome, self.cpf, self.ie, self.telefone, self.cidade, self.uf))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
        
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())        
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, cpf_cnpj, ie, telefone, cidade, uf 
                                    FROM clientes ORDER BY nome_cliente ASC; """)
        
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
        
    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()
        
        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.listaCli.item(n, 'values')
            self.codigo_entry.config(state=NORMAL)  # Permitir edição
            self.codigo_entry.insert(END, col1)
            self.codigo_entry.config(state='readonly')  # Tornar não editável novamente
            self.nome_entry.insert(END, col2)
            self.cpf_entry.insert(END, col3)
            self.ie_entry.insert(END, col4)
            self.telefone_entry.insert(END, col5)
            self.cidade_entry.insert(END, col6)
            self.uf_entry.insert(END, col7)
            
    def deleta_cliente(self):
        self.variaveis()
        print(f"Código do cliente a ser deletado: {self.codigo}")  # Verifique o valor de self.codigo
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
        
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente =?, cpf_cnpj =?, ie=?, telefone=?, cidade=?, uf=?
                            WHERE cod =? """,(self.nome, self.cpf, self.ie, self.telefone, self.cidade, self.uf,self.codigo ))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
        
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
        """ 
            SELECT cod, nome_cliente, cpf_cnpj, ie, telefone, cidade, uf FROM clientes 
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC
        """ % nome
        )
        buscanomeCLi = self.cursor.fetchall()
        for i in buscanomeCLi:
            self.listaCli.insert("",END, values=i)
                                 
        self.limpa_tela()    
        self.desconecta_bd()        

#  class Application(Funcs, Relatorios): após resolver <erro01>     
class Application(Funcs):
    def __init__(self):  # exibir janela
        self.root = root  # 1
        self.tela()
        self.frames_da_tela()
        self.widgets_frame()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        
        root.mainloop()
           
    def tela(self):
        self.root.title("Cadastro de Clientes")  # 1
        self.root.configure(background='blue')
        self.root.geometry('600x500')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#c0c0c0",
                             highlightbackground='#000000',
                             highlightthickness=3)
        self.frame_1.place(relx=0.021, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg="#c0c0c0",
                             highlightbackground='#000000',
                             highlightthickness=3)
        self.frame_2.place(relx=0.021, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame(self):
        # criação do botão limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=4, bg='#52c4e4', fg='white',
                                font=('verdana', 7, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # criação do botão buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=4, bg='#CCCC00', fg='white',
                                font=('verdana', 7, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # criação do botão novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd=4, bg='#6BB26B', fg='white',
                              font=('verdana', 7, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # criação do botão alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=4, bg='#7A378B', fg='white',
                                 font=('verdana', 7, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # criação do botão apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=4, bg='#B22222', fg='white',
                                font=('verdana', 7, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # label e entrada de dados
        self.lb_codigo = Label(self.frame_1, text="Codigo", bg='#000000', fg='white',
                               font=('verdana', 8, 'bold'))
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.codigo_entry.place(relx=0.05, rely=0.16, relwidth=0.08)
        self.codigo_entry.config(state='readonly')  # Torna o campo "Codigo" não editável

        # label e entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#000000', fg='white',
                             font=('verdana', 8, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.36)

        self.nome_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.nome_entry.place(relx=0.05, rely=0.47, relwidth=0.4)
        
        # label e entrada cpf
        self.lb_cpf = Label(self.frame_1, text="CPF ou CNPJ", bg='#000000', fg='white',
                             font=('verdana', 8, 'bold'))
        self.lb_cpf.place(relx=0.47, rely=0.36)
        
        self.cpf_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.cpf_entry.place(relx=0.47, rely=0.47, relwidth=0.3)
        
        # label e entrada inscrição estadual
        self.lb_ie = Label(self.frame_1, text="Inscrição Estadual", bg='#000000', fg='white',
                             font=('verdana', 7, 'bold'))
        self.lb_ie.place(relx=0.80, rely=0.36)
        
        self.ie_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.ie_entry.place(relx=0.80, rely=0.47, relwidth=0.20)
    
        # label e entrada do telefone
        self.lb_telefone = Label(self.frame_1, text="Telefone", bg='#000000', fg='white',
                                 font=('verdana', 8, 'bold'))
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.telefone_entry.place(relx=0.05, rely=0.71, relwidth=0.3)

        # label e entrada do cidade
        self.lb_cidade = Label(self.frame_1, text="Cidade", bg='#000000', fg='white',
                               font=('verdana', 8, 'bold'))
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.cidade_entry.place(relx=0.5, rely=0.71, relwidth=0.3)

        # label e entrada do uf
        self.lb_uf = Label(self.frame_1, text="UF", bg='#000000', fg='white',
                           font=('verdana', 8, 'bold'))
        self.lb_uf.place(relx=0.85, rely=0.6)

        self.uf_entry = Entry(self.frame_1, bd=2, bg='#E1E1E1', font=('verdana', 8, 'bold'))
        self.uf_entry.place(relx=0.85, rely=0.71, relwidth=0.1)

    def lista_frame2(self):
        
        # Criando o Treeview
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="cpf/cnpj")
        self.listaCli.heading("#4", text="ie")
        self.listaCli.heading("#5", text="Telefone")
        self.listaCli.heading("#6", text="Cidade")
        self.listaCli.heading("#7", text="UF")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=150)
        self.listaCli.column("#3", width=135)
        self.listaCli.column("#4", width=80)
        self.listaCli.column("#5", width=100)
        self.listaCli.column("#6", width=100)
        self.listaCli.column("#7", width=50)

        self.listaCli.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.85)
        
        # Scrollbar
        self.scrollLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.85)

        
        # Scrollbar Horizontal
        self.scrollListaHor = Scrollbar(self.frame_2, orient='horizontal', command=self.listaCli.xview)
        self.scrollListaHor.pack(side='bottom', fill='x')
        self.listaCli.configure(xscrollcommand=self.scrollListaHor.set)
        
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        
        def Quit(): self.root.destroy()
        
        menubar.add_cascade(label = "Opções", menu= filemenu)
        menubar.add_cascade(label = "Sobre", menu = filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Limpa Tela", command=self.limpa_tela)
        
        # <erro 01> filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)
        
        
        
Application()







