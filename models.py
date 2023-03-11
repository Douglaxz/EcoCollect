from ecocollect import db

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: USUÁRIOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_user(db.Model):
    cod_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    password_user = db.Column(db.String(50), nullable=False)
    status_user = db.Column(db.Integer, nullable=False)
    login_user = db.Column(db.String(50), nullable=False)
    cod_usertype = db.Column(db.Integer, nullable=False)
    email_user = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TIPO USUÁRIOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_usertype(db.Model):
    cod_usertype = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_usertype = db.Column(db.String(50), nullable=False)
    status_usertype = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    
 
#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: RESÍDUOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_residuos(db.Model):
    cod_residuo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_residuo = db.Column(db.String(50), nullable=False)
    status_residuo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: DESTINADORES
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_destinadores(db.Model):
    cod_destinador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_destinador = db.Column(db.String(50), nullable=False)
    end_destinador = db.Column(db.String(90), nullable=False)
    status_destinador = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TIPO VEÍCULO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_tiposveiculo(db.Model):
    cod_tipoveiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipoveiculo = db.Column(db.String(50), nullable=False)
    status_tipoveiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: VEÍCULO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_veiculos(db.Model):
    cod_veiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa_veiculo = db.Column(db.String(50), nullable=False)
    status_veiculo = db.Column(db.Integer, nullable=False)
    cod_tipoveiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: MOTORISTA
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_motoristas(db.Model):
    cod_motorista = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_motorista = db.Column(db.String(50), nullable=False)
    status_motorista = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: CLIENTES
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_clientes(db.Model):
    cod_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(50), nullable=False)
    end_cliente = db.Column(db.String(90), nullable=False)
    status_cliente = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: PONTOS DE COLETA
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_pontoscoleta(db.Model):
    cod_pontocoleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_cliente = db.Column(db.Integer, nullable=False)
    nome_pontocoleta = db.Column(db.String(50), nullable=False)
    end_pontocoleta = db.Column(db.String(90), nullable=False)
    status_pontocoleta = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
    
#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: ACONDICIONAMENTO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_acondicionamento(db.Model):
    cod_acondicionamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_acondicionamento = db.Column(db.String(50), nullable=False)
    status_acondicionamento = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: PERIODICIDADE
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_periodicidade(db.Model):
    cod_periodicidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_periodicidade = db.Column(db.String(50), nullable=False)
    status_periodicidade = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: PONTOS DE COLETA RESIDUO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_pontocoleta_residuo(db.Model):
    cod_pontocoleta_residuo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_pontocoleta = db.Column(db.Integer, nullable=False)
    cod_residuo = db.Column(db.Integer, nullable=False)
    cod_acondicionamento = db.Column(db.Integer, nullable=False)
    cod_periodicidade = db.Column(db.Integer, nullable=False)
    cod_tipoveiculo = db.Column(db.Integer, nullable=False)
    status_pontocoleta_residuo = db.Column(db.Integer, nullable=False)
    colDom_pontocoleta_residuo = db.Column(db.Integer, nullable=False)
    colSeg_pontocoleta_residuo = db.Column(db.Integer, nullable=False) 
    colTer_pontocoleta_residuo = db.Column(db.Integer, nullable=False) 
    colQua_pontocoleta_residuo = db.Column(db.Integer, nullable=False) 
    colQui_pontocoleta_residuo = db.Column(db.Integer, nullable=False) 
    colSex_pontocoleta_residuo = db.Column(db.Integer, nullable=False)
    colSab_pontocoleta_residuo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
    
#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: ROTAS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_rotas(db.Model):
    cod_rota = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_rota = db.Column(db.String(50), nullable=False)
    status_rota = db.Column(db.Integer, nullable=False)
    cod_veiculo = db.Column(db.Integer, nullable=False)
    cod_motorista = db.Column(db.Integer, nullable=False)
    diasemana_rota = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: PONTO DE COLETA ROTAS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_rotas_pontocoletaresiduos(db.Model):
    cod_rotas_pontocoletaresiduos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_rotas_pontocoletaresiduos = db.Column(db.Integer, nullable=False)
    ordem_rotas_pontocoletaresiduos = db.Column(db.Integer, nullable=False)
    cod_pontocoleta_residuo = db.Column(db.Integer, nullable=False)
    cod_rota = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
