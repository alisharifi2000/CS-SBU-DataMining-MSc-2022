import numpy as np
import pandas as pd
import datetime
#from statsmodels.tsa.ar_model import AutoReg
from utils.common import jalali_to_gregorian, gregorian_to_jalali
from dateutil.relativedelta import relativedelta
from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE, SVMSMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, NearMiss, CondensedNearestNeighbour, TomekLinks, EditedNearestNeighbours, OneSidedSelection


def interpolation_service1(data, type_config,time_config, ip_config):
    mydata = data
    mydata = convert_totime(mydata, type_config, time_config)
    if(isinstance(mydata, str)):
        return mydata
    print(mydata)
    if(ip_config == "linear"):
        mydata = linear_interpolation(mydata, time_config) 
    elif(ip_config == "polynomial"):
        mydata = polynomial_interpolation(mydata, time_config)
    elif(ip_config == "spline"):
        mydata = spline_interpolation(mydata, time_config)
    elif(ip_config=="regression"):
        mydata = regression_interpolation(mydata, time_config)    
    else:
        return "The interpolation method is wrong, we have linear, polynomial and spline method..."    

    if(type_config == "shamsi"):
        if(time_config=="monthly"):
            year = mydata.iloc[0, 0].year
            month = mydata.iloc[0, 0].month
            day = mydata.iloc[0, 0].day
            time_array = gregorian_to_jalali(year, month, day)
            mydata.iloc[0,0]="/".join([str(time_array[0]),str(time_array[1])]) 
            print(mydata.iloc[0,0])
            for i in range(1, mydata.shape[0]):
                if(month < 12):
                    time_array[1] = time_array[1] + 1
                elif(month == 12):
                    time_array[1] = 1
                    time_array[0] = time_array[0] + 1    
                mydata.iloc[i,0]="*".join([str(time_array[0]),str(time_array[1])]) 
                print(mydata.iloc[i,0])
        elif(time_config=="daily"):
            for i in range(0, mydata.shape[0]):
                year = mydata.iloc[i, 0].year
                month = mydata.iloc[i, 0].month
                day = mydata.iloc[i, 0].day
                time_array = gregorian_to_jalali(year, month, day)
                mydata.iloc[i,0]="*".join([str(time_array[0]),str(time_array[1]),str(time_array[2])]) 
                print("day:", mydata.iloc[i,0])
        else:
            return "The time config is wrong. we have daily and monthly"        
    else:
        print("mohammad")
        for i in range(0, mydata.shape[0]):
            print("mohammad")
            year = mydata.iloc[i, 0].year
            month = mydata.iloc[i, 0].month
            day = mydata.iloc[i, 0].day
            time_array = [year, month, day]
            if(time_config=="monthly"):
                mydata.iloc[i,0]="*".join([str(time_array[0]),str(time_array[1])])
            elif(time_config=="daily"):
                mydata.iloc[i,0]="*".join([str(time_array[0]),str(time_array[1]),str(time_array[2])])
            else:
                return "The time config is wrong. we have daily and monthly"
            print("day:", mydata.iloc[i, 0])    
    #mydata["time"] = mydata["time"].astype(str)   
    print(mydata)
    return mydata    

def interpolation_service2(data, time_config, ip_config):
    mydata = data
    mydata = convert_totime(mydata,"miladi", time_config)
    print(mydata)
    if(isinstance(mydata, str)):
        return mydata
    if(ip_config == "linear"):
        mydata = linear_interpolation(mydata, time_config) 
    elif(ip_config == "polynomial"):
        mydata = polynomial_interpolation(mydata, time_config)
    elif(ip_config == "spline"):
        mydata = spline_interpolation(mydata, time_config)
    else:
        return "The interpolation method is wrong, we have linear, polynomial and spline method..."    
    print("shahll") 
    if(time_config=="monthly"):
            year = mydata.iloc[0, 0].year
            month = mydata.iloc[0, 0].month
            day = mydata.iloc[0, 0].day
            time_array = gregorian_to_jalali(year, month, day)
            mydata.iloc[0,0]="*".join([str(time_array[0]),str(time_array[1])]) 
            print(mydata.iloc[0,0])
            for i in range(1, mydata.shape[0]):
                if(month < 12):
                    time_array[1] = time_array[1] + 1
                elif(month == 12):
                    time_array[1] = 1
                    time_array[0] = time_array[0] + 1    
                mydata.iloc[i,0]="*".join([str(time_array[0]),str(time_array[1])]) 
                print(mydata.iloc[i,0])
    elif(time_config=="daily"):
            for i in range(0, mydata.shape[0]):
                year = mydata.iloc[i, 0].year
                month = mydata.iloc[i, 0].month
                day = mydata.iloc[i, 0].day
                time_array = gregorian_to_jalali(year, month, day)
                mydata.iloc[i,0]="*".join([str(time_array[0]),str(time_array[1]),str(time_array[2])]) 
                print(mydata.iloc[i,0])
    else:
        return "The time config is wrong. we have daily and monthly"    
    print(mydata)
    return mydata    

def convert_totime(data, type_config, time_config):
    mydata = data
    for i in range(0, mydata.shape[0]):
        print(type(mydata.iloc[i, 0]))
        if(isinstance(mydata.iloc[i , 0], str) == False):
            return "the format of time is wrong... (y/m(monthly) & y/m/d(daily)"
        timearray = mydata.iloc[i , 0].split("/")
        print(timearray)
        if(type_config=="shamsi"):
            if(len(timearray)==2):
                if(time_config != "monthly"):
                    return "The format time is monthly but the time config is not monthly..."
                if(timearray[1]>12):
                    return "the month must less than 13..."    
                timearray = jalali_to_gregorian(int(timearray[0]),int(timearray[1]), 1) 
                mydata.iloc[i, 0] = datetime.datetime(int(timearray[0]),int(timearray[1]),1)
            elif(len(timearray)==3):
                if(time_config != "daily"):
                    return "The format time is daily but the time config is not daily..."
                if(timearray[1]>12):
                    return "the month must less than 13..."       
                timearray = jalali_to_gregorian(int(timearray[0]),int(timearray[1]), int(timearray[2])) 
                mydata.iloc[i, 0] = datetime.datetime(int(timearray[0]),int(timearray[1]), int(timearray[2]))
            else:
                return "the format of time is wrong... (y/m(monthly) & y/m/d(daily)" 
            print(timearray)     
        elif(type_config == "miladi"):
            if(len(timearray)==2):
                if(time_config != "monthly"):
                    return "The format time is monthly but the time config is not monthly..."
                mydata.iloc[i, 0] = datetime.datetime(int(timearray[0]),int(timearray[1]),1)
            elif(len(timearray)==3): 
                if(time_config != "daily"):
                    return "The format time is daily but the time config is not daily..."   
                mydata.iloc[i, 0] = datetime.datetime(int(timearray[0]),int(timearray[1]), int(timearray[2]))
            else:
                return "the format of time is wrong... (y/m(monthly) & y/m/d(daily)"
        else:
            return "The Type config is wrong, we have miladi and shamsi..."
    return mydata

def convert_totime_shamsi(mydata):
    mydata = data
    for i in range(0, mydata.shape[0]):
        if(isinstance(mydata.iloc[i , 0], str) == False):
            return "the format of time is wrong... (y/m(monthly) & y/m/d(daily)"
        timearray = mydata.iloc[i , 0].split("/")
        print(timearray)
        
        if(len(timearray)==2):
            if(time_config != "monthly"):
                    return "The format time is monthly but the time config is not monthly..."
            timearray = gregorian_to_jalali(int(timearray[0]),int(timearray[1]), 1) 
            mydata.iloc[i, 0] = datetime.datetime(int(timearray[0]),int(timearray[1]),1)
        elif(len(timearray)==3):
            if(time_config != "daily"):
                    return "The format time is daily but the time config is not daily..."
            timearray = gregorian_to_jalali(int(timearray[0]),int(timearray[1]), int(timearray[2])) 
            mydata.iloc[i, 0] = datetime.datetime(int(timearray[0]),int(timearray[1]), int(timearray[2]))
        else:
            return "the format of time is wrong... (y/m(monthly) & y/m/d(daily)"
    return mydata
    

def polynomial_interpolation(data, time_config):
    mydata = data
    min_time = np.min(mydata["time"])
    #min_time = min_time + np.timedelta64(1, 'D')
    max_time = np.max(mydata["time"]) 
    mydata_new = pd.DataFrame(columns=['time', 'vol'])
    row_index = -1
    i = 0
    while min_time <= max_time:
        for j in range(0, mydata.shape[0]):
            if(time_config=="monthly"):
                if(min_time.year == mydata.iloc[j, 0].year and min_time.month == mydata.iloc[j, 0].month):
                    row_index = j
                    break
            elif(time_config=="daily"):
                if(min_time.year == mydata.iloc[j, 0].year and min_time.month == mydata.iloc[j, 0].month and min_time.day == mydata.iloc[j, 0].day):
                    row_index = j
                    break
        print(row_index)
        if(row_index > -1):
            mydata_new = mydata_new.append({"time" : min_time, "vol":mydata.iloc[row_index, 1]}, ignore_index=True)
        else:
            mydata_new = mydata_new.append({"time" : min_time, "vol": None}, ignore_index=True)
        if(time_config == "daily"):    
            min_time = min_time + datetime.timedelta(days=1) 
        elif(time_config == "monthly"):
            min_time = min_time + relativedelta(months=1)
        i = i + 1 
        row_index = -1  
    mydata_new["vol"] = pd.to_numeric(mydata_new["vol"])
    print(mydata_new)
    mydata_new["vol"] = mydata_new["vol"].interpolate(method = "polynomial", order = 2)
    print(mydata_new)
    return mydata_new

def spline_interpolation(data, time_config):
    mydata = data
    min_time = np.min(mydata["time"])
    #min_time = min_time + np.timedelta64(1, 'D')
    max_time = np.max(mydata["time"]) 
    mydata_new = pd.DataFrame(columns=['time', 'vol'])
    row_index = -1
    i = 0
    while min_time <= max_time:
        for j in range(0, mydata.shape[0]):
            if(time_config=="monthly"):
                if(min_time.year == mydata.iloc[j, 0].year and min_time.month == mydata.iloc[j, 0].month):
                    row_index = j
                    break
            elif(time_config=="daily"):
                if(min_time.year == mydata.iloc[j, 0].year and min_time.month == mydata.iloc[j, 0].month and min_time.day == mydata.iloc[j, 0].day):
                    row_index = j
                    break
        print(row_index)
        if(row_index > -1):
            mydata_new = mydata_new.append({"time" : min_time, "vol":mydata.iloc[row_index, 1]}, ignore_index=True)
        else:
            mydata_new = mydata_new.append({"time" : min_time, "vol": None}, ignore_index=True)
        if(time_config == "daily"):    
            min_time = min_time + datetime.timedelta(days=1) 
        elif(time_config == "monthly"):
            min_time = min_time + relativedelta(months=1)
        i = i + 1 
        row_index = -1  
    mydata_new["vol"] = pd.to_numeric(mydata_new["vol"])
    print(mydata_new)
    mydata_new["vol"] = mydata_new["vol"].interpolate(method = "spline", order = 2)
    print(mydata_new)
    return mydata_new

def linear_interpolation(data, time_config):
    mydata = data
    min_time = np.min(mydata["time"])
    #min_time = min_time + np.timedelta64(1, 'D')
    max_time = np.max(mydata["time"]) 
    mydata_new = pd.DataFrame(columns=['time', 'vol'])
    row_index = -1
    i = 0
    while min_time <= max_time:
        for j in range(0, mydata.shape[0]):
            if(time_config=="monthly"):
                if(min_time.year == mydata.iloc[j, 0].year and min_time.month == mydata.iloc[j, 0].month):
                    row_index = j
                    break
            elif(time_config=="daily"):
                if(min_time.year == mydata.iloc[j, 0].year and min_time.month == mydata.iloc[j, 0].month and min_time.day == mydata.iloc[j, 0].day):
                    row_index = j
                    break
        print(row_index)
        if(row_index > -1):
            mydata_new = mydata_new.append({"time" : min_time, "vol":mydata.iloc[row_index, 1]}, ignore_index=True)
        else:
            mydata_new = mydata_new.append({"time" : min_time, "vol": None}, ignore_index=True)
        if(time_config == "daily"):    
            min_time = min_time + datetime.timedelta(days=1) 
        elif(time_config == "monthly"):
            min_time = min_time + relativedelta(months=1)
        i = i + 1 
        row_index = -1  
    mydata_new["vol"] = pd.to_numeric(mydata_new["vol"])
    print(mydata_new)
    mydata_new["vol"] = mydata_new["vol"].interpolate(method = "linear")
    print(mydata_new)
    return mydata_new

def sampling(data, method):
    X = data.iloc[:,0:(data.shape[1]-1)]
    y = data["class"]
    X_new = X
    y_new = y
    if(method=="undersampling"):
        undersample = RandomUnderSampler(sampling_strategy='majority')
        X_new, y_new = undersample.fit_resample(X, y)
    elif(method=="oversampling"):
        oversample = RandomOverSampler(sampling_strategy='minority')
        X_new, y_new = oversample.fit_resample(X, y)
    elif(method=="SMOTE"):
        oversample = SMOTE(k_neighbors=3)
        X_new, y_new = oversample.fit_resample(X, y)
    elif(method=="NearMiss1"):
        undersample = NearMiss(version=1, n_neighbors=3)
        X, y = undersample.fit_resample(X, y)
    elif(method=="NearMiss2"):
        undersample = NearMiss(version=2, n_neighbors=3)
        X, y = undersample.fit_resample(X, y) 
    elif(method=="NearMiss3"):
        undersample = NearMiss(version=3, n_neighbors=3)
        X, y = undersample.fit_resample(X, y)   
    elif(method=="CondensedNearestNeighbour"):
        undersample = CondensedNearestNeighbour(n_neighbors=1)
        X, y = undersample.fit_resample(X, y)
    elif(method=="CondensedNearestNeighbour"):
        undersample = TomekLinks()
        X, y = undersample.fit_resample(X, y) 
    elif(method=="EditedNearestNeighbours"):
        undersample = EditedNearestNeighbours(n_neighbors=3)
        X, y = undersample.fit_resample(X, y)    
    elif(method=="OneSidedSelection"):
        undersample = OneSidedSelection(n_neighbors=1, n_seeds_S=200)
        X, y = undersample.fit_resample(X, y)   
    elif(method=="BorderlineSMOTE"):
        oversample = BorderlineSMOTE()
        X, y = oversample.fit_resample(X, y)  
    elif(method=="SVMSMOTE"):
        oversample = SVMSMOTE()
        X, y = oversample.fit_resample(X, y) 
    elif(method=="ADASYN"):
        oversample = ADASYN()
        X, y = oversample.fit_resample(X, y)
             



    print("mohammad")
    print(X_new)
    print(y_new)
    result = pd.concat([X_new, y_new], axis = 1)
    return result


def outlierDetection(data, config):
    mydata = data
    result = mydata.iloc[:,0]
    if(config):
        firstMethod = firstOutDetec(data["vol"])
        secondMethod = secondOutDetec(data["vol"])
        thirdMethod = thirdOutDetec(data["vol"])
        forthMethod = forthOutDetec(data["vol"])
        result = pd.concat([result, firstMethod, secondMethod, thirdMethod, forthMethod], axis=1, join='inner')

    else:
        firstMethod = firstOutDetec(data["feature"])
        secondMethod = secondOutDetec(data["feature"])
        thirdMethod = thirdOutDetec(data["feature"])
        forthMethod = forthOutDetec(data["feature"])
        result = pd.concat([result, firstMethod, secondMethod, thirdMethod, forthMethod], axis=1, join='inner')

    return result    




def firstOutDetec(data):
    result = pd.DataFrame(columns=['method1'])
    print(data)
    #print(data.iloc[:,0])
    data_std = np.std(data)
    data_mean = np.mean(data)
    print(data_std)
    print(data_mean)
    cut_off = 3 * data_std
    lower_limit = data_mean - cut_off
    upper_limit = data_mean + cut_off
    print("lower",lower_limit)
    print("upper", upper_limit)
    for i in range(0, len(data)):
        print(data[i])
        if(data[i] < lower_limit or data[i] > upper_limit):
            result = result.append({'method1':True}, ignore_index=True)
        else:
            print("x")
            result = result.append({'method1':False}, ignore_index=True)  
    print(result)         
    return result

def secondOutDetec(data):
    result = pd.DataFrame(columns=['method2'])
    firstq = np.quantile(data, 0.25)
    thirdq = np.quantile(data, 0.75)
    IQR = thirdq - firstq
    lower_limit = firstq - 1.5 * IQR
    upper_limit = thirdq - 1.5 * IQR
    for i in range(0, data.shape[0]):
        if(data[i] < lower_limit or data[i]>upper_limit):
            result = result.append({'method2':True}, ignore_index=True)
        else:
            result = result.append({'method2':False}, ignore_index=True)    
    return result

from sklearn.ensemble import IsolationForest
def thirdOutDetec(data):
    data = np.array(data)
    data = data.reshape(-1,1)
    result = pd.DataFrame(columns=['method3'])
    np.random.seed(1)
    clf = IsolationForest(max_samples=100, random_state = 1)
    preds = clf.fit_predict(data)
    for i in range(0, data.shape[0]):
        if(preds[i]==-1):
            result = result.append({'method3':True}, ignore_index=True)
        else:
            result = result.append({'method3':False}, ignore_index=True)    
    return result

from sklearn.cluster import DBSCAN
from random import seed
def forthOutDetec(data):
    data = np.array(data)
    data = data.reshape(-1,1)
    result = pd.DataFrame(columns=['method4'])
    np.random.seed(1)
    outlier_detection = DBSCAN(min_samples = 2, eps = 3)
    clusters = outlier_detection.fit_predict(data)
    for i in range(0, data.shape[0]):
        if(clusters[i]==-1):
            result = result.append({'method4':True}, ignore_index=True)
        else:
            result = result.append({'method4':False}, ignore_index=True)    
    return result



