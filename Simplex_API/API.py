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

    M, sim, H = solver.inicializarProblema(func_obj, restricciones, igualdades, tipos_restriccion)

    M_h, resultados=solver.solve(M,sim,H)

    print("M_r: ", M_h)
    print("resutlados: ",resultados)

    return jsonify({
                    'matrices': M_h,
                    'resultados': resultados,
                    'cabecera': sim ,
                    'lateral': H
                    })


if __name__ == '__main__':
    app.run(debug=True)


