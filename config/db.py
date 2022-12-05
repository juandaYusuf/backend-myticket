# Koneksi database
from sqlalchemy import create_engine, MetaData

# engine = create_engine('mysql+pymysql://localhost:3360/myticket')
dbURL = 'mysql+pymysql://root@127.0.0.1:3306/myticket'
engine= create_engine(dbURL)
metaData = MetaData()
conn = engine.connect()