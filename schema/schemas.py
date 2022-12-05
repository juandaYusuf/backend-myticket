# Variable class untuk menampung data yang akang di eksekusi oleh query
from pydantic import BaseModel


# !USER
class User(BaseModel):
    fullname: str
    email : str
    alamat: str
    noTelepon: str
    password: str
    jenisKelamin: str
    profilPhoto: str
    profilBannerPhoto: str

class LoginData(BaseModel):
    email: str
    password: str

class CheckCurrentPWD(BaseModel):
    id: int
    password: str

class UpdatePWD(BaseModel):
    password: str

class ProfilePicture(BaseModel):
    profilPhoto: str

class BannerPicture(BaseModel):
    profilBannerPhoto: str

# !ARTIKEL
class Artikel(BaseModel):
    title: str
    isi: str

class UpdateThumbnailArtikel(BaseModel):
    thumbnail: str

class postArtikel(BaseModel):
    user_id:int
    title: str
    isi: str

#Tiket 
class tiketOrder(BaseModel):
    stasiun_asal: str
    stasiun_tujuan: str 

class beliTiket(BaseModel):
    user_id: int
    tiket_id: int
    tanggal: str