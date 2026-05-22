CONTRATO_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "titulo": {"type": "STRING", "description": "Título formal do contrato (ex: INSTRUMENTO PARTICULAR DE PRESTAÇÃO DE SERVIÇOS)"},
        "preambulo": {"type": "STRING", "description": "Qualificação detalhada das partes estruturada de forma jurídica, utilizando obrigatoriamente os nomes, documentos e informações de contratante e contratado passados no prompt."},
        "objeto": {"type": "STRING", "description": "Cláusula Primeira - Detalhamento minucioso do que será executado, escopo e prazos de entrega."},
        "valores_pagamento": {"type": "STRING", "description": "Cláusula Segunda - Valores, condições de pagamento, datas de vencimento e meio de pagamento acordado."},
        "clausulas_extras": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista de cláusulas adicionais importantes (multas por atraso, rescisão, propriedade intelectual, etc.) baseadas nos requisitos do usuário."
        },
        "foro": {"type": "STRING", "description": "Cláusula de eleição de foro para resolução de disputas legais."}
    },
    "required": ["titulo", "preambulo", "objeto", "valores_pagamento", "clausulas_extras", "foro"]
}

SYSTEM_INSTRUCTION = """
Você é um advogado especialista em Direito Contratual brasileiro.
Sua tarefa é redigir contratos juridicamente válidos com base nos dados fornecidos pelo usuário.

Ao montar o 'preambulo', você deve formatar os números de CPF/CNPJ enviados no padrão brasileiro (ex: 000.000.000-00 ou 00.000.000/0001-00) para compor a qualificação formal das partes.
Você DEVE preencher todos os campos do esquema fornecido estritamente em português.
"""