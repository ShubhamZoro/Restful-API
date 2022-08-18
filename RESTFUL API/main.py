from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

@app.route("/")
def home():
    return render_template("index.html")

    ## HTTP GET - Read Record



@app.route("/random")
def get_random_cafe():
    # cafes = Cafe.query.all()
    # random_cafe = random.choice(cafes)
    # return jsonify(cafe={
    #     "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # })
    cafes =Cafe.query.all()
    random_cafe = random.choice(cafes)
    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafe=random_cafe.to_dict())

@app.route('/random_all')
def get_all():
    cafes = db.session.query(Cafe).all()

    return jsonify(cafe=[cafe.to_dict() for cafe in cafes])

@app.route('/search')
def search():
    location = request.args.get("loc")
    cafes=Cafe.query.filter_by(location=location).first()
    if cafes:
        return jsonify(cafe=cafes.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})

## HTTP POST - Create Record
@app.route('/add',methods=["POST"])
def add():
    add_cafe=Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(add_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record
@app.route("/update/<int:id>",methods=["PATCH"])
def update(id):
    price = Cafe.query.get(id)
    if price:

        coffee_price = request.args.get("new_price")
        price.coffee_price = coffee_price
        db.session.commit()
        return jsonify(response={"success":"Successfully Updated"})
    else:
        return jsonify(resposne={"Not_Found":"Id not found"})
## HTTP DELETE - Delete Record
@app.route('/delete/<int:id>',methods=["DELETE"])
def delete(id):
    api_key=request.args.get("api-key")
    cafe=Cafe.query.get(id)
    if api_key=="TopSecretApiKey" and cafe:
        Cafe.query.filter_by(id=id).delete()
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted"})
    else:
        return jsonify(response={"KeyError": "Enter correct key or check id"})


if __name__ == '__main__':
    app.run(debug=True)
