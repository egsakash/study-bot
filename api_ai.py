import json
import requests

endpoint = 'https://chatbot-vert-five.vercel.app/api/chat'
headers = {
    "Accept": "*/*",
    "Content-Type": "text/plain;charset=UTF-8",
    "DNT": "1",
    "Origin": "https://chatbot-vert-five.vercel.app",
    "Referer": "https://chatbot-vert-five.vercel.app/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


def gen(msg):
    response = requests.post(endpoint, headers=headers, json=msg)
    return response.json()['message']

prompt_sys = """You are an AI mentor of class 10 . You are created by a Person Named Akash who made you specializing in the NCERT Class 10 syllabus. Your role is to answer questions or explain topics from the syllabus in a clear, professional, and easy-to-understand language. Your responses should be of medium length and structured in a point-wise manner for better comprehension. Use emojis when appropriate to make the explanations engaging. Please note that any messages unrelated to Class 10 NCERT syllabus should not be entertained. Instead, kindly remind the user to focus on Class 10 related doubts or topic explanations. - Extra Tip: you can use <b>Text</b> to bold text . <i></i> To Italic and <u>To Underline</u>. Use this to make Your Message more approriate and beautiful to understand easily.
"""


syllabus = """ Below is the syllabus so try to find topics in this if they are related of these subjects.
- Science
Chemical Reactions and Equations
Acids, Bases and Salts
Metals and Non-metals
Carbon and Its Compounds
Life Processes
Control and Coordination
How Do Organisms Reproduce?
Heredity and Evolution
Light Reflection and Refraction
Human Eye and Colourful World
Electricity
Magnetic Effects of Electric Current
Our Environment

-Maths
Real Numbers
Polynomials
Pair of Linear Equations in Two Variables
Quadratic Equations
Arithmetic Progressions
Triangles
Coordinate Geometry
Introduction to Trigonometry
Some Applications of Trigonometry
Circles
Areas Related to Circles
Surface Areas and Volumes
Statistics
Probability

- History – India and Contemporary World II

The Rise of Nationalism in Europe
Nationalism in India
The Making of a Global World
The Age of Industrialisation
Print Culture and the Modern World1
Geography – Contemporary India II

Resources and Development
Forest and Wildlife Resources
Water Resources
Agriculture

Economics – Understanding Economic Development

Development
Sectors of the Indian Economy
Money and Credit
Globalisation and the Indian Economy
Consumer Rights
Political Science – Democratic Politics II

Power Sharing
Federalism
Democracy and Diversity
Gender, Religion, and Caste
Popular Struggles and Movements
Political Parties
Outcomes of Democracy
Challenges to Democracy


Search for topics in this syllabus if the topic is relevant to this syllabus. And if its out of scope prevent answering as its not your task.
"""

def encode_msg(sys , text):
    return [{"role": "System", "message": sys},{"role": "System", "message": syllabus},{"role":"User" ,"message": f"`{text}`. Use Easy to undertand language. ASCII characters for styling and write in points untill stated."}]

def generate(text):
    return gen(encode_msg(prompt_sys,text))[1:]


def format_topic(topic):
    sys_msg = f""""You are an AI model tasked with generating multiple-choice questions (MCQs) for the NCERT class 10 syllabus. The MCQs should be competency-based and challenging, designed to test the depth of a student's understanding of the topic. Each MCQ should consist of a question, four options, and an explanation. 

The question should be very concise, clear, and professionally worded. It should be framed in such a way that it requires critical thinking and a strong grasp of the topic to answer correctly.

The options should be short and plausible. They should be crafted carefully to avoid any ambiguity. Each option should seem probable to ensure the question is challenging.

The explanation should be brief and directly related to the question and the correct answer. It should provide clear reasoning for why the correct answer is right and why the other options are wrong.

Remember, the language used should be professional and creative. The MCQs should strictly adhere to the NCERT class 10 syllabus and are limited to the content of NCERT Class 10 books . If the topic provided is not part of the syllabus, return a blank JSON. If no specific topic is provided, select a random topic from the NCERT class 10 syllabus.

Here is the format of the MCQ: {{ 'q': '', 'op1': '', 'op2': '', 'op3': '', 'op4': '', 'right': '', 'exp': '' }}

Note that the Question is meant to be posted as a telegram poll using bot , Telegram not allows Very Long options and content for poll . so Keep the length short.

Now, generate an MCQ for the following topic: '{topic}'"
"""
    return sys_msg

def genmcq(topic, retries=3):
    mcqs = []
    for _ in range(retries):
        output = gen([{"role":"User" ,"message": format_topic(topic)}])[1:].replace("'", "\"")
        try:
            mcq = json.loads(output)
            mcqs.append(mcq)
            break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(output)
            print('Trying Again')
    return mcqs

