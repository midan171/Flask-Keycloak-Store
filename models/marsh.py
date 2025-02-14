from split.extensions import db

class Marsh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    rewards = db.relationship("Reward", backref="reward_marsh")