import shutil

import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form
import pandas as pd
from typing import  List

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Track(BaseModel):
    track_name: str
    artist_name: str
    artist_count: int
    released_year: int
    released_month: int
    released_day: int
    in_spotify_playlists: bool
    in_spotify_charts: bool
    streams: int
    in_apple_playlists: bool
    in_apple_charts: bool
    in_deezer_playlists: bool
    in_deezer_charts: bool
    in_shazam_charts: bool
    bpm:float
    key: str
    mode: str
    danceability_percent: float
    valence_percent: float
    energy_percent: float
    acousticness_percent: float
    instrumentalness_percent:float
    liveness_percent: float
    speechiness_percent: float

class ListadoTracks(BaseModel):
    tracks = List[Track]
app = FastAPI(
    title="Servidor de datos",
    description="""Servimos datos de contratos, pero podríamos hacer muchas otras cosas, la la la.""",
    version="0.1.0",
)


@app.get("/retrieve_data/")
def retrieve_data ():
    todosmisdatos = pd.read_csv('spotify-2023.csv',sep=',', encoding = 'ISO-8859-1')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = ListadoTracks()
    listado.tracks = todosmisdatosdict
    return listado
