from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

def write_to_csv(data):
    with open("cafe-data.csv", "a", encoding="utf-8") as csv:
        csv.write(data)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30 PM', validators=[DataRequired()])   
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", 
                                "☕️☕️☕️☕️☕️"])
    wifi_strength_rating = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=["✘", "💪", "💪💪", "💪💪💪", 
                                       "💪💪💪💪", "💪💪💪💪💪"])
    power_socket_availability = SelectField('Power Socket Availability', validators=[DataRequired()], choices=["✘", "🔌", "🔌🔌",
                                            "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    cafe_form = CafeForm()

    cafe_form.validate_on_submit()

    if cafe_form.validate_on_submit():
        print("True")
        cafe = cafe_form.cafe.data
        location = cafe_form.location.data
        location = location.replace(",", '","')
        opening_time = cafe_form.opening_time.data
        closing_time = cafe_form.closing_time.data
        coffee_rating = cafe_form.coffee_rating.data
        wifi_strength_rating = cafe_form.wifi_strength_rating.data
        power_socket_availability = cafe_form.power_socket_availability.data

        csv_string = f"\n{cafe},'{location}',{opening_time},{closing_time},{coffee_rating},{wifi_strength_rating},{power_socket_availability} "
        
        write_to_csv(csv_string)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=cafe_form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
