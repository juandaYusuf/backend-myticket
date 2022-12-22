# Membuat tabel database
from sqlalchemy import DateTime, ForeignKey, Integer, String, Table, Column, Time
from config.db import engine, metaData 

users = Table(
    'users',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('fullname', String(50)),
    Column('email', String(30)),
    Column('alamat', String(255)),
    Column('noTelepon', String(20)),
    Column('password', String(100)),
    Column('jenisKelamin', String(10)),
    Column('profilPhoto', String(255)),
    Column('profilBannerPhoto', String(255))
    )


artikels = Table(
    'artikels',
    metaData,
    Column('id', Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column('title', String(100)),
    Column('isi', String(10000)),
    Column('thumbnail', String(255)),
    )


tiket = Table(
    'tiket',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('nama_kereta', String(50)),
    Column('jumlah_gerbong', Integer),
    Column('kelas', String(20)),
    Column('harga', Integer),
    Column('stasiun_asal', String(100)),
    Column('stasiun_tujuan', String(100)),
    Column('waktu_keberangkatan', Time),
    Column('waktu_tiba', Time),
)

pembelian = Table(
    'pembelian',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("users.id"), nullable=False),
    Column('tiket_id', Integer, ForeignKey("tiket.id"), nullable=False),
    Column('tanggal', DateTime),
)

saldo_user = Table(
    'saldo_user',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("users.id"), nullable=False),
    Column('saldo', Integer)
)


metaData.create_all(engine)