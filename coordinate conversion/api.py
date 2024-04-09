import converter
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Union


conv = FastAPI()


class CRS(str, Enum):
    WGS84 = "WGS84"
    wgs84 = "wgs84"
    GCJ02 = "GCJ02"
    gcj02 = "gcj02"
    BD09 = "BD09"
    bd09 = "bd09"
    MapBar = "MapBar"
    mapbar = "mapbar"




class Coordinates(BaseModel):
    longitude: float
    latitude: float
    origin_crs: CRS
    target_crs: CRS


# class Converted_Coordinates(BaseModel):
#     lng: float
#     lat: float


# @conv.post("/convert/", response_model=Converted_Coordinates)
@conv.post("/convert/")
def convert_coordinates(coords: Coordinates):
    origin_crs = coords.origin_crs.lower()
    target_crs = coords.target_crs.lower()
    convert_algo = f"{origin_crs}_to_{target_crs}"
    lng, lat = getattr(converter, convert_algo)(coords.longitude, coords.latitude)
    result = {"lng": lng, "lat": lat}
    return result