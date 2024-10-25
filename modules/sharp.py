from openai import OpenAI
import random
import os


def generate(api_key):
    client = OpenAI(
    api_key=api_key,
    base_url='https://api.opentyphoon.ai/v1')


    fewshots= (open('quote.txt', 'r',encoding="UTF-8").readlines())
    random.shuffle(fewshots)
    fewshots = "".join(fewshots[0:199])

    chat_completion = client.chat.completions.create(
        model="typhoon-instruct",
        messages=[
    {"role": "systemp", 
    "content": f"""
ระบบ: 
คุณเป็นเครื่องสร้างคำคมที่มีความสุขและขำขันโดยเฉพาะในการสร้าง 'คำคมเสี่ยวๆ จีบสาว' สร้างคำคมเสี่ยวๆ ที่ไม่เคยใช้มาก่อน คำคมต้องเป็นเอกลักษณ์, ขำขัน, และเหมาะสมสำหรับการจีบสาว อย่าใช้คำคมใดๆ ที่ได้รับใน Few Shots หรือการเปลี่ยนแปลงที่คล้ายคลึงกัน ตอบด้วยคำคมเสี่ยวๆ เท่านั้น ไม่มีอะไรอื่น
Few Shots:
{fewshots}
"""},
    {
    "role": "user",
    "content": f"""ขอคําคมเสี่ยวๆ หน่อย""",
    }






    ],temperature=0.9,top_p=0.9
    )
    reply = (chat_completion.choices[0].message.content).replace('"',"").replace("'","")
    if reply.replace(" ","").replace(".","") in fewshots.replace(" ","").replace(".","").replace("'",""):
        return generate()
    else:
        return reply
