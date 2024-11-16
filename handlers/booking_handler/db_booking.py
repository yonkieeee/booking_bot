from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class BookReg(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(55), nullable=False)
    name = Column(String(50))
    surname = Column(String(50))
    domivka = Column(String(50))
    room = Column(String(50))
    date = Column(String(50))
    start_time = Column(String(50))
    end_time = Column(String(50))
    code = Column(String(50))  # код бронювання який є унікальний для кожного бронювання


class BookingDataBase:
    def __init__(self, db_file):
        self.engine = create_engine("postgresql://plast_admin:bs&P71q4to;?@localhost:5432/plast_db",
                                    pool_recycle=3600, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)

    def add_book_reg(self, user_id, user_name, user_surname,
                     user_domivka, user_room, user_date, user_start_time, user_end_time, code_of_booking):
        with sessionmaker(bind=self.engine)() as session:
            new_booking = BookReg(user_id=str(user_id),
                                  name=user_name,
                                  surname=user_surname,
                                  domivka=user_domivka,
                                  room=user_room,
                                  date=user_date,
                                  start_time=user_start_time,
                                  end_time=user_end_time,
                                  code=code_of_booking)
            session.add(new_booking)
            session.commit()
            session.close()

    def get_all_data(self, user_id):
        with sessionmaker(bind=self.engine)() as session:
            records = session.query(BookReg).filter_by(user_id=user_id).all()
            session.close()
            return [
                {
                    "domivka": record.domivka,
                    "room": record.room,
                    "date": record.date,
                    "start_time": record.start_time,
                    "end_time": record.end_time,
                    "code": record.code
                }
                for record in records
            ]


    def delete_booking(self, id_user, user_code):
        with sessionmaker(bind=self.engine)() as session:
            session.query(BookReg).filter_by(user_id=id_user, code=user_code).delete()
            session.commit()
            session.close()

    def get_domivka(self, code):
        with sessionmaker(bind=self.engine)() as session:
            record = session.query(BookReg).filter_by(code=code).first()
            session.close()
            if record:
                return record.domivka
            else:
                return None


