from . import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    birth_date = db.Column(db.String)
    inn = db.Column(db.String)
    gender = db.Column(db.String)
    phone = db.Column(db.Integer)
    address = db.Column(db.String)
    application_date = db.Column(db.String)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    birth_date = db.Column(db.String)
    specialty = db.Column(db.String)
    experience = db.Column(db.Integer)


class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", backref=db.backref("histories", lazy="dynamic"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    doctor = db.relationship("Doctor", backref=db.backref("histories", lazy="dynamic"))
