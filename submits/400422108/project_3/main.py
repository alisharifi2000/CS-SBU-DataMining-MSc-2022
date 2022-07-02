from fastapi import FastAPI
from models import *
import service1
import service2
import service3
import service4

app = FastAPI()


@app.get("/")
@app.post("/")
async def is_up():
    return "API is up!"


####################################################### SERVICE 1


@app.post("/service1")
async def interpolate(data: Service1Data):
    results = service1.interpolate_data(data.data, data.config)
    return results


####################################################### SERVICE 2

# Almost exactly the same as service1, we just assume that our inputs will definitely be miladi and we will convert our timestamps to shamsi at the end
@app.post("/service2")
async def shamsi_interpolate(data: Service2Data):
    results = service2.interpolate_data(data.data, data.config)
    return results


####################################################### SERVICE 3


@app.post("/service3")
async def outlier_detection(data: Service3Data):
    results = service3.detect_outliers(data.data, data.config)
    return results


####################################################### SERVICE 4


@app.post("/service4")
async def minority_class(data: Service4Data):
    results = service4.detect_outliers(data.data, data.config)
    return results
