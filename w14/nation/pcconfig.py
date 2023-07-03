import pynecone as pc
import pymysql
pymysql.install_as_MySQLdb()

#class NationConfig(pc.Config):
#    pass

config = pc.Config(
    app_name="nation",
    db_url='mysql+mysqldb://root:qwer@172.17.0.1:3306/nation',
    env=pc.Env.DEV,
)
