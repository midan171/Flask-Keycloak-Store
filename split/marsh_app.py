from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS  # Add CORS support

app = Flask(__name__,
    static_folder='../static',     # Point to static folder
    template_folder='../templates' # Point to templates folder
)
CORS(app)  # Enable CORS

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Marsh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    rewards = db.relationship("Reward", backref="reward_marsh")

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(50))
    marsh_id = db.Column(db.Integer, db.ForeignKey("marsh.id"))
    

class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward
        load_instance = True

class MarshSchema(ma.SQLAlchemyAutoSchema):
    rewards = ma.Nested(RewardSchema,many=True)
    class Meta:
        model = Marsh
        load_instance = True
        

# Add this new function to check if database is empty
def is_database_empty():
    return Marsh.query.count() == 0

@app.before_first_request
def create_tables():
    db.create_all()  # Only create tables if they don't exist

@app.route('/')
def index():
    return render_template('index.html')

# Modify init route to only add data if database is empty
@app.route("/api/init")
def init_data():
    if not is_database_empty():
        return jsonify({"msg": "Database already initialized"})
    
    # Create stores
    stores = [
        Marsh(name="Electronics Store"),
        Marsh(name="Book Store"),
        Marsh(name="Sports Store"),
        Marsh(name="Fashion Store")
    ]
    for store in stores:
        db.session.add(store)
    db.session.commit()

    # Create rewards/items for each store
    rewards = [
        Reward(reward_name="Laptop", reward_marsh=stores[0]),
        Reward(reward_name="Smartphone", reward_marsh=stores[0]),
        Reward(reward_name="Novel", reward_marsh=stores[1]),
        Reward(reward_name="Comic Book", reward_marsh=stores[1]),
        Reward(reward_name="Football", reward_marsh=stores[2]),
        Reward(reward_name="Tennis Racket", reward_marsh=stores[2]),
        Reward(reward_name="T-Shirt", reward_marsh=stores[3]),
        Reward(reward_name="Jeans", reward_marsh=stores[3])
    ]
    for reward in rewards:
        db.session.add(reward)
    db.session.commit()
    
    return jsonify({"msg": "Dummy data added to database"})

@app.route("/api/check")
def check_data():
    users = Marsh.query.first()
    marsh_schema = MarshSchema()
    output = marsh_schema.dump(users)
    return jsonify({"user": output})

@app.route("/api/user")
def get_user():
    users = Marsh.query.first()
    marsh_schema = MarshSchema()
    output = marsh_schema.dump(users)
    data = marsh_schema.load(output)
    return jsonify({"user": output})

@app.route("/api/rewards")
def get_rewards():
    rewards = Reward.query.all()
    schema = RewardSchema(many=True)
    output = schema.dump(rewards)
    return jsonify({"rewards": output})

@app.route("/api/users")
def get_all_users():
    users = Marsh.query.all()
    marsh_schema = MarshSchema(many=True)
    output = marsh_schema.dump(users)
    return jsonify({"users": output})

@app.route('/stores')
def stores_page():
    return render_template('stores.html')

@app.route('/items')
def items_page():
    return render_template('items.html')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')

