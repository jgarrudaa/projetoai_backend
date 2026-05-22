import os
import json
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import CONTRATO_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def apenas_numeros(valor):
    """Remove qualquer caractere que não seja número da string"""
    if not valor:
        return ""
    return re.sub(r'\D', '', str(valor))

def generate_contract(dados_contrato):
    # O prompt envia os documentos limpos e a IA se encarrega de formatá-los no texto jurídico
    conteudo_prompt = f"""
    Gere um contrato comercial com as seguintes especificações:
    - Tipo de Contrato: {dados_contrato.get('tipo_contrato')}
    
    - Contratante (Nome/Razão Social): {dados_contrato.get('contratante_nome')}
    - Contratante (Apenas números do CPF/CNPJ): {dados_contrato.get('contratante_documento')}
    
    - Contratado (Nome/Razão Social): {dados_contrato.get('contratado_nome')}
    - Contratado (Apenas números do CPF/CNPJ): {dados_contrato.get('contratado_documento')}
    
    - Objeto do Contrato: {dados_contrato.get('objeto')}
    - Valores e Condições de Pagamento: {dados_contrato.get('pagamento')}
    - Cláusulas Opcionais: {dados_contrato.get('clausulas_extras', 'Nenhuma informada.')}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json", 
            response_schema=CONTRATO_SCHEMA,       
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                ),
            ]
        )
    )
    return response.text

@app.route("/")
def root():
    return jsonify({"status": "success", "message": "API Gerador de Contratos Inteligentes funcionando!"}), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados não fornecidos."}), 400
        
    # 1. Validação de campos obrigatórios
    campos_obrigatorios = [
        "tipo_contrato", "contratante_nome", "contratante_documento", 
        "contratado_nome", "contratado_documento", "objeto", "pagamento"
    ]
    campos_ausentes = [campo for campo in campos_obrigatorios if not data.get(campo)]
    
    if campos_ausentes:
        return jsonify({
            "status": "error",
            "message": f"Os seguintes campos são obrigatórios: {', '.join(campos_ausentes)}"
        }), 400

    # 2. Limpeza dos documentos (garante que vai apenas números para a IA)
    data["contratante_documento"] = apenas_numeros(data.get("contratante_documento"))
    data["contratado_documento"] = apenas_numeros(data.get("contratado_documento"))

    # 3. Validação básica de tamanho (CPF deve ter 11 dígitos e CNPJ 14)
    if len(data["contratante_documento"]) not in [11, 14]:
        return jsonify({"status": "error", "message": "O documento do contratante deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)."}), 400
        
    if len(data["contratado_documento"]) not in [11, 14]:
        return jsonify({"status": "error", "message": "O documento do contratado deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)."}), 400

    try:
        contrato_json_string = generate_contract(data)
        contrato_estruturado = json.loads(contrato_json_string)
        
        return jsonify({
            "status": "success",
            "dados_contrato": contrato_estruturado
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao gerar o documento: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)