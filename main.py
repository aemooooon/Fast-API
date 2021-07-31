from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import datetime
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

origins = [
    "http://localhost:5500",
    "http://localhost:8000"
]

# 实例化对象
app = FastAPI()
db = mysql.connector.connect(**config)
cursor = db.cursor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加病人
@app.post("/patients")
async def add_patient(patient: Patient):
    # print(json.dumps(patient.__dict__, indent=4, sort_keys=True, default=str)) // object to dict
    sql = ("INSERT INTO patient(first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)")
    cursor.execute(sql, (patient.first_name, patient.last_name, patient.email, patient.phone,))
    db.commit()
    log_id = cursor.lastrowid
    return CommonResponse(200, {"patient_id":log_id}, "success")

# 删除病人
@app.delete("/patient/{id}")
async def delete_patient_by_id(id:int):
    sql = ("DELETE FROM patient WHERE id = %s")
    cursor.execute(sql, (id,))
    db.commit()
    return CommonResponse(200, {"patient_id": id}, "success")

# 更新病人
@app.put("/patient/{id}")
async def update_patient_by_id(id:int, patient: Patient):
    sql = ("UPDATE patient SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE id= %s")
    cursor.execute(sql, (patient.first_name, patient.last_name, patient.email, patient.phone, id,))
    db.commit()
    return CommonResponse(200, {"patient_id": id}, "success")

# 查询单个病人
@app.get("/patient/{id}")
async def get_patient_by_id(id:int):
    sql = ("SELECT * FROM patient WHERE id = %s")
    cursor.execute(sql, (id,))
    return CommonResponse(200, {"patient": cursor.fetchone()}, "success")

# 查询全部病人
@app.get("/patients")
async def get_patients():
    sql = ("SELECT * FROM patient")
    cursor.execute(sql, ())
    return CommonResponse(200, [row for row in cursor.fetchall()], "success")


# 数据表结构信息
# DROP TABLE IF EXISTS `patient`;
# CREATE TABLE IF NOT EXISTS `patient` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `first_name` varchar(50) DEFAULT NULL,
#   `last_name` varchar(50) DEFAULT NULL,
#   `email` varchar(50) DEFAULT NULL,
#   `phone` varchar(50) DEFAULT NULL,
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;