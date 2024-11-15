from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(55), nullable=False)
    user_nickname = Column(String(50))
    user_name = Column(String(50))
    user_surname = Column(String(50))
    user_age = Column(String(50))
    user_phone = Column(String(50))


class DataBase:
    def __init__(self, db_file):
        self.engine = create_engine("postgresql://plast_admin:bs&P71q4to;?@localhost:5432/plast_db",
                                    pool_recycle=3600, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)

    def add_user(self, user_id, user_nickname, user_name, user_surname, user_age, user_phone):
        with sessionmaker(bind=self.engine)() as session:
            new_user = User(user_id=user_id,
                            user_nickname=user_nickname,
                            user_name=user_name,
                            user_surname=user_surname,
                            user_age=user_age,
                            user_phone=user_phone)

            session.add(new_user)
            session.commit()
            session.close()

    def user_exists(self, user_id) -> bool:
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(User).filter_by(user_id=user_id).first()
            session.close()
        return result is not None

    def get_user(self, user_id):
        with sessionmaker(bind=self.engine)() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            session.close()
            if user:
                return {
                    'user_id': user.user_id,
                    'user_nickname': user.user_nickname,
                    'user_name': user.user_name,
                    'user_surname': user.user_surname,
                    'user_age': user.user_age,
                    'user_phone': user.user_phone
                }
            return None

    def user_delete(self, user_id):
        with sessionmaker(bind=self.engine)() as session:
            session.query(User).filter_by(user_id=user_id).delete()
            session.commit()
            session.close()
