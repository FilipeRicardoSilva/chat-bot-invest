from openai import OpenAI
from dotenv import load_dotenv
import os
from helpers import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

politicas_bi = carrega('dados/políticas_bi.txt')
dados_bi = carrega('dados/dados_bI.txt')
produtos_bi = carrega('dados/produtos_bi.txt')

def selecionar_documento(resposta_openai):
    if "políticas" in resposta_openai:
        return dados_bi + "\n" + politicas_bi
    elif "produtos" in resposta_openai:
        return dados_bi + "\n" + produtos_bi
    else:
        return dados_bi 

def selecionar_contexto(mensagem_usuario):
    prompt_sistema = f"""
    A empresa bi possui três documentos principais que detalham diferentes aspectos do negócio:

    #Documento 1 "\n {dados_bi} "\n"
    #Documento 2 "\n" {politicas_bi} "\n"
    #Documento 3 "\n" {produtos_bi} "\n"

    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne dados se for o Documento 1, políticas se for o Documento 2 e produtos se for o Documento 3. 

    """

    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content" : mensagem_usuario
            }
        ],
        temperature=1,
    )

    contexto = resposta.choices[0].message.content.lower()

    return contexto