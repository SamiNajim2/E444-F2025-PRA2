from flask import Flask, render_template, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_moment import Moment

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"  # OK for classwork
moment = Moment(app)  # keep Moment available for base.html (Activity 1.3)

# ----- Forms -----
class NameEmailForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("What is your UofT Email address?", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

# ----- Routes -----
@app.route("/", methods=["GET", "POST"])
def index():
    form = NameEmailForm()

    # previous values (if any) — used for the "changed" notices
    prev_name = session.get("name")
    prev_email = session.get("email")

    if form.validate_on_submit():
        new_name = form.name.data.strip()
        new_email = form.email.data.strip()

        # "changed" alerts like the handout
        if prev_name and new_name != prev_name:
            flash("Looks like you have changed your name!")
        if prev_email and new_email != prev_email:
            flash("Looks like you have changed your email!")

        # save to session
        session["name"] = new_name
        session["email"] = new_email

        # UofT check: email must contain "utoronto"
        is_uoft = "utoronto" in new_email.lower()

        return render_template(
            "index.html",
            form=form,
            name=new_name,
            email=new_email,
            valid=is_uoft,
        )

    # initial GET or when validation errors exist
    return render_template(
        "index.html",
        form=form,
        name=prev_name,
        email=prev_email,
    )

if __name__ == "__main__":
    app.run(debug=True)
