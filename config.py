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
Você é um advogado especialista em Direito Contratual brasileiro, focado no ecossistema digital, startups e prestadores de serviço.
Sua tarefa é redigir contratos juridicamente válidos com base nos dados fornecidos pelo usuário.

Diretrizes específicas por Tipo de Contrato:
- Para "Tráfego Pago": Deixe claro que o Contratante paga os anúncios e o Contratado gerencia; retire garantias de vendas.
- Para "Influenciador/Conteúdo": Foque em prazos de veiculação das postagens e direito de imagem.
- Para "Cessão de Direitos": Especifique se o cliente vira dono do arquivo final/matriz ou se é apenas uma licença de uso.
- Para "Software": Regule quem fica com o código-fonte e o escopo de manutenção pós-entrega.
- Para "Consultoria": Foque no formato das reuniões/horas e confidencialidade de dados internos.

Ao montar o 'preambulo', formate os números de CPF/CNPJ enviados no padrão brasileiro. 
Você DEVE preencher todos os campos do esquema fornecido estritamente em português.
Ao redigir a propriedade 'valores_pagamento', junte as informações de Valor Total, Meio de Pagamento e Condições de Prazo enviadas em uma redação jurídica fluida, clara, que estipule as obrigações financeiras e eventuais penalidades por inadimplência básica de forma profissional.
"""
