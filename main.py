from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import mysql.connector
import json

# 数据库配置
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'fastapi'
}

# 实体类
class Patient(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None

# 统一返回类型类
class CommonResponse():
    def __init__(self, code, data, message) -> None:
        self.code = code
        self.data = data
        self.message = message

# 实例化对象
app = FastAPI()
db = mysql.connector.connect(**config)
cursor = db.cursor()

# 添加病人
@app.post("/patients")
async def add(patient: Patient):
    # print(json.dumps(patient.__dict__, indent=4, sort_keys=True, default=str)) // object to dict
    sql = ("INSERT INTO patient(first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)")
    cursor.execute(sql, (patient.first_name, patient.last_name, patient.email, patient.phone,))
    db.commit()
    log_id = cursor.lastrowid
    return CommonResponse(200, {"patient_id":log_id}, "success")

# 删除病人
@app.delete("/patient/{id}")
async def delete(id:int):
    sql = ("DELETE FROM patient WHERE id = %s")
    cursor.execute(sql, (id,))
    db.commit()
    return CommonResponse(200, {"patient_id": id}, "success")

# 更新病人
@app.put("/patient/{id}")
async def update(id:int, patient: Patient):
    sql = ("UPDATE patient SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE id= %s")
    cursor.execute(sql, (patient.first_name, patient.last_name, patient.email, patient.phone, id,))
    db.commit()
    return CommonResponse(200, {"patient_id": id}, "success")

# 查询单个病人
@app.get("/patient/{id}")
async def get_one(id:int):
    sql = ("SELECT * FROM patient WHERE id = %s")
    cursor.execute(sql, (id,))
    return CommonResponse(200, {"patient": cursor.fetchone()}, "success")

# 查询全部病人
@app.get("/patients")
async def get_all():
    sql = ("SELECT * FROM patient")
    cursor.execute(sql, ())
    return CommonResponse(200, [row for row in cursor.fetchall()], "success")
