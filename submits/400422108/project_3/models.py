from pydantic import BaseModel
from enum import Enum

################ Define data models

# Date format enum
class DateFormatEnum(str, Enum):
    miladi = "miladi"
    shamsi = "shamsi"


# Interpolation time enum
class InterpolationTimeEnum(str, Enum):
    daily = "daily"
    monthly = "monthly"
    hourly = "hourly"
    minute = "minute"


# Interpolation type enum
class InterpolationType(str, Enum):
    linear = "linear"
    nearest = "nearest"
    spline = "spline"
    polynomial = "polynomial"
    slinear = "slinear"


# Config BaseModel
class ServiceConfig(BaseModel):
    type: DateFormatEnum = DateFormatEnum.miladi
    time: InterpolationTimeEnum = InterpolationTimeEnum.monthly
    interpolation: InterpolationType = InterpolationType.linear


class Service1Data(BaseModel):
    config: ServiceConfig = None
    data: list


#####


class Service2Config(BaseModel):
    time: InterpolationTimeEnum = InterpolationTimeEnum.monthly
    interpolation: InterpolationType = InterpolationType.linear


class Service2Data(BaseModel):
    data: list
    config: Service2Config


#####


class Service3Config(BaseModel):
    time_series: bool


class Service3Data(BaseModel):
    data: list
    config: Service3Config


###
class Service4Config(BaseModel):
    time_series: bool


class Service4Data(BaseModel):
    data: list
    config: Service4Config
