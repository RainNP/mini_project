from xml.dom.minidom import Element
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

class room_detail(BaseModel):
    room1: int
    room2: int
    room3: int
    
client = MongoClient('mongodb://localhost', 27017)

db = client["mini_project"]

collection = db["restroom"]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

to_time = [0,600,600,600]
to_time_num = [0,0,0,0]

@app.get("/room/status/all")
def get_reservation_by_name():
    result = collection.find({},{"_id" :0})
    myre = []
    for r in result:
        myre.append(r)
    return myre

@app.put("/room/update/")
def update_room(room_detail: room_detail,room : int):
    check = collection.find_one({"room":room},{"_id":0})
    if (check["status"] == 0):
        q = {"room":room}
        to_time_num[room] += 1
        time_in = check["time_arr"]
        h_in,m_in,s_in = time_in.split(':')
        total_in = int(h_in)*3600 + int(m_in)*60 + int(s_in)
        cc = datetime.now()
        time_out = cc.strftime("%H:%M:%S")
        h_out,m_out,s_out = time_out.split(':')
        total_out = int(h_out)*3600 + int(m_out)*60 + int(s_out)
        total_est = total_out - total_in
        to_time[room] += total_est
        gg = to_time[room]/to_time_num[room]
        new = {"$set" : {"status":1,"time_est" : gg}}
        collection.update_one(q, new)
        return "done"
    elif (check["status"] == 1):
        q = {"room":room}
        cc = datetime.now()
        time_in = cc.strftime("%H:%M:%S")
        new = {"$set" : {"status":0,"time_arr":time_in}}
        collection.update_one(q, new)
        return "done"
    else:
        return "nothing change"

@app.post("/room/post")
def testpost(room_detail : room_detail):
    check1 = collection.find_one({"room":1},{"_id":0})
    if (check1["status"] != room_detail.room1):
        update_room(room_detail,1)
    check2 = collection.find_one({"room":2},{"_id":0})
    if ((check2["status"] != room_detail.room2)):
        update_room(room_detail,2)
    check3 = collection.find_one({"room":3},{"_id":0})
    if ((check3["status"] != room_detail.room3)):
        update_room(room_detail,3)
    return "done"