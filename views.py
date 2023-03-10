# importação de dependencias
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory,send_file
from flask_qrcode import QRcode
import time
from datetime import date, timedelta
from ecocollect import app, db
from sqlalchemy import func
from models import tb_user,\
    tb_usertype,\
    tb_residuos,\
    tb_destinadores,\
    tb_tiposveiculo,\
    tb_veiculos,\
    tb_motoristas,\
    tb_clientes,\
    tb_pontoscoleta,\
    tb_periodicidade,\
    tb_acondicionamento,\
    tb_pontocoleta_residuo
from helpers import \
    frm_pesquisa, \
    frm_editar_senha,\
    frm_editar_usuario,\
    frm_visualizar_usuario, \
    frm_visualizar_tipousuario,\
    frm_editar_tipousuario,\
    frm_editar_residuo,\
    frm_visualizar_residuo,\
    frm_editar_destinador,\
    frm_visualizar_destinador,\
    frm_editar_tipoveiculo,\
    frm_visualizar_tipoveiculo,\
    frm_editar_veiculo,\
    frm_visualizar_veiculo,\
    frm_editar_motorista,\
    frm_visualizar_motorista,\
    frm_editar_cliente,\
    frm_visualizar_cliente,\
    frm_editar_pontocoleta,\
    frm_visualizar_pontocoleta,\
    frm_editar_acondicionamento,\
    frm_visualizar_acondicionamento,\
    frm_editar_periodicidade,\
    frm_visualizar_periodicidade,\
    frm_editar_pontocoleta_residuo,\
    frm_visualizar_pontocoleta_residuo


# ITENS POR PÁGINA
from config import ROWS_PER_PAGE, CHAVE
from flask_bcrypt import generate_password_hash, Bcrypt, check_password_hash

import string
import random
import numbers

##################################################################################################################################
#GERAL
##################################################################################################################################


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: index
#FUNÇÃO: mostrar pagina principal
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))        
    return render_template('index.html', titulo='Bem vindos')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: logout
#FUNÇÃO: remover seção usuário
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso','success')
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: login
#FUNÇÃO: iniciar seção do usuário
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: autenticar
#FUNÇÃO: autenticar
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    usuario = tb_user.query.filter_by(login_user=request.form['usuario']).first()
    senha = check_password_hash(usuario.password_user,request.form['senha'])
    if usuario:
        if senha:
            session['usuario_logado'] = usuario.login_user
            session['nomeusuario_logado'] = usuario.name_user
            session['tipousuario_logado'] = usuario.cod_usertype
            session['coduser_logado'] = usuario.cod_user
            flash(usuario.name_user + ' Usuário logado com sucesso','success')
            #return redirect('/')
            return redirect('/')
        else:
            flash('Verifique usuário e senha', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso','success')
        return redirect(url_for('login'))

##################################################################################################################################
#USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: usuario
#FUNÇÃO: listar
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/usuario', methods=['POST','GET'])
def usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('usuario')))        
    form = frm_pesquisa()
    page = request.args.get('page', 1, type=int)
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data

    if pesquisa == "" or pesquisa == None:    
        usuarios = tb_user.query\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    else:
        usuarios = tb_user.query\
        .filter(tb_user.name_user.ilike(f'%{pesquisa}%'))\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)


    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoUsuario
#FUNÇÃO: formulário inclusão
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/novoUsuario')
def novoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoUsuario')))     
    form = frm_editar_usuario()
    return render_template('novoUsuario.html', titulo='Novo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuario
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarUsuario', methods=['POST',])
def criarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('criarUsuario')))      
    form = frm_editar_usuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoUsuario'))
    nome  = form.nome.data
    status = form.status.data
    login = form.login.data
    tipousuario = form.tipousuario.data
    email = form.email.data
    #criptografar senha
    senha = generate_password_hash("teste@12345").decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('index')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso','success')
    return redirect(url_for('usuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuarioexterno - NÃO DISPONIVEL NESTA VERSAO
#FUNÇÃO: formulário de inclusão
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/criarUsuarioexterno', methods=['POST',])
def criarUsuarioexterno():    
    nome  = request.form['nome']
    status = 0
    email = request.form['email']
    localarroba = email.find("@")
    login = email[0:localarroba]
    tipousuario = 2
    #criptografar senha
    senha = generate_password_hash(request.form['senha']).decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('login')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso, favor logar com ele','success')
    return redirect(url_for('login'))  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarUsuario
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarUsuario/<int:id>')
def visualizarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = frm_visualizar_usuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('visualizarUsuario.html', titulo='Visualizar Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarUsuario
#FUNÇÃO: formulario de edição
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/editarUsuario/<int:id>')
def editarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarUsuario/<int:id>')))  
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = frm_editar_usuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('editarUsuario.html', titulo='Editar Usuário', id=id, form=form)    
       
#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarUsuario
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = frm_editar_usuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('atualizarUsuario'))
    id = request.form['id']
    usuario = tb_user.query.filter_by(cod_user=request.form['id']).first()
    usuario.name_user = form.nome.data
    usuario.status_user = form.status.data
    usuario.login_user = form.login.data
    usuario.cod_uertype = form.tipousuario.data
    db.session.add(usuario)
    db.session.commit()
    flash('Usuário alterado com sucesso','success')
    return redirect(url_for('visualizarUsuario', id=request.form['id']))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarSenhaUsuario
#FUNÇÃO: formulario de edição
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarSenhaUsuario/')
def editarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    form = frm_editar_senha()
    return render_template('trocarsenha.html', titulo='Trocar Senha', id=id, form=form)  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: trocarSenhaUsuario
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/trocarSenhaUsuario', methods=['POST',])
def trocarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = frm_editar_senha(request.form)
    if form.validate_on_submit():
        id = session['coduser_logado']
        usuario = tb_user.query.filter_by(cod_user=id).first()
        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario'))

        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario')) 

        if form.novasenha1.data != form.novasenha2.data:
            flash('novas senhas não coincidem','danger')
            return redirect(url_for('editarSenhaUsuario')) 
        usuario.password_user = generate_password_hash(form.novasenha1.data).decode('utf-8')
        db.session.add(usuario)
        db.session.commit()
        flash('senha alterada com sucesso!','success')
    else:
        flash('senha não alterada!','danger')
    return redirect(url_for('editarSenhaUsuario')) 

##################################################################################################################################
#TIPO DE USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipousuario
#FUNÇÃO: listar
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipousuario', methods=['POST','GET'])
def tipousuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipousuario')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .filter(tb_usertype.desc_usertype.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipousuarios.html', titulo='Tipo Usuário', tiposusuario=tiposusuario, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoUsuario
#FUNÇÃO: formulario de inclusão
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoUsuario')
def novoTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoUsuario'))) 
    form = frm_editar_tipousuario()
    return render_template('novoTipoUsuario.html', titulo='Novo Tipo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoUsuario
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoUsuario', methods=['POST',])
def criarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoUsuario')))     
    form = frm_editar_tipousuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoUsuario'))
    desc  = form.descricao.data
    status = form.status.data
    tipousuario = tb_usertype.query.filter_by(desc_usertype=desc).first()
    if tipousuario:
        flash ('Tipo Usuário já existe','danger')
        return redirect(url_for('tipousuario')) 
    novoTipoUsuario = tb_usertype(desc_usertype=desc, status_usertype=status)
    flash('Tipo de usuário criado com sucesso!','success')
    db.session.add(novoTipoUsuario)
    db.session.commit()
    return redirect(url_for('tipousuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoUsuario
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoUsuario/<int:id>')
def visualizarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = frm_visualizar_tipousuario()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('visualizarTipoUsuario.html', titulo='Visualizar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoUsuario
##FUNÇÃO: formulário de edição
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoUsuario/<int:id>')
def editarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = frm_editar_tipousuario()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('editarTipoUsuario.html', titulo='Editar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoUsuario
#FUNÇÃO: alterar informações no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoUsuario', methods=['POST',])
def atualizarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoUsuario')))      
    form = frm_editar_tipousuario(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipousuario = tb_usertype.query.filter_by(cod_usertype=request.form['id']).first()
        tipousuario.desc_usertype = form.descricao.data
        tipousuario.status_usertype = form.status.data
        db.session.add(tipousuario)
        db.session.commit()
        flash('Tipo de usuário atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoUsuario', id=request.form['id']))

##################################################################################################################################
#RESIUDOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: residuo
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/residuo', methods=['POST','GET'])
def residuo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('residuo')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        residuos = tb_residuos.query.order_by(tb_residuos.desc_residuo)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        residuos = tb_residuos.query.order_by(tb_residuos.desc_residuo)\
        .filter(tb_residuos.desc_residuo.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('residuo.html', titulo='Resíduos', residuos=residuos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoResiduo
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoResiduo')
def novoResiduo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoResiduo'))) 
    form = frm_editar_residuo()
    return render_template('novoResiduo.html', titulo='Novo Resíduo', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarResiduo
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarResiduo', methods=['POST',])
def criarResiduo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarResiduo')))     
    form = frm_editar_residuo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarResiduo'))
    desc  = form.descricao.data
    status = form.status.data
    residuo = tb_residuos.query.filter_by(desc_residuo=desc).first()
    if residuo:
        flash ('Resíduo já existe','danger')
        return redirect(url_for('residuo')) 
    novoResiduo = tb_residuos(desc_residuo=desc, status_residuo=status)
    flash('Resíduo criado com sucesso!','success')
    db.session.add(novoResiduo)
    db.session.commit()
    return redirect(url_for('residuo'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarResiduo
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarResiduo/<int:id>')
def visualizarResiduo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarResiduo')))  
    residuo = tb_residuos.query.filter_by(cod_residuo=id).first()
    form = frm_visualizar_residuo()
    form.descricao.data = residuo.desc_residuo
    form.status.data = residuo.status_residuo
    return render_template('visualizarResiduo.html', titulo='Visualizar Residuo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarResiduo
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarResiduo/<int:id>')
def editarResiduo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarResiduo')))  
    residuo = tb_residuos.query.filter_by(cod_residuo=id).first()
    form = frm_editar_residuo()
    form.descricao.data = residuo.desc_residuo
    form.status.data = residuo.status_residuo
    return render_template('editarResiduo.html', titulo='Editar Resíduo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarResiduo
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarResiduo', methods=['POST',])
def atualizarResiduo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarResiduo')))      
    form = frm_editar_residuo(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        residuo = tb_residuos.query.filter_by(cod_residuo=request.form['id']).first()
        residuo.desc_residuo = form.descricao.data
        residuo.status_residuo = form.status.data
        db.session.add(residuo)
        db.session.commit()
        flash('Resíduo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarResiduo', id=request.form['id']))    

##################################################################################################################################
#DESTINADORES
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: destinador
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/destinador', methods=['POST','GET'])
def destinador():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('destinador')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        destinadores = tb_destinadores.query.order_by(tb_destinadores.desc_destinador)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        destinadores = tb_destinadores.query.order_by(tb_destinadores.desc_destinador)\
        .filter(tb_destinadores.desc_destinador.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('destinador.html', titulo='Destinadores', destinadores=destinadores, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoDestinador
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoDestinador')
def novoDestinador():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoDestinador'))) 
    form = frm_editar_destinador()
    return render_template('novoDestinador.html', titulo='Novo Destinador', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarDestinador
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarDestinador', methods=['POST',])
def criarDestinador():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarDestinador')))     
    form = frm_editar_destinador(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarResiduo'))
    desc  = form.descricao.data
    endereco  = form.endereco.data
    status = form.status.data
    destinador = tb_destinadores.query.filter_by(desc_destinador=desc).first()
    if destinador:
        flash ('Destinador já existe','danger')
        return redirect(url_for('residuo')) 
    novoDestinador = tb_destinadores(desc_destinador=desc, end_destinador=endereco, status_destinador=status)
    flash('Destinador criado com sucesso!','success')
    db.session.add(novoDestinador)
    db.session.commit()
    return redirect(url_for('destinador'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarDestinador
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarDestinador/<int:id>')
def visualizarDestinador(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarDestinador')))  
    destinador = tb_destinadores.query.filter_by(cod_destinador=id).first()
    form = frm_visualizar_destinador()
    form.descricao.data = destinador.desc_destinador
    form.endereco.data = destinador.end_destinador
    form.status.data = destinador.status_destinador
    return render_template('visualizarDestinador.html', titulo='Visualizar Destinador', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarDestinador
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarDestinador/<int:id>')
def editarDestinador(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarDestinador')))  
    destinador = tb_destinadores.query.filter_by(cod_destinador=id).first()
    form = frm_editar_destinador()
    form.descricao.data = destinador.desc_destinador
    form.endereco.data = destinador.end_destinador
    form.status.data = destinador.status_destinador
    return render_template('editarDestinador.html', titulo='Editar Destinador', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarDestinador
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarDestinador', methods=['POST',])
def atualizarDestinador():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarDestinador')))      
    form = frm_editar_destinador(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        destinador = tb_destinadores.query.filter_by(cod_destinador=request.form['id']).first()
        destinador.desc_destinador = form.descricao.data
        destinador.end_destinador = form.endereco.data
        destinador.status_destinador = form.status.data
        db.session.add(destinador)
        db.session.commit()
        flash('Destinador atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarDestinador', id=request.form['id']))  

##################################################################################################################################
#TIPO VEICULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipoveiculo
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipoveiculo', methods=['POST','GET'])
def tipoveiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipoveiculo')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tiposveiculo = tb_tiposveiculo.query.order_by(tb_tiposveiculo.desc_tipoveiculo)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tiposveiculo = tb_tiposveiculo.query.order_by(tb_tiposveiculo.desc_tipoveiculo)\
        .filter(tb_tiposveiculo.desc_tipoveiculo.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipoveiculo.html', titulo='Tipo Veículo', tiposveiculo=tiposveiculo, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoVeiculo
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoVeiculo')
def novoTipoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoVeiculo'))) 
    form = frm_editar_tipoveiculo()
    return render_template('novoTipoVeiculo.html', titulo='Novo Tipo Veículo', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoVeiculo
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoVeiculo', methods=['POST',])
def criarTipoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoVeiculo')))     
    form = frm_editar_tipoveiculo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarResiduo'))
    desc  = form.descricao.data
    status = form.status.data
    tipoveiculo = tb_tiposveiculo.query.filter_by(desc_tipoveiculo=desc).first()
    if tipoveiculo:
        flash ('Tipo veículo já existe','danger')
        return redirect(url_for('tipoveiculo')) 
    novoTipoVeiculo = tb_tiposveiculo(desc_tipoveiculo=desc, status_tipoveiculo=status)
    flash('Tipo veículo criado com sucesso!','success')
    db.session.add(novoTipoVeiculo)
    db.session.commit()
    return redirect(url_for('tipoveiculo'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoVeiculo
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoVeiculo/<int:id>')
def visualizarTipoVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoVeiculo')))  
    tipoveiculo = tb_tiposveiculo.query.filter_by(cod_tipoveiculo=id).first()
    form = frm_visualizar_tipoveiculo()
    form.descricao.data = tipoveiculo.desc_tipoveiculo
    form.status.data = tipoveiculo.status_tipoveiculo
    return render_template('visualizarTipoVeiculo.html', titulo='Visualizar Tipo Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoVeiculo
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoVeiculo/<int:id>')
def editarTipoVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoVeiculo')))  
    tipoveiculo = tb_tiposveiculo.query.filter_by(cod_tipoveiculo=id).first()
    form = frm_editar_tipoveiculo()
    form.descricao.data = tipoveiculo.desc_tipoveiculo
    form.status.data = tipoveiculo.status_tipoveiculo
    return render_template('editarTipoVeiculo.html', titulo='Editar Tipo Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoVeiculo
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoVeiculo', methods=['POST',])
def atualizarTipoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoVeiculo')))      
    form = frm_editar_tipoveiculo(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipoveiculo = tb_tiposveiculo.query.filter_by(cod_tipoveiculo=request.form['id']).first()
        tipoveiculo.desc_tipoveiculo = form.descricao.data
        tipoveiculo.status_tipoveiculo = form.status.data
        db.session.add(tipoveiculo)
        db.session.commit()
        flash('Tipo Veículo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoVeiculo', id=request.form['id']))

##################################################################################################################################
#VEICULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: veiculo
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/veiculo', methods=['POST','GET'])
def veiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('veiculo')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        veiculos = tb_veiculos.query.order_by(tb_veiculos.placa_veiculo)\
        .join(tb_tiposveiculo, tb_tiposveiculo.cod_tipoveiculo==tb_veiculos.cod_tipoveiculo)\
        .add_columns(tb_veiculos.cod_veiculo, tb_veiculos.placa_veiculo, tb_tiposveiculo.desc_tipoveiculo, tb_veiculos.status_veiculo)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        veiculos = tb_veiculos.query.order_by(tb_veiculos.placa_veiculo)\
        .join(tb_tiposveiculo, tb_tiposveiculo.cod_tipoveiculo==tb_veiculos.cod_tipoveiculo)\
        .add_columns(tb_veiculos.cod_veiculo, tb_veiculos.placa_veiculo, tb_tiposveiculo.desc_tipoveiculo, tb_veiculos.status_veiculo)\
        .filter(tb_veiculos.placa_veiculo.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('veiculo.html', titulo='Veículos', veiculos=veiculos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoVeiculo
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoVeiculo')
def novoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoVeiculo'))) 
    form = frm_editar_veiculo()
    return render_template('novoVeiculo.html', titulo='Novo Veículo', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarVeiculo
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarVeiculo', methods=['POST',])
def criarVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarVeiculo')))     
    form = frm_editar_veiculo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarVeiculo'))
    placa  = form.placa.data
    tipoveiculo  = form.tipoveiculo.data
    status = form.status.data
    veiculo = tb_veiculos.query.filter_by(placa_veiculo=placa).first()
    if veiculo:
        flash ('Veículo já existe','danger')
        return redirect(url_for('veiculo')) 
    novoVeiculo = tb_veiculos(placa_veiculo=placa, cod_tipoveiculo=tipoveiculo, status_veiculo=status)
    flash('Veículo criado com sucesso!','success')
    db.session.add(novoVeiculo)
    db.session.commit()
    return redirect(url_for('veiculo'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarVeiculo
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarVeiculo/<int:id>')
def visualizarVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarVeiculo')))  
    veiculo = tb_veiculos.query.filter_by(cod_veiculo=id).first()
    form = frm_visualizar_veiculo()
    form.placa.data = veiculo.placa_veiculo
    form.tipoveiculo.data = veiculo.cod_tipoveiculo
    form.status.data = veiculo.status_veiculo
    return render_template('visualizarVeiculo.html', titulo='Visualizar Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarVeiculo
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarVeiculo/<int:id>')
def editarVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarVeiculo')))  
    veiculo = tb_veiculos.query.filter_by(cod_veiculo=id).first()
    form = frm_editar_veiculo()
    form.placa.data = veiculo.placa_veiculo
    form.tipoveiculo.data = veiculo.cod_tipoveiculo
    form.status.data = veiculo.status_veiculo
    return render_template('editarVeiculo.html', titulo='Editar Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarVeiculo
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarVeiculo', methods=['POST',])
def atualizarVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarVeiculo')))      
    form = frm_editar_veiculo(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        veiculo = tb_veiculos.query.filter_by(cod_veiculo=request.form['id']).first()
        veiculo.placa_veiculo = form.placa.data
        veiculo.cod_tipoveiculo = form.tipoveiculo.data
        veiculo.status_tipoveiculo = form.status.data
        db.session.add(veiculo)
        db.session.commit()
        flash('Veículo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarVeiculo', id=request.form['id']))  

##################################################################################################################################
#MOTORISTAS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: motorista
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/motorista', methods=['POST','GET'])
def motorista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('motorista')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        motoristas = tb_motoristas.query.order_by(tb_motoristas.nome_motorista)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        motoristas = tb_motoristas.query.order_by(tb_motoristas.nome_motorista)\
        .filter(tb_motoristas.nome_motorista.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('motorista.html', titulo='Motoristas', motoristas=motoristas, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoMotorista
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoMotorista')
def novoMotorista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoMotorista'))) 
    form = frm_editar_motorista()
    return render_template('novoMotorista.html', titulo='Novo Motorista', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarMotorista
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarMotorista', methods=['POST',])
def criarMotorista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarMotorista')))     
    form = frm_editar_motorista(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarMotorista'))
    nome  = form.nome.data
    status = form.status.data
    motorista = tb_motoristas.query.filter_by(nome_motorista=nome).first()
    if motorista:
        flash ('Motorista já existe','danger')
        return redirect(url_for('motorista')) 
    novoMotorista = tb_motoristas(nome_motorista=nome, status_motorista=status)
    flash('Motorista criado com sucesso!','success')
    db.session.add(novoMotorista)
    db.session.commit()
    return redirect(url_for('motorista'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarMotorista
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarMotorista/<int:id>')
def visualizarMotorista(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarMotorista')))  
    motorista = tb_motoristas.query.filter_by(cod_motorista=id).first()
    form = frm_visualizar_motorista()
    form.nome.data = motorista.nome_motorista
    form.status.data = motorista.status_motorista
    return render_template('visualizarMotorista.html', titulo='Visualizar Motorista', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarMotorista
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarMotorista/<int:id>')
def editarMotorista(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarMotorista')))  
    motorista = tb_motoristas.query.filter_by(cod_motorista=id).first()
    form = frm_editar_motorista()
    form.nome.data = motorista.nome_motorista
    form.status.data = motorista.status_motorista
    return render_template('editarMotorista.html', titulo='Editar Motorista', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarMotorista
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarMotorista', methods=['POST',])
def atualizarMotorista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarMotorista')))      
    form = frm_editar_motorista(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        motorista = tb_motoristas.query.filter_by(cod_motorista=request.form['id']).first()
        motorista.nome_motorista = form.nome.data
        motorista.status_motorista = form.status.data
        db.session.add(motorista)
        db.session.commit()
        flash('Motorista atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarMotorista', id=request.form['id']))

##################################################################################################################################
#CLIENTE
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: cliente
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/cliente', methods=['POST','GET'])
def cliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('cliente')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        clientes = tb_clientes.query.order_by(tb_clientes.nome_cliente)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        clientes = tb_clientes.query.order_by(tb_clientes.desc_destinador)\
        .filter(tb_clientes.nome_cliente.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('cliente.html', titulo='Clientes', clientes=clientes, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoCliente
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoCliente')
def novoCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoCliente'))) 
    form = frm_editar_cliente()
    return render_template('novoCliente.html', titulo='Novo Cliente', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarCliente
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarCliente', methods=['POST',])
def criarCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarCliente')))     
    form = frm_editar_cliente(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarCliente'))
    nome  = form.nome.data
    endereco  = form.endereco.data
    status = form.status.data
    cliente = tb_clientes.query.filter_by(nome_cliente=nome).first()
    if cliente:
        flash ('Cliente já existe','danger')
        return redirect(url_for('cliente')) 
    novoCliente = tb_clientes(nome_cliente=nome, end_cliente=endereco, status_cliente=status)
    flash('Cliente criado com sucesso!','success')
    db.session.add(novoCliente)
    db.session.commit()
    return redirect(url_for('cliente'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarCliente
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarCliente/<int:id>')
def visualizarCliente(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarCliente')))  
    cliente = tb_clientes.query.filter_by(cod_cliente=id).first()
    #pontoscoleta = tb_pontoscoleta.query.filter_by(cod_cliente=cliente.cod_cliente)

    pontoscoleta = tb_pontoscoleta.query.order_by(tb_pontoscoleta.nome_pontocoleta)\
        .filter(tb_pontoscoleta.cod_cliente == id)
    

    form = frm_visualizar_cliente()
    form.nome.data = cliente.nome_cliente
    form.endereco.data = cliente.end_cliente
    form.status.data = cliente.status_cliente
    endereco = cliente.end_cliente
    return render_template('visualizarCliente.html', titulo='Visualizar Cliente', id=id, form=form, pontoscoleta=pontoscoleta,endereco=endereco)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarCliente
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarCliente/<int:id>')
def editarCliente(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarCliente')))  
    cliente = tb_clientes.query.filter_by(cod_cliente=id).first()
    form = frm_editar_cliente()
    form.nome.data = cliente.nome_cliente
    form.endereco.data = cliente.end_cliente
    form.status.data = cliente.status_cliente
    return render_template('editarCliente.html', titulo='Editar Cliente', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarCliente
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarCliente', methods=['POST',])
def atualizarCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarCliente')))      
    form = frm_editar_cliente(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        cliente = tb_clientes.query.filter_by(cod_cliente=request.form['id']).first()
        cliente.nome_cliente = form.nome.data
        cliente.end_cliente = form.endereco.data
        cliente.status_cliente = form.status.data
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarCliente', id=request.form['id']))
##################################################################################################################################
#ACONDICIONAMENTO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: acondicionamento
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/acondicionamento', methods=['POST','GET'])
def acondicionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('acondicionamento')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        acondicionamentos = tb_acondicionamento.query.order_by(tb_acondicionamento.desc_acondicionamento)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        acondicionamentos = tb_acondicionamento.query.order_by(tb_acondicionamento.desc_acondicionamento)\
        .filter(tb_acondicionamento.desc_acondicionamento.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('acondicionamento.html', titulo='Acondicionamento', acondicionamentos=acondicionamentos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoAcondicionamento
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoAcondicionamento')
def novoAcondicionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoAcondicionamento'))) 
    form = frm_editar_acondicionamento()
    return render_template('novoAcondicionamento.html', titulo='Novo Acondicionamento', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarAcondicionamento
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarAcondicionamento', methods=['POST',])
def criarAcondicionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarAcondicionamento')))     
    form = frm_editar_acondicionamento(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarAcondicionamento'))
    desc  = form.descricao.data
    status = form.status.data
    acondicionamento = tb_acondicionamento.query.filter_by(desc_acondicionamento=desc).first()
    if acondicionamento:
        flash ('Acondicionamento já existe','danger')
        return redirect(url_for('acondicionamento')) 
    novoAcondicionamento = tb_acondicionamento(desc_acondicionamento=desc, status_acondicionamento=status)
    flash('Acondicionamento criado com sucesso!','success')
    db.session.add(novoAcondicionamento)
    db.session.commit()
    return redirect(url_for('acondicionamento'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarAcondicionamento
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarAcondicionamento/<int:id>')
def visualizarAcondicionamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarAcondicionamento')))  
    acondicionamento = tb_acondicionamento.query.filter_by(cod_acondicionamento=id).first()
    form = frm_visualizar_acondicionamento()
    form.descricao.data = acondicionamento.desc_acondicionamento
    form.status.data = acondicionamento.status_acondicionamento
    return render_template('visualizarAcondicionamento.html', titulo='Visualizar Acondicionamento', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarAcondicionamento
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarAcondicionamento/<int:id>')
def editarAcondicionamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarAcondicionamento')))  
    acondicionamento = tb_acondicionamento.query.filter_by(cod_acondicionamento=id).first()
    form = frm_editar_acondicionamento()
    form.descricao.data = acondicionamento.desc_acondicionamento
    form.status.data = acondicionamento.status_acondicionamento
    return render_template('editarAcondicionamento.html', titulo='Editar Acondicionamento', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarAcondicionamento
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarAcondicionamento', methods=['POST',])
def atualizarAcondicionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarAcondicionamento')))      
    form = frm_editar_acondicionamento(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        acondicionamento = tb_acondicionamento.query.filter_by(cod_acondicionamento=request.form['id']).first()
        acondicionamento.desc_acondicionamento = form.descricao.data
        acondicionamento.status_acondicionamento = form.status.data
        db.session.add(acondicionamento)
        db.session.commit()
        flash('Acondicionamento atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarAcondicionamento', id=request.form['id']))   

##################################################################################################################################
#PERIODICIDADE
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: periodicidade
#FUNÇÃO: listar informações
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/periodicidade', methods=['POST','GET'])
def periodicidade():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('periodicidade')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        periodicidades = tb_periodicidade.query.order_by(tb_periodicidade.desc_periodicidade)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        periodicidades = tb_periodicidade.query.order_by(tb_periodicidade.desc_periodicidade)\
        .filter(tb_periodicidade.desc_periodicidade.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('periodicidade.html', titulo='Periodicidade', periodicidades=periodicidades, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoPeriodicidade
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoPeriodicidade')
def novoPeriodicidade():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoPeriodicidade'))) 
    form = frm_editar_residuo()
    return render_template('novoPeriodicidade.html', titulo='Nova Periodicidade', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarPeriodicidade
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarPeriodicidade', methods=['POST',])
def criarPeriodicidade():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarPeriodicidade')))     
    form = frm_editar_periodicidade(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarPeriodicidade'))
    desc  = form.descricao.data
    status = form.status.data
    periodicidade = tb_periodicidade.query.filter_by(desc_periodicidade=desc).first()
    if periodicidade:
        flash ('Periodicidade já existe','danger')
        return redirect(url_for('periodicidade')) 
    novoPeriodicidade = tb_periodicidade(desc_periodicidade=desc, status_periodicidade=status)
    flash('Periodicidade criada com sucesso!','success')
    db.session.add(novoPeriodicidade)
    db.session.commit()
    return redirect(url_for('periodicidade'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarPeriodicidade
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarPeriodicidade/<int:id>')
def visualizarPeriodicidade(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarPeriodicidade')))  
    periodicidade = tb_periodicidade.query.filter_by(cod_periodicidade=id).first()
    form = frm_visualizar_periodicidade()
    form.descricao.data = periodicidade.desc_periodicidade
    form.status.data = periodicidade.status_periodicidade
    return render_template('visualizarPeriodicidade.html', titulo='Visualizar Periodicidade', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarPeriodicidade
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarPeriodicidade/<int:id>')
def editarPeriodicidade(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarPeriodicidade')))  
    periodicidade = tb_periodicidade.query.filter_by(cod_periodicidade=id).first()
    form = frm_editar_periodicidade()
    form.descricao.data = periodicidade.desc_periodicidade
    form.status.data = periodicidade.status_periodicidade
    return render_template('editarPeriodicidade.html', titulo='Editar Periodicidade', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarPeriodicidade
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarPeriodicidade', methods=['POST',])
def atualizarPeriodicidade():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarPeriodicidade')))      
    form = frm_editar_periodicidade(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        periodicidade = tb_periodicidade.query.filter_by(cod_periodicidade=request.form['id']).first()
        periodicidade.desc_periodicidade = form.descricao.data
        periodicidade.status_periodicidade = form.status.data
        db.session.add(periodicidade)
        db.session.commit()
        flash('Periodicidade atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarPeriodicidade', id=request.form['id'])) 

##################################################################################################################################
#PONTO DE COLETA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoCliente
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoPontoColeta/<int:idcliente>')
def novoPontoColeta(idcliente):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoPontoColeta'))) 
    form = frm_editar_pontocoleta()
    return render_template('novoPontoColeta.html', titulo='Novo Ponto Coleta', form=form, idcliente=idcliente)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarPontoColeta
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarPontoColeta/<int:idcliente>', methods=['POST','GET'])
def criarPontoColeta(idcliente):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoPontoColeta',idcliente=idcliente)))     
    form = frm_editar_pontocoleta(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoPontoColeta',idcliente=idcliente))
    nome  = form.nome.data
    endereco  = form.endereco.data
    status = form.status.data
    novoPontoColeta = tb_pontoscoleta(nome_pontocoleta=nome, end_pontocoleta=endereco, status_pontocoleta=status, cod_cliente=idcliente)
    flash('Ponto Coleta criado com sucesso!','success')
    db.session.add(novoPontoColeta)
    db.session.commit()
    return redirect(url_for('visualizarCliente',id=idcliente))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarPontoColeta
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarPontoColeta/<int:idpontocoleta>')
def visualizarPontoColeta(idpontocoleta):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarPontoColeta')))  
    pontocoleta = tb_pontoscoleta.query.filter_by(cod_pontocoleta=idpontocoleta).first()
    id = pontocoleta.cod_cliente


    residuospontocoleta = tb_pontocoleta_residuo.query.order_by(tb_pontocoleta_residuo.cod_pontocoleta_residuo)\
        .filter(tb_pontocoleta_residuo.cod_pontocoleta == idpontocoleta)\
        .join(tb_residuos, tb_residuos.cod_residuo==tb_pontocoleta_residuo.cod_residuo)\
        .join(tb_acondicionamento, tb_acondicionamento.cod_acondicionamento==tb_pontocoleta_residuo.cod_acondicionamento)\
        .add_columns(tb_pontocoleta_residuo.cod_pontocoleta_residuo, tb_pontocoleta_residuo.cod_pontocoleta, tb_acondicionamento.desc_acondicionamento, tb_residuos.desc_residuo,tb_pontocoleta_residuo.status_pontocoleta_residuo)\
    
    form = frm_visualizar_pontocoleta()
    form.nome.data = pontocoleta.nome_pontocoleta
    form.endereco.data = pontocoleta.end_pontocoleta
    form.status.data = pontocoleta.status_pontocoleta
    endereco=pontocoleta.end_pontocoleta
    return render_template('visualizarPontoColeta.html', titulo='Visualizar Ponto de Coleta', id=id, form=form, idpontocoleta=idpontocoleta,residuospontocoleta=residuospontocoleta,endereco=endereco)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarPontoColeta
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarPontoColeta/<int:idpontocoleta>')
def editarPontoColeta(idpontocoleta):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarPontoColeta')))  
    pontocoleta = tb_pontoscoleta.query.filter_by(cod_pontocoleta=idpontocoleta).first()
    id = pontocoleta.cod_cliente
    form = frm_editar_pontocoleta()
    form.nome.data = pontocoleta.nome_pontocoleta
    form.endereco.data = pontocoleta.end_pontocoleta
    form.status.data = pontocoleta.status_pontocoleta
    return render_template('editarPontoColeta.html', titulo='Editar Ponto de Coleta', id=id, form=form,idpontocoleta=idpontocoleta)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarPontoColeta
#FUNÇÃO: alteraçõa no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarPontoColeta', methods=['POST',])
def atualizarPontoColeta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarPontoColeta')))      
    form = frm_editar_pontocoleta(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        idpontocoleta = request.form['idpontocoleta']
        pontocoleta = tb_pontoscoleta.query.filter_by(cod_pontocoleta=request.form['idpontocoleta']).first()
        pontocoleta.nome_pontocoleta = form.nome.data
        pontocoleta.end_pontocoleta = form.endereco.data
        pontocoleta.status_pontocoleta = form.status.data
        db.session.add(pontocoleta)
        db.session.commit()
        flash('Ponto de coleta atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarPontoColeta', id=request.form['id'],idpontocoleta=request.form['idpontocoleta']))  



##################################################################################################################################
#PONTO DE COLETA - RESIDUO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoColetaResiduo
#FUNÇÃO: formulario de cadastro
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoPontoColetaResiduo/<int:id>/<int:idpontocoleta>')
def novoPontoColetaResiduo(id,idpontocoleta):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoPontoColetaResiduo'))) 
    form = frm_editar_pontocoleta_residuo()
    return render_template('novoPontoColetaResiduo.html', titulo='Novo Resíduo', form=form, id=id, idpontocoleta=idpontocoleta)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarPontoColetaResiduo
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarPontoColetaResiduo/<int:idpontocoleta>', methods=['POST',])
def criarPontoColetaResiduo(idpontocoleta):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarPontoColetaResiduo')))     
    form = frm_editar_pontocoleta_residuo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarPontoColetaResiduo'))
    pontocoleta  = idpontocoleta
    residuo = form.residuo.data 
    acondicionamento = form.acondicionamento.data 
    periodicidade = form.periodicidade.data 
    tipoveiculo = form.tipoveiculo.data 
    status = form.status.data
    novoPontoColetaResiduo = tb_pontocoleta_residuo(cod_pontocoleta=pontocoleta, cod_periodicidade=periodicidade, cod_acondicionamento=acondicionamento, cod_tipoveiculo=tipoveiculo, cod_residuo=residuo, status_pontocoleta_residuo=status)
    flash('Periodicidade criada com sucesso!','success')
    db.session.add(novoPontoColetaResiduo)
    db.session.commit()
    return redirect(url_for('visualizarPontoColeta',idpontocoleta=idpontocoleta))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarPontoColetaResiduo
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarPontoColetaResiduo/<int:idpontocoletaresiduo>')
def visualizarPontoColetaResiduo(idpontocoletaresiduo):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarPontoColetaResiduo')))  
    pontocoletaresiduo = tb_pontocoleta_residuo.query.filter_by(cod_pontocoleta_residuo=idpontocoletaresiduo).first()
    idpontocoleta = pontocoletaresiduo.cod_pontocoleta
    form = frm_visualizar_pontocoleta_residuo()
    form.acondicionamento.data  = pontocoletaresiduo.cod_acondicionamento
    form.residuo.data  = pontocoletaresiduo.cod_residuo
    form.periodicidade.data  = pontocoletaresiduo.cod_periodicidade
    form.tipoveiculo.data  = pontocoletaresiduo.cod_tipoveiculo
    form.status.data = pontocoletaresiduo.status_pontocoleta_residuo
    return render_template('visualizarPontoColetaResiduo.html', titulo='Visualizar Resíduo', idpontocoletaresiduo=idpontocoletaresiduo,idpontocoleta=idpontocoleta, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarPontoColetaResiduo
##FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarPontoColetaResiduo/<int:idpontocoletaresiduo>')
def editarPontoColetaResiduo(idpontocoletaresiduo):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarPontoColetaResiduo')))  
    pontocoletaresiduo = tb_pontocoleta_residuo.query.filter_by(cod_pontocoleta_residuo=idpontocoletaresiduo).first()
    idpontocoleta = pontocoletaresiduo.cod_pontocoleta
    form = frm_editar_pontocoleta_residuo()
    form.acondicionamento.data  = pontocoletaresiduo.cod_acondicionamento
    form.residuo.data  = pontocoletaresiduo.cod_residuo
    form.periodicidade.data  = pontocoletaresiduo.cod_periodicidade
    form.tipoveiculo.data  = pontocoletaresiduo.cod_tipoveiculo
    form.status.data = pontocoletaresiduo.status_pontocoleta_residuo
    return render_template('editarPontoColetaResiduo.html', titulo='Editar Resíduo', idpontocoletaresiduo=idpontocoletaresiduo,idpontocoleta=idpontocoleta,form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarPontoColetaResiduo
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarPontoColetaResiduo', methods=['POST',])
def atualizarPontoColetaResiduo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarPontoColetaResiduo')))      
    form = frm_editar_pontocoleta_residuo(request.form)
    if form.validate_on_submit():
        idpontocoletaresiduo = request.form['idpontocoletaresiduo']
        idpontocoleta = request.form['idpontocoleta']
        pontocoletaresiduo = tb_pontocoleta_residuo.query.filter_by(cod_pontocoleta_residuo=idpontocoletaresiduo).first()
        pontocoletaresiduo.cod_residuo = form.residuo.data
        pontocoletaresiduo.cod_acondicionamento = form.acondicionamento.data
        pontocoletaresiduo.cod_tipoveiculo = form.tipoveiculo.data
        pontocoletaresiduo.status_periodicidade = form.status.data
        db.session.add(pontocoletaresiduo)
        db.session.commit()
        flash('Resíduo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarPontoColetaResiduo', idpontocoleta=idpontocoleta,idpontocoletaresiduo=idpontocoletaresiduo)) 