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
async def minority_class(
    data: Service4Data = Body(
        example={
            "undersampling": {
                "config": {
                    "majority_class": 0,
                    "minority_class": 1,
                    "method": "undersampling",
                },
                "data": [
                    [0.12346424839969106, -0.8701646721968559, 0],
                    [-1.8748529075964784, -0.40010135008438796, 0],
                    [0.793217140386937, -0.6912429964714355, 1],
                    [-0.16314873233434635, -1.8697774314986293, 0],
                    [-1.1716059191794728, -0.7283634326060804, 0],
                    [-0.04578830191059091, -2.151375357516452, 1],
                    [-1.651009544147267, 2.510516526380222, 0],
                    [-1.3215663086656722, -2.841491435394474, 0],
                    [-0.3304726765698237, 0.08480610918924336, 0],
                    [-1.6695343313053086, -0.8068025216308399, 0],
                    [-0.7445720943799232, 0.4739444475550111, 0],
                    [-2.250933393613063, 1.7811167190069725, 0],
                    [0.9377527701232387, 1.3292657509166568, 1],
                    [-1.480954703170113, -1.8228845715395012, 0],
                    [-1.1483213463681816, 1.41178816262066, 0],
                    [-2.0304700502304525, -1.9980043668356209, 0],
                    [-0.5928838983866704, -1.0568115826711584, 0],
                    [-0.6318051649121657, 0.4644650922277097, 0],
                    [-0.9997186744882598, 1.3324797655474232, 0],
                    [-0.48757014121881015, 0.2803985098515429, 0],
                    [-0.413138715826726, 0.4183568305364106, 0],
                    [-0.8800205431359317, -1.5478414679483468, 0],
                    [-1.7237084116827144, -1.6752206369497684, 0],
                    [-1.2219087483271986, -0.9502245403777934, 0],
                    [0.17688017594491545, 0.5593139444068438, 0],
                    [-2.2324615490291526, -1.9227974592261017, 0],
                    [-0.1232188619444674, -0.2978982389044267, 0],
                    [-2.6446075806124387, 2.8771695874712266, 0],
                    [-2.132999508814976, 2.593311400836134, 0],
                    [-1.629783167051352, 1.2704301267739482, 0],
                ],
            },
            "oversampling": {
                "config": {
                    "majority_class": 0,
                    "minority_class": 1,
                    "method": "oversampling",
                },
                "data": [
                    [0.12346424839969106, -0.8701646721968559, 0],
                    [-1.8748529075964784, -0.40010135008438796, 0],
                    [0.793217140386937, -0.6912429964714355, 1],
                    [-0.16314873233434635, -1.8697774314986293, 0],
                    [-1.1716059191794728, -0.7283634326060804, 0],
                    [-0.04578830191059091, -2.151375357516452, 1],
                    [-1.651009544147267, 2.510516526380222, 0],
                    [-1.3215663086656722, -2.841491435394474, 0],
                    [-0.3304726765698237, 0.08480610918924336, 0],
                    [-1.6695343313053086, -0.8068025216308399, 0],
                    [-0.7445720943799232, 0.4739444475550111, 0],
                    [-2.250933393613063, 1.7811167190069725, 0],
                    [0.9377527701232387, 1.3292657509166568, 1],
                    [-1.480954703170113, -1.8228845715395012, 0],
                    [-1.1483213463681816, 1.41178816262066, 0],
                    [-2.0304700502304525, -1.9980043668356209, 0],
                    [-0.5928838983866704, -1.0568115826711584, 0],
                    [-0.6318051649121657, 0.4644650922277097, 0],
                    [-0.9997186744882598, 1.3324797655474232, 0],
                    [-0.48757014121881015, 0.2803985098515429, 0],
                    [-0.413138715826726, 0.4183568305364106, 0],
                    [-0.8800205431359317, -1.5478414679483468, 0],
                    [-1.7237084116827144, -1.6752206369497684, 0],
                    [-1.2219087483271986, -0.9502245403777934, 0],
                    [0.17688017594491545, 0.5593139444068438, 0],
                    [-2.2324615490291526, -1.9227974592261017, 0],
                    [-0.1232188619444674, -0.2978982389044267, 0],
                    [-2.6446075806124387, 2.8771695874712266, 0],
                    [-2.132999508814976, 2.593311400836134, 0],
                    [-1.629783167051352, 1.2704301267739482, 0],
                ],
            },
            "SMOTE": {
                "config": {
                    "majority_class": 0,
                    "minority_class": 1,
                    "method": "smote",
                },
                "data": [
                    [
                        [
                            -0.09193080062419168,
                            -0.8794384629627301,
                            1.2215550100703374,
                            0,
                        ],
                        [
                            -1.1138853817418313,
                            -0.9389773417606101,
                            -0.3866060005865022,
                            0,
                        ],
                        [
                            -1.0162012984316529,
                            0.05883374608962129,
                            -0.8611880706522596,
                            0,
                        ],
                        [
                            -1.0677563754622608,
                            -0.3480385753502833,
                            -1.204201511401986,
                            0,
                        ],
                        [
                            -1.658393598013502,
                            -0.2002345982311558,
                            0.8543282171937338,
                            0,
                        ],
                        [
                            -0.8264541374396093,
                            -1.1498314714020554,
                            1.0132341125423934,
                            0,
                        ],
                        [
                            -1.0425130494394859,
                            0.16450430576611405,
                            0.9833688672544408,
                            0,
                        ],
                        [
                            -0.3731086832095556,
                            0.23922850568292559,
                            -0.9890872113291048,
                            0,
                        ],
                        [-0.3089478089963994, 0.5580799054117489, 1.169102560060586, 0],
                        [
                            -1.2606529816061345,
                            -0.9582586255280183,
                            0.9486029013499785,
                            0,
                        ],
                        [
                            -0.8425913477014167,
                            -0.2804882330991991,
                            1.0025664883093148,
                            0,
                        ],
                        [
                            -1.6458694417237332,
                            -1.836657710245329,
                            -0.8092429444204252,
                            0,
                        ],
                        [
                            -0.7616056403567351,
                            -2.8928467875654302,
                            1.0648228806496471,
                            0,
                        ],
                        [
                            -2.0097557748782817,
                            0.07997103579254916,
                            0.7752269581924383,
                            0,
                        ],
                        [
                            -1.5835099804248494,
                            -0.3931890050030262,
                            -0.8450354554818829,
                            0,
                        ],
                        [
                            -2.0757967522664207,
                            -0.06331949482400803,
                            -0.8457784890007576,
                            0,
                        ],
                        [
                            -0.8110955422920885,
                            0.40030119813620135,
                            1.0279610246170099,
                            0,
                        ],
                        [
                            -1.107515494874578,
                            0.19175626251633474,
                            1.0100674691724625,
                            0,
                        ],
                        [
                            -1.5118514958670468,
                            0.625698848976413,
                            -1.0272144923916566,
                            0,
                        ],
                        [
                            -0.5994224754843178,
                            -0.06473269268757761,
                            1.0907063674508588,
                            0,
                        ],
                        [
                            -1.535895680192659,
                            1.7067862934916216,
                            -0.41349615519133176,
                            0,
                        ],
                        [
                            0.3963940183027822,
                            -0.7494142710826572,
                            -0.43899795629651117,
                            1,
                        ],
                        [
                            -0.44102419471928267,
                            -0.6715419651599653,
                            1.1162074081655597,
                            0,
                        ],
                        [
                            -0.5131745620822068,
                            -1.513150448645347,
                            -1.1997862887337492,
                            0,
                        ],
                        [
                            -0.8383097907430014,
                            0.4399749511958037,
                            -1.2733936331586504,
                            0,
                        ],
                        [
                            -0.11768155831102811,
                            0.5847961001232227,
                            -1.3016933247819027,
                            0,
                        ],
                        [
                            -2.257860323713821,
                            0.17875987177058125,
                            -0.6429558817508314,
                            0,
                        ],
                        [
                            -0.1477702333080988,
                            -0.13740115829626168,
                            -0.96422942781116,
                            0,
                        ],
                        [
                            1.2781897870201602,
                            1.0807017473030096,
                            -1.1906649402497953,
                            1,
                        ],
                        [
                            0.4866629352619415,
                            -0.37792194493700537,
                            -0.22117781731986663,
                            1,
                        ],
                        [
                            -0.5310296851966423,
                            -0.19334647046740144,
                            1.064386517418847,
                            0,
                        ],
                        [
                            -2.596940031686306,
                            -0.5775884825691815,
                            -0.9476331262785068,
                            0,
                        ],
                        [
                            -0.4924923654411828,
                            0.6534490489246408,
                            -1.503057869769688,
                            0,
                        ],
                        [
                            -0.839289482910288,
                            -0.08320657954480688,
                            -0.8091067041181313,
                            0,
                        ],
                        [
                            -0.3601619863936105,
                            0.2829246706824095,
                            -1.5608366726161935,
                            0,
                        ],
                        [
                            -0.8976545906646928,
                            1.9462776881435735,
                            1.0841678960760075,
                            0,
                        ],
                        [-1.15934453080372, 1.1942902751194884, 0.9468912353088124, 0],
                        [
                            -0.8734785436979016,
                            -0.7163838138648405,
                            -1.4863135209673637,
                            0,
                        ],
                        [-2.0981434629066813, -0.678599917026062, 0.727821528955432, 0],
                        [1.741069048966288, 1.0399977218323795, -1.5749301096139077, 1],
                        [-1.939345916710654, 0.748692242678393, -1.6820695107654342, 0],
                        [
                            -1.0184887618197942,
                            -0.319098097196024,
                            1.0710878773711536,
                            0,
                        ],
                        [
                            -1.8874468683990604,
                            1.2959533828998773,
                            0.7657224812539047,
                            0,
                        ],
                        [2.2013628936212903, 2.4512327721885083, 1.573130615243493, 1],
                        [
                            -0.7508823644255702,
                            -0.026863041157366985,
                            1.050597281683663,
                            0,
                        ],
                        [
                            -0.7536387375214628,
                            0.14195641024284072,
                            -0.6430339559460144,
                            0,
                        ],
                        [
                            -0.5958943263256973,
                            1.2628419906798114,
                            -1.5595657166109278,
                            0,
                        ],
                        [-1.147580061724108, -0.828010051432538, 0.9609943011464745, 0],
                        [-0.6705702133260655, 0.451929933406163, 1.1173573086548805, 0],
                        [
                            -1.231001795841048,
                            -1.0000680299164921,
                            -0.853783833414391,
                            0,
                        ],
                    ]
                ],
            },
        }
    )
):
    results = service4.minority_class_handle(data.data, data.config)
    return {"data": results}
