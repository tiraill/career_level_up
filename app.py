import os
from flask import (
    Flask, render_template, redirect, url_for
)
from flask_bootstrap import Bootstrap
from requests import post, RequestException
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


app = Flask(__name__)
Bootstrap(app)

app.config.update(dict(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    WTF_CSRF_SECRET_KEY=os.getenv('WTF_CSRF_SECRET_KEY')
))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CallBackForm()
    if form.validate_on_submit():
        notification(f'Новая заявка: {form.name.data}\n{form.phonenumber.data}')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


def notification(message: str) -> None:
    try:
        response = post(URL, data={'chat_id': CHAT_ID, 'text': message})
    except RequestException as exc:
        print(f'Send message error: {exc}')
    else:
        print(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


class CallBackForm(FlaskForm):
    name = StringField('First Name', [validators.DataRequired()])
    phonenumber = StringField('Phone Number', [validators.DataRequired()])
    submit = SubmitField('Записаться на консультацию')
