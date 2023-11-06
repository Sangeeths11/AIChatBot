import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config
from chatbots.documentQuestionAnswering import documentQA, getConversationHistoryGeneral, getConversationHistoryResources


db = firestore.client()


# gets the last [count] messages in the conversation history or the whole, if no count is given
def getConversationHistory(userId, subjectId, chatbot, count = None):
    hist = []
    if chatbot is None: chatbot = "general"
    
    if chatbot == "resources":
        hist = getConversationHistoryResources(userId, subjectId)
    elif chatbot == "general":
        hist = getConversationHistoryGeneral(userId, subjectId)

    if not count or count == "":
        return hist
    
    if len(hist) < count:
        count = len(hist)
        
    # return last x elements from the end of the list
    return hist[-count:]





def promptChatbot(userId, subjectId, chatbot, prompt = "Erzähl mir etwas über das Subject"):
    hist = []
    if chatbot is None: chatbot = "general"
    
    if chatbot == "resources":
        hist = documentQA(userId, subjectId, prompt)
    elif chatbot == "general":
        pass
        #chatbot general prompting 
