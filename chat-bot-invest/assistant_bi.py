from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selection_persona import *
import json
from tools_bi import *


load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"
contexto = carrega("dados/bi.txt")

def criar_lista_ids():
    lista_ids_arquivos = []

    file_dados = cliente.files.create(
        file=open("dados/dados_bI.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_dados.id)

    file_politicas = cliente.files.create(
        file=open("dados/políticas_bi.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_politicas.id)

    file_produtos = cliente.files.create(
        file=open("dados/produtos_bi.txt", "rb"),
        purpose="assistants"
    )

    lista_ids_arquivos.append(file_produtos.id)

    return lista_ids_arquivos

def pegar_json():
    filename = "assistant.json"
    
    if not os.path.exists(filename):
        thread_id = criar_thread()
        file_id_list = criar_lista_ids()
        assistant_id = criar_assistente(file_id_list)
        data = {
            "assistant_id": assistant_id.id,
            "thread_id": thread_id.id,
            "file_ids": file_id_list
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Arquivo 'assistant.json' criado com sucesso.")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Arquivo 'assistant.json' não encontrado.")


def criar_thread():
    return cliente.beta.threads.create()

def criar_assistente(file_ids=[]):
    assistente = cliente.beta.assistants.create(
        name="Atendente BI_Finance",
        instructions = f"""
                Você é um chatbot de atendimento a clientes de uma plataforma de investimento. 
                Você não deve responder perguntas que não sejam dados da plataforma informado!
                Além disso, acesse os arquivos associados a você e a thread para responder as perguntas.
                """,
        model = modelo,
        tools= minhas_tools,
        file_ids = file_ids
    )
    return assistente

