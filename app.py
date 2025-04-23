from flask import Flask, request, render_template
import pandas as pd
app = Flask(__name__)

@app.route('/')
def iniciar():
    return render_template('index.html')

@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    valor = request.form['materia']
    pesquisa = request.form['query']
    if valor != '' and pesquisa == '':
        imagens = []
        
        df = pd.read_csv('baseQuestoes.csv')
        
        resultado = df[df['principal'].str.contains(valor)]
        indices = resultado['numero_questao'].tolist() 
        for index, row in resultado.iterrows():
            pagina_int = int(row['pagina'])
            caminho = f"/static/imagemPaginas/{row['semestre']}ano{row['ano']}/pagina_{pagina_int}.png"
            print(caminho)
            imagens.append(caminho)
        
        # Renderizar o template com os resultados
        return render_template('resultado.html', imagens=imagens, resultado=resultado , indices=indices)
    
    elif valor == '' and pesquisa != '':
         
        imagens = []
        
        df = pd.read_csv('baseQuestoes.csv')
        
        resultado = df[df['texto'].str.contains(pesquisa)]
        indices = resultado['numero_questao'].tolist() 
        for index, row in resultado.iterrows():
            pagina_int = int(row['pagina'])
            caminho = f"/static/imagemPaginas/{row['semestre']}ano{row['ano']}/pagina_{pagina_int}.png"
            print(caminho)
            imagens.append(caminho)
        
        # Renderizar o template com os resultados
        return render_template('resultado.html', imagens=imagens, resultado=resultado , indices=indices)
    
    elif valor != '' and pesquisa != '':
        
        imagens = []
        
        df = pd.read_csv('baseQuestoes.csv')
        
        resultado = df[(df['principal'].str.contains(valor)) & (df['texto'].str.contains(pesquisa))]
        indices = resultado['numero_questao'].tolist() 
        for index, row in resultado.iterrows():
            pagina_int = int(row['pagina'])
            caminho = f"/static/imagemPaginas/{row['semestre']}ano{row['ano']}/pagina_{pagina_int}.png"
            print(caminho)
            imagens.append(caminho)
        
        # Renderizar o template com os resultados
        return render_template('resultado.html', imagens=imagens, resultado=resultado , indices=indices)
    
    elif valor == '' and pesquisa == '':
        return render_template('index.html')
    
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)