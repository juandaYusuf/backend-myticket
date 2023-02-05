# Request Method
from fastapi import APIRouter, UploadFile, File
import secrets
from PIL import Image
from models.tabel import users, artikels, tiket, pembelian, saldo_user, topup_user, like_artikels, comment_artikels
from config.db import conn
from schema.schemas import User, LoginData, CheckCurrentPWD, UpdatePWD, ProfilePicture, BannerPicture, Artikel, UpdateThumbnailArtikel, postArtikel, tiketOrder, beliTiket, answerChecker, sendComment, editComment


router = APIRouter()

#! USER  ==============================================================================
@router.get('/')
async def fetchAllUserData():
    return conn.execute(users.select()).fetchall()

@router.get('/profile/{id}')
async def profile(id: int):
    return conn.execute(users.select().where(users.c.id == id)).first()

# *Upload File
@router.post('/image/')
async def profileimage(image: UploadFile =File(...)):
    FILEPATH = "./static/images/"
    fileName = image.filename
    extensions = fileName.split(".")[1]
    if extensions not in ['png', 'jpg', 'jpeg']:
        return {
            "status": "error",
            "detail": "file extension is not allowed"
            }
    token_name = secrets.token_hex(10)+"."+extensions
    generated_name = FILEPATH + token_name
    file_content = await image.read()

    #* simpan ke direktory
    with open(generated_name, "wb") as f:
        f.write(file_content)

    #* PILLOW. berfungsi untuk mengeksekusi gambar bisa juga untuk resize gambar
    img = Image.open(generated_name)
    img.save(generated_name)
    await image.close()
    
    file_url = 'http://127.0.0.1:8000'+generated_name[1:]
    return {"status":"uploaded" ,"url":file_url}


@router.post('/login/')
async def login(data: LoginData):
    response = conn.execute(users.select().where(users.c.email == data.email, users.c.password == data.password ))
    if (response):
        return response.first()

@router.post('/register/')
async def register(user: User):
    conn.execute(users.insert().values(fullname = user.fullname,email  = user.email,alamat = user.alamat,noTelepon = user.noTelepon,password = user.password,jenisKelamin = user.jenisKelamin))
    return conn.execute(users.select()).fetchall()


@router.put('/update/{id}')
async def updateUserData(id: int, user: User):
    conn.execute(users.update().values(fullname = user.fullname,email  = user.email,alamat = user.alamat,noTelepon = user.noTelepon,password = user.password,jenisKelamin = user.jenisKelamin).where(users.c.id == id))
    return conn.execute(users.select()).fetchall()

@router.post('/checkcurrentpassword/')
async def checkCurrentPassword(pwdByID:CheckCurrentPWD):
    response = conn.execute(users.select().where(users.c.id == pwdByID.id, users.c.password == pwdByID.password ))
    if response:
        return response.first()


@router.put('/changepassword/{id}')
async def updatePassword(id: int, pwd: UpdatePWD):
    response = conn.execute(users.update().values(password =  pwd.password).where(users.c.id == id))
    if(response):
        return conn.execute(users.select().where(users.c.id == id)).first()

# *Update profile picture
@router.put('/profile_picture/{id}')
async def profilePicture(id: int, picture: ProfilePicture):
    response = conn.execute(users.update().values(profilPhoto = picture.profilPhoto).where(users.c.id == id))
    if(response):
        return conn.execute(users.select().where(users.c.id == id)).first()

# *Update profile picture
@router.put('/banner_picture/{id}')
async def bannerPicture(id: int, picture: BannerPicture):
    response = conn.execute(users.update().values(profilBannerPhoto = picture.profilBannerPhoto).where(users.c.id == id))
    if(response):
        return conn.execute(users.select().where(users.c.id == id)).first()

@router.delete('/{id}')
async def deleteUserData(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select()).fetchall()

# !ARTIKEL  ==============================================================================
@router.get('/artikelall/')
async def fetchAllArtikel():
    return conn.execute(artikels.select()).fetchall()

@router.get('/artikel-comment/{id}')
async def fetchAllArtikel(id : int):
    return conn.execute(artikels.select().where(artikels.c.id == id)).first()


@router.get('/artikel_of_user/{idOfUser}')
async def artikelOfUser(idOfUser: int):
    return conn.execute(artikels.select().where(artikels.c.user_id == idOfUser)).fetchall()

@router.put('/update_artikel/{id}/{idOfUser}')
async def updateArtikel(id:int, idOfUser: int, update: Artikel):
    response = conn.execute(artikels.update().values(title = update.title, isi  = update.isi,).where(artikels.c.id == id, artikels.c.user_id == idOfUser))
    if(response):
        return conn.execute(artikels.select().where(artikels.c.id == id)).first()

@router.put('/update_thumbnail_artikel/{id}/{idOfUser}')
async def updateThumbnail(id: int, idOfUser: int, image: UpdateThumbnailArtikel):
    response = conn.execute(artikels.update().values(thumbnail = image.thumbnail,).where(artikels.c.id == id, artikels.c.user_id == idOfUser))
    if(response):
        return conn.execute(artikels.select().where(artikels.c.id == id)).first()

@router.post('/post_artikel/{idOfUser}')
async def uploadArtikel(idOfUser: int, data: postArtikel):
    response = conn.execute(artikels.insert().values( user_id = idOfUser, title= data.title, isi= data.isi,))
    if response:
        return conn.execute(artikels.select().order_by(artikels.c.id.desc())).first()

@router.delete('/delete_artikel/{id}/{idOfUser}')
async def deleteArtikel(id: int, idOfUser: int):
    conn.execute(artikels.delete().where(artikels.c.id == id, artikels.c.user_id == idOfUser))
    return conn.execute(artikels.select().where(artikels.c.user_id == idOfUser)).fetchall()

# !tiket  ==============================================================================
@router.post('/order_tiket/')
async def orderTiket(tiketOrder: tiketOrder):
    response = conn.execute(tiket.select().where(tiket.c.stasiun_asal == tiketOrder.stasiun_asal, tiket.c.stasiun_tujuan == tiketOrder.stasiun_tujuan)).first()
    return response

@router.get('/bought_tiket/{tiketID}')
async def boughtTiket(tiketID: int):
    response = conn.execute(tiket.select().where(tiket.c.id == tiketID)).fetchall()
    return response

@router.get('/show_tiket/')
async def showTiket():
    return conn.execute(tiket.select()).fetchall()

# !pembelian  ==============================================================================
@router.post('/pembelian_tiket/')
async def buyTiket(dataPembeli: beliTiket):
    response = conn.execute(pembelian.insert().values( user_id = dataPembeli.user_id, tiket_id = dataPembeli.tiket_id, tanggal= dataPembeli.tanggal ))
    return conn.execute(pembelian.select().where(pembelian.c.user_id == dataPembeli.user_id)).fetchall()

@router.get('/tiket_saya/{userID}')
async def tiketSaya(userID: int):
    response = conn.execute(pembelian.select().where(pembelian.c.user_id == userID)).fetchall()
    return response

# !Saldo user ==============================================================================
@router.get('/saldo/')
async def chekUserSaldo(userID: int):
    return conn.execute(saldo_user.select().where(saldo_user.c.user_id == userID)).first()

@router.post('/topup/{userID}/{nominalSaldo}')
async def  topup( userID: int, nominalSaldo: int):
    checkAvailabilityUser = conn.execute(saldo_user.select().where(saldo_user.c.user_id == userID)).fetchall()
    if not checkAvailabilityUser :
        conn.execute(saldo_user.insert().values(user_id = userID, saldo = nominalSaldo))
    else:
        conn.execute(saldo_user.update().values(user_id = userID, saldo = nominalSaldo).where(saldo_user.c.user_id == userID))
    return conn.execute(saldo_user.select().where(saldo_user.c.user_id == userID)).fetchall()

# Topup dengan soal pertanyaan
@router.get('/questions-for-topup/')
async def questionsForTopUp():
    return conn.execute(topup_user.select()).fetchall()

@router.post('/questions-for-topup/answer-checker')
async def checkAnswer(data: answerChecker):
    response = conn.execute(topup_user.select().where(topup_user.c.soal == data.soal, topup_user.c.correct_answer == data.correct_answer)).first()
    if not response :
        return "incorrect"
    else:
        return "correct"

# !Like artikel (sukai artikel)
@router.get('/total-like-artikel/{artikelID}')
async def totalLikesArtikel(artikelID: int):
    response = conn.execute(like_artikels.select().where(like_artikels.c.artikel_id == artikelID, like_artikels.c.deskripsi == "like")).fetchall()
    return len(response)

@router.get('/show-artikel-like/{userID}/{artikelID}')
async def showLikerOfArtikels(userID: int, artikelID: int):
    response = conn.execute(like_artikels.select().where(like_artikels.c.user_id == userID, like_artikels.c.artikel_id == artikelID)).first()
    if not response :
        return 'this user likes it yet'
    else :
        return response 

@router.post('/like-artikel/{userID}/{artikelID}/')
async def usersLikeArticles(userID: int, artikelID: int):
    response = conn.execute(like_artikels.select().where(like_artikels.c.user_id == userID, like_artikels.c.artikel_id == artikelID)).first()
    if response :
        if response.deskripsi == 'like' :
            conn.execute(like_artikels.update().values( deskripsi = "unlike").where(like_artikels.c.artikel_id == artikelID, like_artikels.c.user_id == userID))
        elif response.deskripsi == 'unlike' :
            conn.execute(like_artikels.update().values( deskripsi = "like").where(like_artikels.c.artikel_id == artikelID, like_artikels.c.user_id == userID))
    else :
        conn.execute(like_artikels.insert().values( user_id = userID, artikel_id = artikelID, deskripsi = "like"))
    return conn.execute(like_artikels.select().where(like_artikels.c.user_id == userID, like_artikels.c.artikel_id == artikelID)).first()

# !Komentar Artikel
@router.get('/total-comment-artikel/{artikelID}')
async def totalCommentArtikel(artikelID: int):
    response = conn.execute(comment_artikels.select().where(comment_artikels.c.artikels_id == artikelID)).fetchall()
    return len(response)

@router.get('/show-artikel-comment/{userID}/{artikelID}')
async def showLikerOfArtikels(userID: int, artikelID: int):
    response = conn.execute(comment_artikels.select().where(comment_artikels.c.user_id == userID, comment_artikels.c.artikels_id == artikelID)).first()
    if not response :
        return 'this user comment it yet'
    else :
        return response 

@router.get('/comment-public/{artikelID}') #Menampilkan seluruh komentar per-artikel
async def showAllCommentOfArtikel(artikelID: int):
    return conn.execute(comment_artikels.select().where(comment_artikels.c.artikels_id == artikelID)).fetchall()

@router.post('/send-comment-public/')
async def sendComment(commentData : sendComment):
    conn.execute(comment_artikels.insert().values(user_id = commentData.user_id, artikels_id = commentData.artikels_id, content = commentData.content ))
    return conn.execute(comment_artikels.select().where(comment_artikels.c.artikels_id == commentData.artikels_id)).fetchall()

@router.put('/edit-comment-public/')
async def editComment(commentData : editComment):
    conn.execute(comment_artikels.update().values(content = commentData.content ).where(comment_artikels.c.id == commentData.id, comment_artikels.c.user_id == commentData.user_id, comment_artikels.c.artikels_id == commentData.artikels_id))
    return conn.execute(comment_artikels.select().where(comment_artikels.c.id == commentData.id, comment_artikels.c.user_id == commentData.user_id, comment_artikels.c.artikels_id == commentData.artikels_id)).first()

@router.delete('/delet-comment-public/{id}')
async def deletCommentPublic(id: int):
    conn.execute(comment_artikels.delete().where(comment_artikels.c.id == id))
    response = conn.execute(comment_artikels.select().where(comment_artikels.c.id == id)).first()
    if not response :
        return 'comment has been deleted'
    else :
        return 'failed to delete comment'