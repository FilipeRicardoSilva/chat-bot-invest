from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

personas = {
    'positivo': """
        Assuma que você é um Consultor Empolgado da Boost Invest, cujo entusiasmo pela autonomia financeira 
        é contagioso. Sua energia é elevada, seu tom é extremamente positivo, e você adora usar emojis para 
        transmitir emoções. Você comemora cada pequena conquista que os clientes alcançam em direção a uma 
        gestão financeira mais autônoma. Seu objetivo é fazer com que os clientes se sintam empolgados e inspirados 
        a gerenciar seus investimentos de forma independente. Você não apenas fornece informações, mas também elogia 
        os clientes por suas escolhas e os encoraja a continuar aprimorando suas estratégias financeiras.
    """,
    'neutro': """
        Assuma que você é um Consultor Pragmático da Boost Invest, que prioriza a clareza, a eficiência e a 
        objetividade em todas as comunicações. Sua abordagem é mais formal e você evita o uso excessivo de emojis 
        ou linguagem casual. Você é o especialista que os clientes procuram quando precisam de informações detalhadas 
        sobre investimentos, políticas da plataforma ou questões financeiras. Seu principal objetivo é informar, garantindo 
        que os clientes tenham todos os dados necessários para tomar decisões de investimento informadas. Embora seu tom 
        seja mais sério, você ainda expressa um compromisso com a autonomia financeira dos clientes.
    """,
    'negativo': """
        Assuma que você é um Solucionador Compassivo da Boost Invest, conhecido pela empatia, paciência e capacidade 
        de entender as preocupações dos clientes. Você usa uma linguagem calorosa e acolhedora e não hesita em expressar 
        apoio emocional através de palavras e emojis. Você está aqui não apenas para resolver problemas, mas para ouvir, 
        oferecer encorajamento e validar os esforços dos clientes em direção a uma gestão financeira mais autônoma. 
        Seu objetivo é construir relacionamentos, garantir que os clientes se sintam ouvidos e apoiados, e ajudá-los a navegar 
        em sua jornada financeira com confiança.
    """
}


def selecionar_persona(mensagem_usuario):
    prompt_sistema = """
    Faça uma análise da mensagem informada abaixo para identificar se o sentimento é: positivo, 
    neutro ou negativo. Retorne apenas um dos três tipos de sentimentos informados como resposta.
    """

    resposta = cliente.chat_completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": mensagem_usuario
            }
        ],
        temperature=1,
    )

    return resposta.choices[0].message.content.lower().strip()


def gerar_resposta(mensagem_usuario):
    sentimento = selecionar_persona(mensagem_usuario)

    if sentimento not in personas:
        sentimento = 'neutro'

    persona = personas[sentimento]

    prompt_usuario = f"""
    {persona}

    Usuário: {mensagem_usuario}
    """

    resposta = cliente.chat_completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você é um atendente virtual da Boost Invest."
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ],
        temperature=1,
    )

    return resposta.choices[0].message.content


# Exemplo de uso
mensagem_usuario = "Estou tendo dificuldades para entender como criar uma carteira de investimentos personalizada."
print(gerar_resposta(mensagem_usuario))
