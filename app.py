from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import EmailField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["ADMIN_MAIL"] = os.environ.get("ADMIN_MAIL")
mail = Mail(app)


class FeedBackForm(FlaskForm):
    mail = EmailField('Email', validators=[DataRequired(), Length(1, 64)])
    name = StringField('Имя', validators=[DataRequired(), Length(1, 64)])
    text = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Send')

def send_email(form):
    msg = Message(f"[Чиним Тачки] Вопрос от {form['name']}", sender=app.config["MAIL_USERNAME"], recipients=[app.config["ADMIN_MAIL"]])
    msg.body = f"Почта: {form['mail']}\n Сообщение: {form['text']}"
    msg.html = f"<h1>Почта: {form['mail']}</h1> <h2>Сообщение: {form['text']}</h2>"
    mail.send(msg)
    return True


@app.route("/", methods=['GET'])
def main():
    return render_template("index.html")

@app.route("/prices", methods=['GET'])
def prices():
    return render_template("prices.html")

@app.route("/sitemap", methods=['GET'])
def sitemap():
    return render_template("sitemap.html")

@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedBackForm(request.form)
    if form.validate_on_submit():
        if send_email(request.form):
            flash("Сообщение отправлено")
        else:
            flash("Произошла ошибка при отправке сообщения")
            return redirect(url_for('feedback'))
    return render_template("feedback.html", form=form)


if __name__ == "__main__":
    app.run()
