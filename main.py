from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from fastapi.middleware.cors import CORSMiddleware
import json

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Patient(BaseModel):
    id:Annotated[str,Field(...,description="id of the patient",examples=["P001"])]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="city in which the citizen is living")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal["male","female","others"],Field(...,description="Gender of patient")]  
    height:Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round((self.weight/self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) ->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else :
            return "Obese"
        

class PatientUpdate(BaseModel):
    id:Annotated[Optional[str],Field(description="id of the patient",examples=["P001"],default=None)]
    name: Annotated[Optional[str],Field(description="Name of the patient",default=None)]
    city:Annotated[Optional[str],Field(description="city in which the citizen is living",default=None)]
    age:Annotated[Optional[int],Field(gt=0,lt=120,description="Age of the patient",default=None)]
    gender:Annotated[Optional[Literal["male","female","others"]],Field(description="Gender of patient",default=None)]
    height:Annotated[Optional[float],Field(gt=0,description="Height of the patient in meters",default=None)]
    weight:Annotated[Optional[float],Field(gt=0,description="Weight of the patient in kgs",default=None)]




def load_data():
    with open('patients.json','r') as f:
        data=json.load(f) 
    return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)

@app.get("/")
async def hello():
    return {"val":"Patient Management System API"}

@app.get('/view')
def view():
    data=load_data()
    return data


@app.get("/view/{patient_id}")
def view_patient(patient_id:str = Path(...,description='ID of the patient in the DB', example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by : str = Query(...,description="Sort on the basis of height/weight/bmi"), order : str = Query('asc',description="sort in ascending or descending order")):
    valid_fields=["weight", "height", "bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail="Invalid field ,select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order, select asc or desc order")
    data=load_data()

    sort_order=True if order=="desc" else False
    sorted_data=sorted(data.values(),key= lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient:Patient):
    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201,content={"message":"patient created sucessfully"})



@app.put("/edit/{patient_id}")
def update_patient(patient_id:str,patient_update: PatientUpdate):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    exisiting_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        exisiting_patient_info[key]=value
    exisiting_patient_info['id']=patient_id
    patient=Patient(**exisiting_patient_info)
    exisiting_patient_info=patient.model_dump(exclude="id")
    data[patient_id]=exisiting_patient_info
    save_data(data)
    return JSONResponse(status_code=200,content={"message":"patient details updated"})


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found")
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200,content={"message":"patient deleted"})