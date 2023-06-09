from gerencianet import Gerencianet

import credentials
import sys
import time
import json

from flask import Flask, jsonify
from flask import Flask, request
gn = Gerencianet(credentials.CREDENTIALS)

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#________________________Gera CobranÃ§a_____________________________#

@app.route('/')
def index():
    return "Documentação API" 

@app.route('/select') # SELECIONA O PRODUTO
def produto_s():
    produto_str = str(request.args['produto'])
    
    produtos = {
        'a': 1.0, #botao 1
        'b': 2.0, #botao 2
        'c': 3.0, #botao 3
        'd': 4.0,
        'e': 5.0,
        'f': 6.0,
        'g': 7.0,
        'h': 8.0
    }

    if produto_str in produtos:
        valor = produtos[produto_str]
        valor = '%.2f' % valor

        body = {
            'calendario': {'expiracao': 90},
            'devedor': {'cpf': '12345678909', 'nome': 'teste'},
            'valor': {'original': valor},
            'chave': '89cc274e-dcdf-46d0-9dd1-af1e78d1069f',
            'solicitacaoPagador': '89cc274e-dcdf-46d0-9dd1-af1e78d1069f'
        }

        response = gn.pix_create_immediate_charge(body=body)
        print(response)
        ids = str(response['loc']['id'])
        txid = str(response['txid'])
        params = {'id': ids}
        response = gn.pix_generate_QRCode(params=params)
        qr_code = response['qrcode']

        result = {"QRCODE": qr_code, "TXID": txid}
        return result
    else:
        return "Invalid product selection"

#________________________CheckOut____________________________#

@app.route('/check')
def check_out():
    try:
       txid =str(request.args['txid'])
       params = {'txid': txid}
       status=  gn.pix_detail_charge(params=params)
       status=str(status['status'])
       if status == "CONCLUIDA":
           db.child(machine).child("ESTADO").update({"BUTTON":"8"})
    except:
        status ="ATIVA"
    return (status)



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)