from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Book_Reg(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    surname = Column(String)
    name_of_booking = Column(String)
    domivka = Column(String)
    room = Column(String)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    code = Column(String)#код бронювання який є унікальний для кожного бронювання


class Booking_DataBase:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def add_book_reg(self, user_id, user_name, user_surname, user_name_of_booking,
                     user_domivka, user_room, user_date, user_start_time, user_end_time, code_of_booking):
        new_booking = Book_Reg(user_id=user_id,
                               name=user_name,
                               surname=user_surname,
                               name_of_booking = user_name_of_booking,
                               domivka=user_domivka,
                               room=user_room,
                               date=user_date,
                               start_time=user_start_time,
                               end_time=user_end_time,
                               code=code_of_booking)
        self.session.add(new_booking)
        self.session.commit()

    def get_all_data(self, user_id):
        records = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

        return [
            {
                "name_of_booking": record.name_of_booking,
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
        self.session.query(Book_Reg).filter_by(user_id=id_user, code=user_code).delete()
        self.session.commit()
        
    def get_domivka(self, code):
        record = self.session.query(Book_Reg).filter_by(code=code).first()
        if record:
            return record.domivka
        else:
            return None

        
