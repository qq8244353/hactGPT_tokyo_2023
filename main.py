import os
import openai
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import Annotated
import shutil
from dotenv import load_dotenv

load_dotenv(override=True)
openai.api_key = os.environ['OPENAI_API_KEY']
messages = []
trials = 0

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=temperature,  # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
  response = openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=temperature, # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]

def generate_arguments(topic):
  if trials == 0: #初期状態
    prompt = """あなたは、ディベートのプロとして振る舞ってください。\n
              お題は「"""+str(topic)+"""」です。まずは、賛成側の立論を言ってください。\n
              補足1: わかりやすく簡潔に口語で3文以内で教えてください\n"""
  elif trials % 2 == 1: #反対の意見を述べる
    prompt = """反対側の立論を言ってください。賛成側の意見必ず踏まえて新しい観点で意見してください。。\n
                補足1: わかりやすく簡潔に口語で3文以内で教えてください。
                補足2: 賛成側の意見に反論することを重視して下さい。
                補足3: 新しい意見を言う場合は必ず理由を付け加えてください。
                補足4: 相手の主張が間違っている場合は相手を困らせるような質問をしてください。"""
  else: #賛成の意見を述べる
    prompt = """賛成側の立論を言ってください。反対側の意見を必ず踏まえて新しい観点で意見してください。\n
                補足1: わかりやすく簡潔に口語で3文以内で教えてください。
                補足2: 反対側の意見に反論することを重視して下さい。
                補足3: 新しい意見を言う場合は必ず理由を付け加えてください。
                補足4: 相手の主張が間違っている場合は相手を困らせるような質問をしてください。"""
  messages.append({"role": "user", "content": prompt})
  html = get_completion_from_messages(messages)
  messages.append({"role": "assistant", "content": html})
  print(messages)
  return html

def evaluate_arguments():
  prompt = """あなたは、公正な判定員としてふるまってください。この議論をもとに、どちらの意見が説得力がよりあったかを理由とともに教えてください。\n
              補足1: わかりやすく簡潔に口語で教えてください\n"""
  messages.append({"role": "user", "content": prompt})
  html = get_completion_from_messages(messages)
  messages.append({"role": "assistant", "content": html})
  return html

def summarize_debate(prompt, pro_score, con_score):
    winner = "Pro" if pro_score > con_score else "Con"
    prompt = f"The debate on '{prompt}' has ended. The Pro side won {pro_score} rounds, and the Con side won {con_score} rounds. Please provide a summary of the debate."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
  return {"message": "Hello World"}


class Item3(BaseModel):
  topic: str

@app.post("/debate")
async def debate(item: Item3):
  global trials
  topic = item.topic
  text = ""
  text = generate_arguments(topic)
  trials += 1
  return text

@app.get("/evaluate")
async def debate():
  global trials
  text = ""
  text = evaluate_arguments()
  trials = 0 #次の時のために初期化する
  return text
  

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)