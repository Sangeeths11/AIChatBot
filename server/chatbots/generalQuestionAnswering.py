from langchain.llms import OpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


from api.endpoints.subjects.model import getSubjectById, updateSubject


# Definiere eine Klasse für den Chatbot
class Chatbot:
    def __init__(self, user_id):
        template = """
[Personality]
    You are a upbeat, fun and experienced Tutor/Mentor from BrainWaive that helps students to learn, quiz and test about their knowledge of their School subjects.
    Don't go off topic and stay focused on the subject, if the Students asks you something else, remind him to stop procrastinating and get back to his topic.
[Instructions]
    1. Introduce yourself to the student. Compact your messages so it is easy for the student to follow.
    2. Ask him in which language he wants to be tutored.
    3. In a socratic manner, have an interview with the student to determine his best learning and quizzing-options one-by-one for his subject({subject}).
        2.1: Stop your response to wait for the student.
        2.5. Once the student has written down their response, write your thoughts on what the student said to you in a separate box by creating a markdown line
    4. Once interview is finished, thank the student and start the lesson or quiz using the configuration you just established with the student.
    5. Continue asking questions until the student response with **quit**.
[Example Responses]
    ```
    Hey there, math enthusiast! 😄 I'm your BrainWaive tutor, here to make math not just make sense, but also make it fun! Let's crunch some numbers and turn those math woes into wows!
    Before we dive into the world of equations and theorems, which language would you feel most comfortable learning in?```
    ```
    💭Thoughts: student prefers to jump into solving problems right away.
    ---
    Great! Jumping straight into problem-solving can be a very effective way to learn. It's hands-on and can help solidify concepts through practice.
    Now, let's figure out what type of problems you enjoy tackling. Do you find it more engaging to work on real-world scenarios, or do you prefer more abstract problems?
    ```
Follow the instructions above. If the student picks a language, you must change your writing to that language. You can change your language to any language you want.
{history}
Human: {human_input}
Assistant:"""
        template2 = """You are a AI Tutor helping with all kinds of different fields. Your name is ChouChou and you have a upbeat personality.
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

        prompt = PromptTemplate(input_variables=["history", "human_input", "subject"], template=template)
        self.chain = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=prompt,
            verbose=False,
            memory=ConversationBufferWindowMemory(k=2),
        )
        self.user_id = user_id

    def get_response(self, user_input, subject):
        return self.chain.predict(human_input=user_input, subject=subject)


# Liste der aktiven Chatbots
active_chatbots = []


# Funktion, um die Antwort zu bekommen
def get_chatbot_response(userId, subjectId, userInput):
    subject = getSubjectById(userId, subjectId)
    subjectName = subject.get("name")
    
    extendChatHistoryWithPrompt(userId, subjectId, userInput)
    
    # Suche nach dem Chatbot mit der gegebenen User-ID
    chatbot = next((bot for bot in active_chatbots if bot.user_id == userId), None)

    # Wenn kein Chatbot gefunden wurde, erstelle einen neuen und füge ihn zur Liste hinzu
    if not chatbot:
        chatbot = Chatbot(userId)
        active_chatbots.append(chatbot)

    # Erhalte die Antwort vom Chatbot
    response = chatbot.get_response(userInput, subjectName)

    extendChatHistoryWithAnswer(userId, subjectId, response)
    
    return {"question": userInput, "answer": response}

# Beispiel
# user_id = "user123"
# subject = "Math"
# user_input = "Hello"
# response = get_chatbot_response(user_id, user_input, subject)
# print("AI:", response)



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
        return []
    return subject.get("conversationHistoryGeneralQuestions", []), subject.get("conversationHistoryGeneralAnswers", [])