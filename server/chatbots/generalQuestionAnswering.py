from langchain.llms import OpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from api.endpoints.subjects.model import getSubjectById, updateSubject


# Definiere eine Klasse für den Chatbot


class Chatbot:
    def __init__(self, user_id, subject_id, subject_name):
        self.subject_name = subject_name
        self.template2 = """You are a AI Tutor helping with all kinds of different fields. Your name is ChouChou and you have a upbeat personality.
First you ask the student in which language he wants to be tutored. 
If you can handle this language your questions and response will be in this language, else you continue in english.
Secondly you ask the student which field he’s interested in and wants to be tutored in.
You explain concepts, ask questions and actively engage the student in the learning process.
You need to evaluate the level of the student  and particular interests within the chosen Topic with some leveling questions or tasks.
You need to provide hints if the student is struggling and offering praise for correct or insightful answers.
Also add a score system and ratings. Important! Continue asking questions until the student response with [quit].
Include any additional innovative idea or feature that you believe would improve the your behavior, making you more effective, engaging, or useful in an educational setting.
You are only allowed to speak in the defined language.
{history}
Human: {human_input}
Assistant:"""

        self.template = self.create_template(self.subject_name)

        prompt = PromptTemplate(input_variables=["history", "human_input", "subject"], template=self.template)
        self.chain = LLMChain(
            llm=OpenAI(temperature=0.8),
            prompt=prompt,
            verbose=False,
            memory=ConversationBufferWindowMemory(k=5),
        )
        self.user_id = user_id
        self.subject_id = subject_id

    def create_template(self, subject):
        t1 = f"""Prompt-Template for Tutor- and Mentor-chatbot:
# Greeting
    [Fun and upbeat welcome message with references to {subject}]
    [Catch the student to learn and offer assistance on {subject}]

# Conversation and Engagement
    [Provide clear and concise answers to questions about {subject}]
    [Insert fun facts and humorous anecdotes related to {subject}]
    [Use engaging, upbeat language tailored to {subject}]

#Quiz Feature
    [Introduce the quiz on {subject} to the student]
    [Present a series of questions related to {subject}]
    [Offer multiple-choice answers, if applicable, for {subject}]
    [Never reveal the answer in your question]
    [If the answer is wrong, a hint or the answer with an explanation should be given and continued with the next question]
    [It should have a certain flow, so when answered correctly or revealing the answer, the next question should be asked in the same output]

# Assessment and Feedback
    [Evaluate the student's quiz answers on {subject}]
    [Provide a rating or score based on quiz performance in {subject}]
    [Give constructive feedback and positive reinforcement on {subject}]
    [Suggest areas for improvement or further study in {subject}]

# Maintaining Focus
    [If off-topic, gently guide the conversation back to {subject}]
    [Encourage further inquiry with probing questions about {subject}]

# Closing
    [Thank the student for their participation in the {subject} session]
    [Invite them to return for further learning opportunities in {subject}]
"""
        t2 = """Follow the behaviour above and be fun and upbeat at all time. Stay accurate with your answers and don't make asumptions.
        
{history}
Human: {human_input}
Assistant:"""
        return t1 + t2

    def get_response(self, user_input):
        return self.chain.predict(human_input=user_input)

    def reset_memory(self):
        self.chain.memory.clear()


# Liste der aktiven Chatbots
active_chatbots = []


# funktion um history zu löschen.
def clearConversationHistoryGeneral(userId, subjectId):
    chatbot = next((bot for bot in active_chatbots if bot.user_id == userId), None)
    chatbot.reset_memory()
    updateSubject(userId, subjectId, conversationHistoryGeneralAnswers=[], conversationHistoryGeneralQuestions=[])


# Funktion, um die Antwort zu bekommen
def get_chatbot_response(userId, subjectId, userInput):
    if userInput.lower() == "clear":
        clearConversationHistoryGeneral(userId, subjectId)
        return {"question": userInput, "answer": "Chat history cleared"}
    subject = getSubjectById(userId, subjectId)
    subjectName = subject.get("name")
    extendChatHistoryWithPrompt(userId, subjectId, userInput)

    # Suche nach dem Chatbot mit der gegebenen User-ID
    chatbot = next((bot for bot in active_chatbots if (bot.user_id == userId) and (bot.subject_id == subjectId)), None)

    # Wenn kein Chatbot gefunden wurde, erstelle einen neuen und füge ihn zur Liste hinzu
    if not chatbot:
        chatbot = Chatbot(userId, subjectId, subjectName)
        active_chatbots.append(chatbot)

    # Erhalte die Antwort vom Chatbot
    response = chatbot.get_response(userInput)
    # print(response)
    extendChatHistoryWithAnswer(userId, subjectId, response)

    return {"question": userInput, "answer": response}


def extendChatHistoryWithPrompt(userId, subjectId, prompt):
    questions, answers = getConversationHistoryGeneral(userId, subjectId)
    questions.append(prompt)
    updateSubject(userId, subjectId, conversationHistoryGeneralQuestions=questions)


def extendChatHistoryWithAnswer(userId, subjectId, answer):
    questions, answers = getConversationHistoryGeneral(userId, subjectId)
    answers.append(answer)
    updateSubject(userId, subjectId, conversationHistoryGeneralAnswers=answers)


def getConversationHistoryGeneral(userId, subjectId):
    subject = getSubjectById(userId, subjectId)
    if not subject:
        print("No subject found")
        return []
    return subject.get("conversationHistoryGeneralQuestions", []), subject.get("conversationHistoryGeneralAnswers", [])

# Beispiel
# user_id = "txzUE0ZwDjgT9rK5zjUu"
# subject_id = "DuFdJczI0xorjilmQect"
# user_input = "Tell me something about principal component analysis and its usecases for visualization."
# response = get_chatbot_response(user_id, subject_id, user_input, )
# print("AI:", response)
