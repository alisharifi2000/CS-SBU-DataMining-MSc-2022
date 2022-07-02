from pydantic import BaseModel
from enum import Enum

################ Define data models

# Date format enum
class DateFormatEnum(str, Enum):
    """
        Enum of specifying calendar. Used in service pydantic models.
        Possible values are: miladi, shamsi
    """
    miladi = "miladi"
    shamsi = "shamsi"


# Interpolation time enum
class InterpolationTimeEnum(str, Enum):
    """
        Enum for specifying interpolation interval. Used in service pydantic models.
        Possible values are: daily, monthly, hourly, minute
    """
    daily = "daily"
    monthly = "monthly"
    hourly = "hourly"
    minute = "minute"


# Interpolation type enum
class InterpolationType(str, Enum):
    """
        Enum for specifying interpolation type. Used in service pydantic models.
        Possible values are: linear, nearest, spline, polynomial, slinear. 
        Interpolation methods that require an order (such as polynomial) are hardcoded to order=3
    """
    linear = "linear"
    nearest = "nearest"
    spline = "spline"
    polynomial = "polynomial"
    slinear = "slinear"


# Config BaseModel
class ServiceConfig(BaseModel):
    """
        Model for service configs, aka for storing service config data such as calendar types.
        As per problem specification
    """
    type: DateFormatEnum = DateFormatEnum.miladi
    time: InterpolationTimeEnum = InterpolationTimeEnum.monthly
    interpolation: InterpolationType = InterpolationType.linear


class Service1Data(BaseModel):
    """
        Model for service 1. 
        Contains 2 fields, one for config, one for data, which is in the form of a list. 
        Please refer to the docs for more information.
    """
    config: ServiceConfig = None
    data: list


#####


class Service2Config(BaseModel):
    """
        Model for service configs, aka for storing service config data such as calendar types.
        As per problem specification
    """
    time: InterpolationTimeEnum = InterpolationTimeEnum.monthly
    interpolation: InterpolationType = InterpolationType.linear


class Service2Data(BaseModel):
    """
        Model for service 2. 
        Contains 2 fields, one for config (interpolation type (monthly, daily, ...)), and one for data which is in the form of a list.
        Please refer to the docs for more information.
    """
    data: list
    config: Service2Config


#####


class Service3Config(BaseModel):
    """
        Model for service configs, aka for storing service config data such as calendar types.
        As per problem specification
    """
    time_series: bool


class Service3Data(BaseModel):
    """
        Model for service 1. 
        Contains 2 fields, one for config, one for data, which is in the form of a list. 
        Please refer to the docs for more information.
    """
    data: list
    config: Service3Config


###
class Service4Config(BaseModel):
    """
        Model for service configs, aka for storing service config data such as calendar types.
        As per problem specification
    """
    time_series: bool


class Service4Data(BaseModel):
    data: list
    config: Service4Config
