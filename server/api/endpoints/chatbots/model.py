import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config
from chatbots.documentQuestionAnswering import documentQA, getConversationHistoryResources
from chatbots.generalQuestionAnswering import get_chatbot_response, getConversationHistoryGeneral
from itertools import zip_longest

db = firestore.client()


# gets the last [count] messages in the conversation history or the whole, if no count is given
def getConversationHistory(userId, subjectId, chatbot, count=None):
    hist = []
    if chatbot is None: chatbot = "general"

    if chatbot == "resources":
        questions, answers = getConversationHistoryResources(userId, subjectId)
    elif chatbot == "general":
        questions, answers = getConversationHistoryGeneral(userId, subjectId)

    hist = assembleList(questions, answers)
    if not count or count == "":
        return hist

    if len(hist) < int(count):
        count = len(hist)

    # return last x elements from the end of the list
    return hist[-count:]


def promptChatbot(userId, subjectId, chatbot, prompt="Erzähl mir etwas über das Subject"):
    hist = []
    if chatbot is None: chatbot = "general"

    if chatbot == "resources":
        return documentQA(userId, subjectId, prompt)
    elif chatbot == "general":
        return get_chatbot_response(userId, subjectId, prompt)
    else:
        return None


# Return in form [[q, a],[q, a],[q, ""]]
def assembleList(questions, answers):
    return list(zip_longest(questions, answers, fillvalue=""))

