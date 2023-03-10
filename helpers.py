#importações
import os
from ecocollect import app, db
from models import tb_user, tb_usertype, tb_residuos, tb_tiposveiculo, tb_veiculos, tb_motoristas,tb_clientes, tb_periodicidade, tb_acondicionamento
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SubmitField,IntegerField, SelectField,PasswordField,DateField,EmailField,BooleanField,RadioField, TextAreaField, TimeField, TelField, DateTimeLocalField,FloatField, DecimalField 

##################################################################################################################################
#PESQUISA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pesquisa (geral)
#TIPO: edição
#TABELA: nenhuma
#---------------------------------------------------------------------------------------------------------------------------------
class frm_pesquisa(FlaskForm):
    pesquisa = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    pesquisa_responsiva = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    salvar = SubmitField('Pesquisar')

##################################################################################################################################
#USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_usuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o nome do usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")])
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o login do usuário"})    
    tipousuario = SelectField('Situação:', coerce=int,  choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')])
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o email do usuário"})
    salvar = SubmitField('Salvar')


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: visualização
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_usuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")], render_kw={'readonly': True})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    tipousuario = SelectField('Tipo:', coerce=int, choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')], render_kw={'readonly': True})
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    salvar = SubmitField('Editar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: trocar senha do usuário
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_senha(FlaskForm):
    senhaatual = PasswordField('Senha Atual:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a senha atual"})
    novasenha1 = PasswordField('Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a nova senha"})
    novasenha2 = PasswordField('Confirme Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite novamente a senha"})
    salvar = SubmitField('Editar')  

##################################################################################################################################
#TIPO DE USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: edição
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_tipousuario(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: visualização
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_tipousuario(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#RESIDUOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: residuos
#TIPO: edição
#TABELA: tb_residuos
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_residuo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do resíduo"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: residuos
#TIPO: visualização
#TABELA: tb_residuos
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_residuo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#DESTINADORES
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: destinadores
#TIPO: edição
#TABELA: tb_destinadores
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_destinador(FlaskForm):
    descricao = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do destinador"})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={"placeholder": "digite o endereço do destinador"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: destinadores
#TIPO: visualização
#TABELA: tb_destinadores
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_destinador(FlaskForm):
    descricao = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#TIPO VEÍCULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipoveiculos
#TIPO: edição
#TABELA: tb_tipoveiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_tipoveiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o tipo de veículo"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipoveiculos
#TIPO: visualização
#TABELA: tb_tipoveiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_tipoveiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar') 

##################################################################################################################################
#VEÍCULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: veiculos
#TIPO: edição
#TABELA: tb_veiculos
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_veiculo(FlaskForm):
    placa = StringField('Placa:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o tipo de veículo"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    tipoveiculo = SelectField('Tipo:', coerce=int, choices=[(g.cod_tipoveiculo, g.desc_tipoveiculo) for g in tb_tiposveiculo.query.order_by('desc_tipoveiculo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: veiculos
#TIPO: visualização
#TABELA: tb_veiculos
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_veiculo(FlaskForm):
    placa = StringField('Placa:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    tipoveiculo = SelectField('Tipo:', coerce=int, choices=[(g.cod_tipoveiculo, g.desc_tipoveiculo) for g in tb_tiposveiculo.query.order_by('desc_tipoveiculo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar') 

##################################################################################################################################
#MOTORISTAS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: motoristas
#TIPO: edição
#TABELA: tb_motorista
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_motorista(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do motorista"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: motoristas
#TIPO: visualização
#TABELA: tb_motorista
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_motorista(FlaskForm):
    nome = StringField('Placa:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')

##################################################################################################################################
#CLIENTES
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: clientes
#TIPO: edição
#TABELA: tb_clientes
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_cliente(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do cliente"})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={"placeholder": "digite o endereço do cliente"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: clientes
#TIPO: visualização
#TABELA: tb_clientes
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_cliente(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')

##################################################################################################################################
#PONTOS DE COLETA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pontos coleta
#TIPO: edição
#TABELA: tb_pontoscoleta
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_pontocoleta(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do ponto de coleta"})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={"placeholder": "digite o endereço do ponto de coleta"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pontos coleta
#TIPO: visualização
#TABELA: tb_pontoscoleta
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_pontocoleta(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')

##################################################################################################################################
#ACONDICIONAMENTO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: acondicionamento
#TIPO: edição
#TABELA: tb_acondicionamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_acondicionamento(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do acondicionamento"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: acondicionamento
#TIPO: visualização
#TABELA: tb_acondicionamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_acondicionamento(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')

##################################################################################################################################
#PERIODICIDADE
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: periodicidade
#TIPO: edição
#TABELA: tb_periodicidade
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_periodicidade(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome da periodicidade"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: periodicidade
#TIPO: visualização
#TABELA: tb_periodicidade
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_periodicidade(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')

##################################################################################################################################
#PONTO COLETA / RESIDUO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pontocoleta_residuo
#TIPO: edição
#TABELA: tb_periodicidade
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_pontocoleta_residuo(FlaskForm):
    residuo = SelectField('Resíduo:', coerce=int, choices=[(g.cod_residuo, g.desc_residuo) for g in tb_residuos.query.order_by('desc_residuo')])
    acondicionamento = SelectField('Acondicionamento:', coerce=int, choices=[(g.cod_acondicionamento, g.desc_acondicionamento) for g in tb_acondicionamento.query.order_by('desc_acondicionamento')])
    periodicidade = SelectField('Periodicidade:', coerce=int, choices=[(g.cod_periodicidade, g.desc_periodicidade) for g in tb_periodicidade.query.order_by('desc_periodicidade')])
    tipoveiculo = SelectField('Veículo:', coerce=int, choices=[(g.cod_tipoveiculo, g.desc_tipoveiculo) for g in tb_tiposveiculo.query.order_by('desc_tipoveiculo')])
    diadom = BooleanField('Domingo:')
    diaseg = BooleanField('Segunda:')
    diater = BooleanField('Terça:')
    diaqua = BooleanField('Quarta:')
    diaqui = BooleanField('Quinta:')
    diasex = BooleanField('Sexta:')
    diasab = BooleanField('Sábado:')
    salvar = SubmitField('Salvar')
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pontocoleta_residuo
#TIPO: visualização
#TABELA: tb_periodicidade
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_pontocoleta_residuo(FlaskForm):
    residuo = SelectField('Resíduo:', coerce=int, choices=[(g.cod_residuo, g.desc_residuo) for g in tb_residuos.query.order_by('desc_residuo')])
    acondicionamento = SelectField('Acondicionamento:', coerce=int, choices=[(g.cod_acondicionamento, g.desc_acondicionamento) for g in tb_acondicionamento.query.order_by('desc_acondicionamento')])
    periodicidade = SelectField('Periodicidade:', coerce=int, choices=[(g.cod_periodicidade, g.desc_periodicidade) for g in tb_periodicidade.query.order_by('desc_periodicidade')])
    tipoveiculo = SelectField('Veículo:', coerce=int, choices=[(g.cod_tipoveiculo, g.desc_tipoveiculo) for g in tb_tiposveiculo.query.order_by('desc_tipoveiculo')])
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    diadom = BooleanField('Domingo:', render_kw={'readonly': True})
    diaseg = BooleanField('Segunda:', render_kw={'readonly': True})
    diater = BooleanField('Terça:', render_kw={'readonly': True})
    diaqua = BooleanField('Quarta:', render_kw={'readonly': True})
    diaqui = BooleanField('Quinta:', render_kw={'readonly': True})
    diasex = BooleanField('Sexta:', render_kw={'readonly': True})
    diasab = BooleanField('Sábado:', render_kw={'readonly': True})    
    salvar = SubmitField('Editar', render_kw={'readonly': True})
    salvar = SubmitField('Salvar') 

##################################################################################################################################
#ROTAS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: rotas
#TIPO: edição
#TABELA: tb_rotas
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_rota(FlaskForm):
    descricao = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome da rota"})
    diadasemana = SelectField('Situação:', coerce=int, choices=[(0, 'DOM'),(1, 'SEG'),(2, 'TER'),(3, 'QUA'),(4, 'QUI'),(5, 'SEX'),(7, 'SAB')])
    veiculo = SelectField('Veículo:', coerce=int, choices=[(g.cod_veiculo, g.placa_veiculo) for g in tb_veiculos.query.order_by('placa_veiculo')])
    motorista = SelectField('Motorista:', coerce=int, choices=[(g.cod_motorista, g.nome_motorista) for g in tb_motoristas.query.order_by('nome_motorista')])
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: rotas
#TIPO: visualização
#TABELA: tb_rotas
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_rota(FlaskForm):
    descricao = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    diadasemana = SelectField('Situação:', coerce=int, choices=[(0, 'DOM'),(1, 'SEG'),(2, 'TER'),(3, 'QUA'),(4, 'QUI'),(5, 'SEX'),(7, 'SAB')], render_kw={'readonly': True})
    veiculo = SelectField('Veículo:', coerce=int, choices=[(g.cod_veiculo, g.placa_veiculo) for g in tb_veiculos.query.order_by('placa_veiculo')], render_kw={'readonly': True})
    motorista = SelectField('Motorista:', coerce=int, choices=[(g.cod_motorista, g.nome_motorista) for g in tb_motoristas.query.order_by('nome_motorista')], render_kw={'readonly': True})    
    salvar = SubmitField('Salvar')

##################################################################################################################################
#ROTAS / PONTO COLETA RESÍDUOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: rotas / ponto coleta residuos
#TIPO: edição
#TABELA: tb_rotas
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_rotas_pontocoletaresiduos(FlaskForm):
    ordem = IntegerField('Ordem de execução:', [validators.DataRequired()], render_kw={"placeholder": "digite a ordem de execução deste ponto"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    pontocoleta_residuo = SelectField('Ponto de Coleta | Resíduo:', coerce=int, choices=[])



#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: rotas / ponto coleta residuos
#TIPO: visualização
#TABELA: tb_rotas
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_rotas_pontocoletaresiduos(FlaskForm):
    ordem = IntegerField('Ordem de execução:', [validators.DataRequired()], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    pontocoleta_residuo = SelectField('Ponto de Coleta | Resíduo:', coerce=int, choices=[], render_kw={'readonly': True})
