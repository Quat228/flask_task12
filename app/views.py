from flask import render_template, request, redirect, url_for, flash
from . import db
from . import models
from . import forms


def client_doctor():
    clients = models.Client.query.all()
    doctors = models.Doctor.query.all()
    return render_template("client_doctor.html", clients=clients, doctors=doctors)


def client_add():
    form = forms.ClientForm()
    if request.method == "POST":
        if form.validate_on_submit():
            client = models.Client()
            form.populate_obj(client)
            db.session.add(client)
            db.session.commit()
            flash("Клиент успешно сохранен", category="success")
            return redirect(url_for("client_doctor"))
        else:
            print(form.errors)
    return render_template("standart_form.html", form=form)


def doctor_add():
    form = forms.DoctorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            doctor = models.Doctor()
            form.populate_obj(doctor)
            db.session.add(doctor)
            db.session.commit()
            flash("Доктор успешно сохранен", category="success")
            return redirect(url_for("client_doctor"))
        else:
            print(form.errors)
    return render_template("standart_form.html", form=form)
