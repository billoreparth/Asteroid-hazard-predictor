import os 
import sys
import random
import pandas as pd 
from fastapi import FastAPI , Request 
from dotenv import load_dotenv
from datetime import datetime , timedelta
from fastapi.templating import Jinja2Templates
import httpx
from Prediction_pipeline.prediction_pipeline import Prediction_pipeline
from Torino_system.torino_system import torino
from fastapi.responses import JSONResponse , HTMLResponse
from fastapi.staticfiles import StaticFiles
import pymongo
from datetime import datetime
import requests
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


def get_data_from_api():
    present = datetime.now()
    today = present.strftime('%Y-%m-%d')
    yesterday_time = present + timedelta(days=-1)
    yesterday = yesterday_time.strftime('%Y-%m-%d')
    
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={yesterday}&end_date={today}&api_key={os.getenv('API_KEY')}"
    
    response = requests.get(url)
    
    pred_pipe = Prediction_pipeline(response=response , yesterday=yesterday,today=today)
    pred_df , info_df = pred_pipe.run_pipeline()
    pred_df['name'] = info_df['name']
    pred_df['id'] = info_df['id']
    tor_sys = torino(pred_df)
    final_df = tor_sys.give_torino_rating(3500)

    

    records_pred = final_df.to_dict("records")
    records_info = info_df.to_dict("records")

    return records_pred , records_info

def update_server_data():
    try:
        
        url = os.getenv("MONGO_DB_URL")
        client = pymongo.MongoClient(url)
        client.admin.command('ping')
        print("connection succesfull")

    except Exception as e : 
        print(f"server connection failure: {e}")
    
    try:
        astroid_dict , info_dict = get_data_from_api()
        db = client['AsteroidDB']
        collection = db['Asteroid-pred-data']
        collection2 = db['ASteroid-info-data']

        setup_logging("Uploading the prediction data")
        collection.delete_many({})
        collection.insert_many((astroid_dict))
        collection.insert_one({"_meta":True,"last_updated":datetime.now()})

        setup_logging("Uploading the information data")
        collection2.delete_many({})
        collection2.insert_many((info_dict))
        collection2.insert_one({"_meta":True,"last_updated":datetime.now()})
    
    except Exception as e : 
        print("failed to get data from api")
        raise custom_exception(e,sys)
        

def fetch_ped_data_from_server():
    try:
        
        url = os.getenv("MONGO_DB_URL")
        client = pymongo.MongoClient(url)
        client.admin.command('ping')
        print("connection succesfull")

    except Exception as e : 
        print(f"server connection failure: {e}")

    try : 
        db = client['AsteroidDB']
        collection = db['Asteroid-pred-data']
        data = list(collection.find())
        df = pd.DataFrame(data)
        return df
    except Exception as e  :
        raise custom_exception(e,sys)
    

def fetch_info_data_from_server():
    try:
        
        url = os.getenv("MONGO_DB_URL")
        client = pymongo.MongoClient(url)
        client.admin.command('ping')
        print("connection succesfull")

    except Exception as e : 
        print(f"server connection failure: {e}")

    try : 
        db = client['AsteroidDB']
        collection = db['ASteroid-info-data']
        data = list(collection.find())
        df = pd.DataFrame(data)
        return df 
    except Exception as e  :
        raise custom_exception(e,sys)


async def fetch_background_image():
    fallback_images = [
    "/static/assets/background1.jpg",
    "/static/assets/background2.jpg",
    "/static/assets/background3.jpg"]
    url = f"https://api.nasa.gov/planetary/apod?api_key={os.getenv("API_KEY")}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url)
            res.raise_for_status()
            data = res.json()
            return {
                "url": data.get("url"),
                "title": data.get("title", "NASA Image")
            }
    except Exception as e:
        print("NASA API failed, using fallback:", e)
        # pick a random local background
        return {
            "url": random.choice(fallback_images),
            "title": "Fallback Space Background"
        }

     
@app.get("/updateData")
async def updateData():
    update_server_data()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    bg_url = None
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={os.getenv("API_KEY")}"
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            bg_url = data.get("url")
    except Exception as e:
        print(f"NASA API failed: {e}")
        # fallback to local static image
        fallback_image =  [
    "/static/assets/background1.jpg",
    "/static/assets/background2.jpg",
    "/static/assets/background3.jpg"]
        bg_url = random.choice(fallback_image)

    return templates.TemplateResponse("index.html", {"request": request, "bg_url": bg_url})

@app.post("/predict")
async def predict_hazard(request : Request):
    df = fetch_ped_data_from_server()
    df = df.drop(columns=["_id","_meta","last_updated"], errors="ignore")
    df = df.sort_values("miss_distance_in_astronomical", ascending=True).head(10)
    print(df)
    records = df.to_dict(orient="records")

    return JSONResponse(content={"asteroids": records})
  
@app.get("/visualize")
async def visualize(request: Request):
    """
    Renders the 3D visualization page. The page's JS will call /predict to get the asteroid list.
    """
    return templates.TemplateResponse("visualize.html", {"request": request})

@app.get("/moreinfovisualize", response_class=HTMLResponse)
async def moreinfo_visualize(id: str, request: Request):
    # fetch asteroid info by ID
    df = fetch_ped_data_from_server()
    df = df[df["id"] == id]

    if df.empty:
        return HTMLResponse("<h2>Asteroid not found</h2>", status_code=404)

    asteroid = df.to_dict(orient="records")[0]
    return templates.TemplateResponse("moreinfovisualize.html", {"request": request, "asteroid": asteroid})

