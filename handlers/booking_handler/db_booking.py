from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Book_Reg(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    surname = Column(String)
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

    def add_book_reg(self, user_id, user_name, user_surname,
                     user_domivka, user_room, user_date, user_start_time, user_end_time, code_of_booking):
        new_booking = Book_Reg(user_id=user_id,
                               name=user_name,
                               surname=user_surname,
                               domivka=user_domivka,
                               room=user_room,
                               date=user_date,
                               start_time=user_start_time,
                               end_time=user_end_time,
                               code=code_of_booking)
        self.session.add(new_booking)
        self.session.commit()

        def get_domivka(self, user_id):
            domivkas = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

            return [record.domivka for record in domivkas]

        def get_room(self, user_id):
            rooms = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

            return [record.room for record in rooms]

        def get_date(self, user_id):
            dates = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

            return [record.date for record in dates]

        def get_start_time(self, user_id):
            start_times = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

            return [record.start_time for record in start_times]

        def get_end_time(self, user_id):
            end_times = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

            return [record.end_time for record in end_times]

        def get_code(self, user_id):
            codes = self.session.query(Book_Reg).filter_by(user_id=user_id).all()

            return [record.code for record in codes]

        def delete_booking(self, id_user, user_code):
            self.session.query(Book_Reg).filter_by(user_id=id_user, code=user_code).delete()
            self.session.commit()

