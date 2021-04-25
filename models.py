from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    myingredients = db.relationship('ingredient', backref='user', lazy=True) 

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }
    
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    
    def __repr__(self):
        return '<User {}>'.format(self.username)  

class ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255),nullable=False)
  userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
  have = db.Column(db.Boolean, nullable=False)

  def toDict(self):
   return {
     'id': self.id,
     'name': self.name,
     'userid': self.userid,
     'have': self.have
   }
