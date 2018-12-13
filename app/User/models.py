from sqlalchemy import PrimaryKeyConstraint

from app import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(512))
    image_url = db.Column(db.String(1024))

    def import_data(self, data):
        self.name = data['name']
        self.email = data['email']
        self.image_url = data['image_url']

    def export_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "image_url": self.image_url
        }

class User_Song(db.Model):
    __tablename__ = "user_song"

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __table_args__ = (
        PrimaryKeyConstraint('song_id', 'user_id'),
        {}
    )

    def import_data(self, data):
        self.song_id = data['song_id']
        self.user_id = data['user_id']

    def export_data(self):
        return {
            "song_id": self.song_id,
            "user_id": self.user_id
        }
