import pynecone as pc

class MemorymatchConfig(pc.Config):
    pass

config = MemorymatchConfig(
    app_name="memory_match",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)