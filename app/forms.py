import datetime

import wtforms as wf
from flask_wtf import FlaskForm
from .models import Client, Doctor
from datetime import date, datetime


def get_client_choices():
    clients = Client.query.all()
    choices = []
    for client in clients:
        choices.append((client.id, client.fullname))
    return choices


def get_doctor_choices():
    doctors = Doctor.query.all()
    choices = []
    for doctor in doctors:
        choices.append((doctor.id, doctor.fullname))
    return choices


def check_name_validator(form, field):
    for letter in field.data:
        if letter not in "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ":
            raise wf.ValidationError("Имя должно быть только из кириллицы")


class ClientForm(FlaskForm):
    fullname = wf.StringField(label="ФИО", validators=[
        check_name_validator,
        wf.validators.DataRequired()
    ])
    birth_date = wf.DateField(label="Дата рождения")
    inn = wf.StringField(label="ИНН", validators=[
        wf.validators.Length(min=16, max=16),
        wf.validators.DataRequired()
    ])
    gender = wf.StringField(label="Пол", validators=[
        wf.validators.DataRequired()
    ])
    phone = wf.StringField(label="Номер телефона", validators=[
        wf.validators.Length(min=13, max=13),
        wf.validators.DataRequired()
    ])
    address = wf.StringField(label="Адрес проживания", validators=[
        wf.validators.DataRequired()
    ])
    application_date = wf.DateField(label="Дата обращения", validators=[
        wf.validators.DataRequired()
    ])

    def get_age(self):
        try:
            age = date.today() - self.birth_date.data
            return age.days / 365
        except Exception:
            raise wf.ValidationError("Недопустымый год")

    def validate_birth_date(self, field):
        age = self.get_age()

        if age < 18:
            raise wf.ValidationError("Пациент должен быть старше 18")

    def validate_inn(self, field):
        if not field.data.isdigit():
            raise wf.ValidationError("Инн должен быть только из чисел")

    def validate_phone(self, field):
        if field.data[0] != "+":
            raise wf.ValidationError("Должно начинаться с +")

    def validate_address(self, field):
        print("hi")
        for letter in field.data:
            print(letter)
            if not letter.isdigit():
                print("isdigit")
                if not letter.isalpha():
                    print("isalpha")
                    if letter != " ":
                        if letter not in ["-", "«", "»", '"', "'", "/", ","]:
                            print(letter)
                            raise wf.ValidationError("В адресе могут только буквы,"
                                                     " цифры, тире(-), ковычки(«») и слеш(/) и ЗАПЯТЫЕ (,)")

    def validate_application_date(self, field):
        if field.data > date.today():
            raise wf.ValidationError("Дата обращения не может быть позже чем сегодняшний день")


class DoctorForm(FlaskForm):
    fullname = wf.StringField(label="ФИО", validators=[
        check_name_validator,
        wf.validators.DataRequired()
    ])
    birth_date = wf.DateField(label="Дата рождения", validators=[
        wf.validators.DataRequired()
    ])
    specialty = wf.StringField(label="Специальность", validators=[
        wf.validators.DataRequired()
    ])
    experience = wf.IntegerField(label="Стаж", validators=[
        wf.validators.DataRequired()
    ])

    def get_age(self):
        try:
            age = date.today() - self.birth_date.data
            return age.days / 365
        except Exception:
            raise wf.ValidationError("Недопустымый год")

    def validate_birth_date(self, field):
        age = self.get_age()
        if age < 25:
            raise wf.ValidationError("Вы должны быть 25 или старше")

    def validate_experience(self, field):
        age = self.get_age()
        if age - 25 < self.experience.data:
            raise wf.ValidationError("Стаж врача не может быть больше (возраст – 25лет)")

    def validate_specialty(self, field):
        for letter in field.data:
            if not letter.isalpha() and letter != " ":
                print(letter)
                if not letter == "-":
                    print(letter)
                    raise wf.ValidationError("Специальность может быть только из букв, и –(тире)")


class MedicalHistoryForm(FlaskForm):
    client = wf.SelectField(label="ФИО клиента", choices=[])
    doctor = wf.SelectField(label="ФИО врача", choices=[])
    diagnosis = wf.StringField(label="Диагноз")

    def __init__(self):
        self.client.choices = get_client_choices()
        self.doctor.choices = get_doctor_choices()
