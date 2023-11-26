from flask import Flask, request, jsonify
from flask_cors import CORS
from Simplex import MetodoSimplex


app = Flask(__name__)
CORS(app) 

@app.route('/simplex_api/', methods=['POST'])
def simplex_api():
    data = request.get_json()

    func_obj = data['zValues']
    restricciones = data['constraintValues']
    igualdades = data['lastInputValues']
    tipos_restriccion = data['selectValues']

    solver = MetodoSimplex()
    
    #print(func_obj, restricciones, igualdades, tipos_restriccion)

    solver.inicializarProblema(func_obj, restricciones, igualdades, tipos_restriccion)

    return jsonify("Done")


if __name__ == '__main__':
    app.run(debug=True)


