from flask import Flask, request, render_template
import pandas as pd
import os
app = Flask(__name__)

@app.route('/')
def iniciar():
    return render_template('index.html')

@app.route("/provas")
def provas():
    pdf = os.listdir('static/pdfs')
    return render_template("provas.html" , pdf=pdf)

@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    valor = request.form['materia']
    pesquisa = request.form['query']
    ano = request.form['ano']
    
    df = pd.read_csv('baseQuestoes.csv')
    filtros = []

    if valor != '':
        filtros.append((df['principal'].str.contains(valor)) | (df['secundarias'].str.contains(valor)))
    if pesquisa != '':
        filtros.append(df['texto'].str.contains(pesquisa))
    if ano != '':
        filtros.append(df['ano'].astype(str) == ano)  

    # Aplica os filtros combinados
    if filtros:
        from functools import reduce
        import operator
        filtro_completo = reduce(operator.and_, filtros)
        resultado = df[filtro_completo]
    else:
        return render_template('index.html')

    indices = resultado['numero_questao'].tolist()
    imagens = []

    for index, row in resultado.iterrows():
        pagina_int = int(row['pagina'])
        caminho = f"/static/imagemPaginas/{row['semestre']}ano{row['ano']}/pagina_{pagina_int}.png"
        print(caminho)
        imagens.append(caminho)

    return render_template('resultado.html', imagens=imagens, resultado=resultado, indices=indices)


if __name__ == '__main__':
    app.run(debug=True)