# Koneksi database
from sqlalchemy import create_engine, MetaData

# engine = create_engine('mysql+pymysql://localhost:3360/myticket')
# dbURL = 'mysql+pymysql://root@127.0.0.1:3306/myticket'
dbURL = 'mysql+pymysql://sql12605397:V4AuiCYv8m@sql12.freesqldatabase.com:3306/sql12605397'
engine= create_engine(dbURL)
metaData = MetaData()
conn = engine.connect()