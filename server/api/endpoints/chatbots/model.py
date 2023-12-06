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
    """
    Gets the last [count] messages in the conversation history or the whole, if no count is given.

    Args:
      userId (str): The user's ID.
      subjectId (str): The subject's ID.
      chatbot (str): The chatbot type.
      count (int, optional): The number of messages to return. Defaults to None.

    Returns:
      list: A list of conversation history messages.

    Examples:
      >>> getConversationHistory("user1", "subject1", "general", 5)
      [[q1, a1], [q2, a2], [q3, a3], [q4, a4], [q5, a5]]
    """
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
    """
    Prompts the chatbot with a given prompt.

    Args:
      userId (str): The user's ID.
      subjectId (str): The subject's ID.
      chatbot (str): The chatbot type.
      prompt (str, optional): The prompt to give the chatbot. Defaults to "Erzähl mir etwas über das Subject".

    Returns:
      str: The chatbot's response.

    Examples:
      >>> promptChatbot("user1", "subject1", "general", "What is the capital of Germany?")
      "Berlin"
    """
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
    """
    Assembles a list of questions and answers.

    Args:
      questions (list): A list of questions.
      answers (list): A list of answers.

    Returns:
      list: A list of questions and answers.

    Examples:
      >>> assembleList(["What is the capital of Germany?", "What is the capital of France?"], ["Berlin", "Paris"])
      [[q1, a1], [q2, a2]]
    """
    return list(zip_longest(questions, answers, fillvalue=""))

