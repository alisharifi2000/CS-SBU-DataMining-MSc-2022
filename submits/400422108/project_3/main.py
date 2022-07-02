from fastapi import FastAPI, Body
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
async def interpolate(
    data: Service1Data = Body(
        example={
            "config": {"time": "monthly", "interpolation": "linear", "type": "shamsi"},
            "data": [
                ["1397-06-27T18:34:10", 47827],
                ["1398-12-27T18:34:10", 70403],
                ["1395-06-27T18:34:10", 19129],
                ["1395-12-27T18:34:10", 63988],
                ["1400-01-27T18:34:10", 72013],
                ["1395-11-27T18:34:10", 63526],
                ["1399-02-27T18:34:10", 47184],
                ["1401-05-27T18:34:10", 88643],
                ["1400-02-27T18:34:10", 47827],
                ["1401-03-27T18:34:10", 90657],
            ],
        }
    )
):
    results = service1.interpolate_data(data.data, data.config)
    return results


####################################################### SERVICE 2

# Almost exactly the same as service1, we just assume that our inputs will definitely be miladi and we will convert our timestamps to shamsi at the end
@app.post("/service2")
async def shamsi_interpolate(
    data: Service2Data = Body(
        example={
            "config": {"time": "monthly", "interpolation": "linear"},
            "data": [
                ["1997-06-27T18:34:10", 47827],
                ["1998-12-27T18:34:10", 70403],
                ["1995-06-27T18:34:10", 19129],
                ["1995-12-27T18:34:10", 63988],
                ["2000-01-27T18:34:10", 72013],
                ["1995-11-27T18:34:10", 63526],
                ["1999-02-27T18:34:10", 47184],
                ["2001-05-27T18:34:10", 88643],
                ["2000-02-27T18:34:10", 47827],
                ["2001-03-27T18:34:10", 90657],
            ],
        }
    )
):
    results = service2.interpolate_data(data.data, data.config)
    return results


####################################################### SERVICE 3


@app.post("/service3")
async def outlier_detection(
    data: Service3Data = Body(
        examples={
            "with numerical index": {
                "config": {"time_series": "false"},
                "data": [
                    [0, 61.472635650492734],
                    [1, 98.80073800308276],
                    [2, 128.29438351371977],
                    [3, 60.959891186396284],
                    [4, -13.909137525328175],
                    [5, 46.3656622863595],
                    [6, 73.90197771562248],
                    [7, 172.87762781118286],
                    [8, -18.011298600593374],
                    [9, -94.71363236599937],
                    [10, -196.48695474702927],
                    [11, -162.96587660758814],
                    [12, 152.6664803860904],
                    [13, -16.94891320515504],
                    [14, -222.82136940095248],
                ],
            },
            "with datetime index": {
                "config": {"time_series": "true"},
                "data": [
                    ["2017-06-27T18:34:10", 61.472635650492734],
                    ["2018-06-27T18:34:10", 98.80073800308276],
                    ["2019-06-27T18:34:10", 128.29438351371977],
                    ["2016-06-27T18:34:10", 60.959891186396284],
                    ["2015-06-27T18:34:10", -13.909137525328175],
                    ["2016-05-27T18:34:10", 46.3656622863595],
                    ["2020-04-27T18:34:10", 73.90197771562248],
                    ["2020-01-27T18:34:10", 172.87762781118286],
                    ["2017-11-27T18:34:10", -18.011298600593374],
                    ["2017-10-27T18:34:10", -94.71363236599937],
                    ["2019-12-27T18:34:10", -196.48695474702927],
                    ["2019-11-27T18:34:10", -162.96587660758814],
                    ["2022-02-27T18:34:10", 152.6664803860904],
                    ["2021-03-27T18:34:10", -16.94891320515504],
                    ["2021-09-27T18:34:10", -222.82136940095248],
                ],
            },
        }
    )
):
    results = service3.detect_outliers(data.data, data.config)
    return results


####################################################### SERVICE 4


@app.post("/service4")
async def minority_class(data: Service4Data):
    results = service4.detect_outliers(data.data, data.config)
    return results
