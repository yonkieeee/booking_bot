from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_nickname = Column(String)
    user_name = Column(String)
    user_surname = Column(String)
    user_age = Column(String)
    user_phone = Column(String)
    user_email = Column(String)


class DataBase:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def add_user(self, user_id, user_nickname, user_name, user_surname, user_age, user_phone, user_email):
        new_user = User(user_id=user_id,
                        user_nickname=user_nickname,
                        user_name=user_name,
                        user_surname=user_surname,
                        user_age=user_age,
                        user_phone=user_phone,
                        user_email=user_email)

        self.session.add(new_user)
        self.session.commit()

    def user_exists(self, user_id) -> bool:
        result = self.session.query(User).filter_by(user_id=user_id).first()

        return result is not None

    def get_user(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            return {
                'user_id': user.user_id,
                'user_nickname': user.user_nickname,
                'user_name': user.user_name,
                'user_surname': user.user_surname,
                'user_age': user.user_age,
                'user_phone': user.user_phone,
                'user_email': user.user_email
            }
        return None


