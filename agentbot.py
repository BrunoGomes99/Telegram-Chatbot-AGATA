# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 16:17:56 2020

@author: Bruno


Este Script é reponsável por detectar a intenção do usuário no DialogFlow e retornar a possível resposta

"""

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "aga-uema-sxla-e5cb501e29a5.json" # Nome do arquivo da chave de autenticação que dentro da pasta com este arquivo .py

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "aga-uema-sxla" # Pegamos nas configurações desse Agent lá no dialogFlow


def detect_intent_from_text(text, session_id, language_code='pt-br'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(query, session_Id):
    response = detect_intent_from_text(query, session_Id)
    return response.fulfillment_messages
    
# response.fulfillment_text (A primeira resposta que o bot vai mandar - no formato de string já)

# response.intent.display_name (Nome do intent utilizado. Lembrando que intent é o nome dos arquivos de treino lá no dialog flow)

# response.intent_detection_confidence (A precisão da detecção do intent de 0.1 a 1 (0 a 100%))