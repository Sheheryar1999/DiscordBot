import db

class Scam(db.Base):
    __tablename__ = 'scams'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    reason = db.Column(db.String(255))
    
    def __repr__(self):
        return '<Scam %r>' % self.user_id