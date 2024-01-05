#### Bibliotecas ####
from flask import Flask, request
from datetime import datetime
import joblib
import sqlite3

#### Instanciar o aplicativo ####
aplicativo = Flask(__name__)

#### Carregando o modelo ####
modelo = joblib.load('Modelo_Floresta_Aleatorio_v100.pkl')

#### Função para receber nossa API ####
@aplicativo.route('/API_PREDITIVO/<area>;<rooms>;<bathrooms>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao(area, rooms, bathrooms, parking_spaces, floor, animal, furniture, hoa, property_tax):
    
    data_inicio = datetime.now()
    
    #### Recebendo os parâmetros ####
    lista_parametros = [area, rooms, bathrooms, parking_spaces, floor, animal, furniture, hoa, property_tax]
    #### Garantindo a integridade dos dados ####
    lista_parametros = [float(i) for i in lista_parametros]

    try:
        #### Previsão do modelo ####
        previsao = modelo.predict([lista_parametros])
        input=''
        for i in lista_parametros:
            input=input+';'+str(i)
        input = input[1:]
        
        data_fim = datetime.now()
        tempo_processamento = data_fim - data_inicio

        #### Conexão com o banco de dados ####
        conexao_banco = sqlite3.connect('banco_dados_api.db')
        cursor = conexao_banco.cursor()

        #### Inserindo os parâmetros na base de dados
        query_insercao_dados = f'''
                                    INSERT INTO log_api (inputs_fornecidos, inicio_sessao, fim_sessao, processamento, valor_aluguel)
                                    VALUES ( '{input}', '{data_inicio}', '{data_fim}', '{tempo_processamento}','{previsao}')
                                '''
        cursor.execute(query_insercao_dados)
        conexao_banco.commit()
        cursor.close()

        return {'Valor do aluguel previsto:': str(previsao)}
    except Exception as inst:
        return {'Aviso:':inst}

if __name__ == '__main__':
    aplicativo.run(debug=True)
