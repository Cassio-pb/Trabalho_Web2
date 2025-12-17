from flask import *
from dao.banco import init_db, SessionLocal
from dao.usuarioDAO import *
from dao.hamburguerDAO import *

app = Flask(__name__)
app.secret_key = 'cassinepedrin'

hamburgueres = listar_hambuerguer()
pedidos = []

usuarios = None

init_db()

@app.before_request
def pegar_sessao():
    g.session = SessionLocal()

@app.teardown_appcontext
def encerrar_sessao(exception=None):
    SessionLocal.remove()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fazerlogin', methods=['POST', 'GET'])
def fazer_login():

    if request.method == 'GET' and 'login' in session:
        return render_template('logado.html')

    login = request.form.get('loginusuario')
    senha = request.form.get('senhausuario')

    usuario_dao = UsuarioDAO(g.session)

    #if verificar_login(usuarios, login, senha):
    usuario = usuario_dao.autenticar(login, senha)
    if usuario:
        print(usuario)
        session['login'] = login
        return render_template('pedidos.html', hamburgueres = listar_hambuerguer() )
    else:
        #aqui o usuario digitou o login ou senha errado
        msg = 'Usuário ou senha inválidos'
        return render_template('index.html', texto=msg)

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method == 'GET':
        return render_template('paginacadastro.html')

    usuario_dao = UsuarioDAO(g.session)

    nome = request.form.get('nomeuser')
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirma = request.form.get('confirmacao')

    if senha == confirma:
        novo_usuario = Usuario(email=email, nome=nome, senha=senha)
        usuario_dao.criar(novo_usuario)
        return render_template('index.html')
    else:
        msg = 'a senha e a confirmação de senha não são iguais'
        return render_template('paginacadastro.html', msg=msg)



@app.route('/fazerPedido', methods=['POST'])
def fazerPedido():
    nome = request.form['nome']
    hamburguer_nome = request.form['hamburguer']
    quantidade = int(request.form.get('quantidade', 1))
    if quantidade < 1:
        quantidade = 1
    elif quantidade > 99:
        quantidade = 99

    # Busca o preco do hamburguer selecionado
    preco_unitario = 0
    for h in hamburgueres:
        if h['nome'] == hamburguer_nome:
            preco_unitario = h['preco']
            break

    total = quantidade * preco_unitario

    pedido = {
        'nome': nome,
        'hamburguer': hamburguer_nome,
        'quantidade': quantidade,
        'preco_unitario': preco_unitario,
        'total': total
    }

    pedidos.append(pedido)
    session['ultimoPedido'] = pedido

    return redirect('/pedidoConfirmado')

@app.route('/pedidoConfirmado')
def pedidoConfirmado():
    pedido = session.get('ultimoPedido')
    if not pedido:
        return redirect('/')
    return render_template('pedidoConfirmado.html', pedido=pedido)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '1':
            session['admin'] = True
            return redirect('/homepage')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/homepage')
def homepage():
    if not session.get('admin'):
        return redirect('/login')
    return render_template('homepage.html')

@app.route('/pedidos')
def mostrarPedidos():
    if not session.get('admin'):
        return redirect('/login')
    return render_template('gerenciarPedidos.html', pedidos=pedidos)

@app.route('/gerenciar', methods=['GET', 'POST'])
def gerenciar():
    if not session.get('admin'):
        return redirect('/login')

    mensagem = ''
    if request.method == 'POST':
        if 'adicionar' in request.form:
            nome = request.form['nome']
            ingredientes = request.form['ingredientes']
            try:
                preco = float(request.form['preco'])
            except ValueError:
                preco = 0.0
            
            resultado = criar_hamburguer(nome,ingredientes,preco)
            print(f'resultado:{resultado}')
        elif 'remover' in request.form:
            nome = request.form['nome']

            resul = remover_hamburguer(nome)
            if resul:
                print(f'hamburguer removido')
    hamburgueres = listar_hambuerguer()
    print(f'lista de hamburgueres:{hamburgueres}')

    return render_template('gerenciar.html', hamburgueres=hamburgueres, mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)