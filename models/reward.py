from split.extensions import db

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(50))
    marsh_id = db.Column(db.Integer, db.ForeignKey("marsh.id")) 