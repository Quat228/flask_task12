from . import app
from . import views

app.add_url_rule("/", view_func=views.client_doctor)
app.add_url_rule("/client/add", view_func=views.client_add, methods=["GET", "POST"])
app.add_url_rule("/doctor/add", view_func=views.doctor_add, methods=["GET", "POST"])
