from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

codificador = tiktoken.encoding_for_model(modelo)

prompt_sistema = """
Identifique o perfil de resposta do Cliente
"""

prompt_usuario = input("Teste de controle de model")

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens}")
tamanho_esperado_saida = 2048

if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = "gpt-4-1106-preview"

print(f"Modelo escolhido: {modelo}")

lista_mensagens = [
    {
        "role": "system",
        "content": prompt_sistema
    },
    {
        "role": "user",
        "content": prompt_usuario
    }
]

resposta = client.chat.completions.create(
    messages=lista_mensagens,
    model=modelo
)

print(resposta.choices[0].message.content)
