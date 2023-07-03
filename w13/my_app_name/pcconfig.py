import pynecone as pc

class MyappnameConfig(pc.Config):
    pass

config = MyappnameConfig(
    app_name="my_app_name",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)