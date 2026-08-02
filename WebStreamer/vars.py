# (c) @EverythingSuckz | @AbirHasan2005

from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    API_ID = int(getenv("API_ID"))
    API_HASH = str(getenv("API_HASH"))
    BOT_TOKEN = str(getenv("BOT_TOKEN"))

    SESSION_NAME = str(getenv("SESSION_NAME", "AHFile2LinkBot"))
    SLEEP_THRESHOLD = int(getenv("SLEEP_THRESHOLD", "60"))
    WORKERS = int(getenv("WORKERS", "4"))

    BIN_CHANNEL = int(getenv("BIN_CHANNEL"))

    PORT = int(getenv("PORT", 8080))
    BIND_ADRESS = "0.0.0.0"
    FQDN = "0.0.0.0"

    OWNER_ID = int(getenv("OWNER_ID", "1445283714"))
    NO_PORT = bool(getenv("NO_PORT", False))

    ON_HEROKU = False
    APP_NAME = None

    DATABASE_URL = str(getenv("DATABASE_URL"))
    PING_INTERVAL = int(getenv("PING_INTERVAL", "500"))
    UPDATES_CHANNEL = str(getenv("UPDATES_CHANNEL", None))

    BANNED_CHANNELS = list(
        set(
            int(x)
            for x in str(
                getenv("BANNED_CHANNELS", "-1001362659779")
            ).split()
        )
    )
