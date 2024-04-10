import converter
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Union
import uvicorn

conv = FastAPI()


class CRS(str, Enum):
    # 为什么要分开大小写？
    WGS84 = "WGS84"
    wgs84 = "wgs84"
    GCJ02 = "GCJ02"
    gcj02 = "gcj02"
    BD09 = "BD09"
    bd09 = "bd09"
    MapBar = "MapBar"
    mapbar = "mapbar"




class Coordinates(BaseModel):
    longitude: float # 可以用Field添加字段描述，然后用简短的字段来命名，lng,lat,from,to等等
    latitude: float
    origin_crs: CRS
    target_crs: CRS


class Converted_Coordinates(BaseModel):
    lng: float
    lat: float


@conv.post("/convert/", response_model=Converted_Coordinates)
# @conv.post("/convert/")
def convert_coordinates(coords: Coordinates):# 实现功能：可以传入一个列表，批量转换
    origin_crs = coords.origin_crs.lower()
    target_crs = coords.target_crs.lower()
    # 假设origin_crs == target_crs，则不需要转换
    convert_algo = f"{origin_crs}_to_{target_crs}"
    # 要先判断是否存在这个算法，否则会报错
    lng, lat = getattr(converter, convert_algo)(coords.longitude, coords.latitude)
    result = {"lng": lng, "lat": lat}
    return result

if __name__ == '__main__':
    uvicorn.run(conv, host='127.0.0.1', port=8000)