from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

DataBase = config.DataBase

db_name = DataBase.db_name
username = DataBase.username
password = DataBase.password
port = DataBase.port
host = DataBase.host

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}",
                       echo=True, convert_unicode=True)

# db_session 은 engine 객체를 사용해서 연결,
# 세션을 관리할 scoped_session class가 sessionmaker 인스턴스를 받음
db_session = scoped_session(sessionmaker(autocommit=False,  # 오토커밋
                                         autoflush=False,  # 쿼리를 바로 실행할 것인지
                                         bind=engine))  # 사용할 DB 엔진
Base = declarative_base()  # Table 클래스가 상속할 기본 모델 클래스


# Base.query = db_session.query_property()


def init_db():
    import db
    Base.metadata.create_all(bind=engine)
