from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email


engine = create_engine('sqlite:///contacts.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Context:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def create_record(self, name, phone, email):
        contact = Contact(name=name, phone=phone, email=email)
        session.add(contact)
        session.commit()

    def read_records(self):
        return session.query(Contact).all()

    def update_record(self, record_id, name, phone, email):
        contact = session.query(Contact).filter_by(id=record_id).first()
        contact.name = name
        contact.phone = phone
        contact.email = email
        session.commit()

    def delete_record(self, record_id):
        contact = session.query(Contact).filter_by(id=record_id).first()
        session.delete(contact)
        session.commit()

    #
    # def search_record(self, q):
    #     return session.query().filter(
    #         (Contact.name.like(f'%{q}%')) | (Contact.phone.like(f'%{q}%')) | (Contact.email.like(f'%{q}%'))
    #     ).all()

    def search_record(self, q):
        return session.query(Contact).filter(
            or_(
                Contact.name.ilike(f'%{q}%'),
                Contact.phone.ilike(f'%{q}%'),
                Contact.email.ilike(f'%{q}%')
            )
        ).all()
