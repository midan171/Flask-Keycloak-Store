from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os
from model.item import ItemModel
from model.store import StoreModel
from split.extensions import db, ma

app = Flask(__name__,
    static_folder='../static',     
    template_folder='../templates' 
)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions with app
db.init_app(app)
ma.init_app(app)

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True

class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)
    class Meta:
        model = StoreModel
        load_instance = True
        
# Add this new function to check if database is empty
def is_database_empty():
    return StoreModel.query.count() == 0

@app.before_first_request
def create_tables():
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create new tables with updated schema

@app.route('/')
def index():
    return render_template('index.html')

# Modify init route to only add data if database is empty
@app.route("/api/init")
def init_data():
    # if not is_database_empty():
    #     return jsonify({"msg": "Database already initialized"})
    
    # Create stores
    stores = [
        StoreModel(name="Electronics Store"),
        StoreModel(name="Book Store"), 
        StoreModel(name="Sports Store"),
        StoreModel(name="Fashion Store")
    ]
    for store in stores:
        db.session.add(store)
    db.session.commit()

    # Create items for each store
    items = [
        ItemModel(name="Laptop", price=999.99, store_id=stores[0].id),
        ItemModel(name="Smartphone", price=599.99, store_id=stores[0].id),
        ItemModel(name="Novel", price=14.99, store_id=stores[1].id),
        ItemModel(name="Comic Book", price=9.99, store_id=stores[1].id),
        ItemModel(name="Football", price=29.99, store_id=stores[2].id),
        ItemModel(name="Tennis Racket", price=89.99, store_id=stores[2].id),
        ItemModel(name="T-Shirt", price=19.99, store_id=stores[3].id),
        ItemModel(name="Jeans", price=49.99, store_id=stores[3].id)
    ]
    for item in items:
        db.session.add(item)
    db.session.commit()
    
    return jsonify({"msg": "Dummy data added to database"})

@app.route("/api/check")
def check_data():
    store = StoreModel.query.first()
    store_schema = StoreSchema()
    output = store_schema.dump(store)
    return jsonify({"store": output})

@app.route("/api/store")
def get_store():
    store = StoreModel.query.first()
    store_schema = StoreSchema()
    output = store_schema.dump(store)
    data = store_schema.load(output)
    return jsonify({"store": output})

@app.route("/api/items")
def get_items():
    items = ItemModel.query.all()
    schema = ItemSchema(many=True)
    output = schema.dump(items)
    return jsonify({"items": output})

@app.route("/api/stores")
def get_all_stores():
    stores = StoreModel.query.all()
    store_schema = StoreSchema(many=True)
    output = store_schema.dump(stores)
    return jsonify({"stores": output})

@app.route('/stores')
def stores_page():
    return render_template('stores.html')

@app.route('/items')
def items_page():
    return render_template('items.html')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')

