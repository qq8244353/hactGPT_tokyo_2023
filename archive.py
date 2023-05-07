import os
import openai
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import Annotated
import shutil
import time
from dotenv import load_dotenv

load_dotenv(override=True)
openai.api_key = os.environ['OPENAI_API_KEY']

# debate functions
def generate_arguments(prompt, stance):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{stance} argument: {prompt}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

def evaluate_arguments(pro_argument, con_argument):
    prompt = f"Between the pro argument '{pro_argument}' and the con argument '{con_argument}', which one is more logical and persuasive?"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=30,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

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

def debate(prompt, rounds=3):
    print(f"Debate topic: {prompt}\n")
    
    pro_score = 0
    con_score = 0
    
    for round_num in range(1, rounds + 1):
        print(f"Round {round_num}:")
        pro_argument = generate_arguments(prompt, "Pro")
        time.sleep(3) # Wait a bit to prevent API rate limits
        con_argument = generate_arguments(prompt, "Con")
        time.sleep(3) # Wait a bit to prevent API rate limits
        
        print(f"Pro: {pro_argument}")
        print(f"Con: {con_argument}\n")
        
        winner = evaluate_arguments(pro_argument, con_argument)
        time.sleep(3) # Wait a bit to prevent API rate limits
        print(f"Winner: {winner}\n")
        
        if winner == "Pro":
            pro_score += 1
        else:
            con_score += 1
    
    print("Debate results:")
    print(f"Pro: {pro_score}")
    print(f"Con: {con_score}")

    summary = summarize_debate(prompt, pro_score, con_score)
    return summary

# debate_topic = "AI should be regulated"
# debate(debate_topic)

# def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
#   messages = [{"role": "user", "content": prompt}]
#   response = openai.ChatCompletion.create(
#     model=model,
#     messages=messages,
#     temperature=
#     temperature,  # this is the degree of randomness of the model's output
#   )
#   return response.choices[0].message["content"]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
  return {"message": "Hello World"}


class Item(BaseModel):
  json_str: str


@app.post("/json2html")
async def json2html(item: Item):
  _json = item.json_str
  prompt = "以下のJSONをHTMLに変換してください。:\n" + str(_json)
  html = get_completion(prompt)
  return html

class Item2(BaseModel):
  command: str
  html: str


@app.post("/paint")
async def paint(item: Item2):
  command = item.command
  html = item.html
  prompt = f"""
  以下のhtmlに、以下の「操作」を加えたhtmlを出力してください。
  
  html: {html}
  操作: {command}
  """
  html = get_completion(prompt)
  return html


# @app.post("/upload_audio")
# async def upload_audio(file: Annotated[bytes, File()]):
#   audio_file = file.file
#   transcript = openai.Audio.transcribe("whisper-1", audio_file)
#   print(transcript)

#   return {"filename": file.filename}


@app.post("/upload_audio")
async def fileupload_post(request: Request):
  '''docstring
    アップロードされたファイルを保存する
    '''
  form = await request.form()
  for formdata in form:
    uploadfile = form[formdata]
    file_temp = uploadfile.file.read()
    # file = open("data/test.audio", mode="w")
    with open("data/test.mp3", "wb+") as f:
      f.write(file_temp)
    with open("data/test.mp3", "rb") as f:
      transcript_text = openai.Audio.transcribe("whisper-1", f)["text"]
    response = get_completion(transcript_text)
  return {"transcript": transcript_text, "response": response}
  
@app.post("/kabukayosou")
async def kabukayosou(item: Item2):
  command = item.command
  html = item.html
  prompt = f"""
  以下のhtmlに、以下の「操作」を加えたhtmlを出力してください。
  
  html: {html}
  操作: {command}
  """
  html = get_completion(prompt)
  return html

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
