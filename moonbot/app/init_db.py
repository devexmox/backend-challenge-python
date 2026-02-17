from sqlalchemy import create_engine

from moonbot.adapters.orm import Base
from moonbot.settings import settings


def main():
    engine = create_engine(settings.DB_URI)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
