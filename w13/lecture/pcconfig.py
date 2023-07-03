import pynecone as pc

class LectureConfig(pc.Config):
    pass

config = LectureConfig(
    app_name="lecture",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)