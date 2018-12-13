from app import db

class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    image_url = db.Column(db.String(1024))

    def import_data(self, data):
        self.name = data['name']
        self.image_url = data['image_url']

    def export_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url
        }

class Album(db.Model):
    __tablename__ = "album"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    image_url = db.Column(db.String(1024))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), index=True)

    def import_data(self, data):
        self.name = data['name']
        self.image_url = data['image_url']
        self.artist_id = data['artist_id']

    def export_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "artist_id": self.artist_id
        }

class Song(db.Model):
    __tablename__ = "song"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), index=True)

    stream_url = db.Column(db.String(1024))

    def import_data(self, data):
        self.name = data['name']
        self.album_id = data['album_id']
        self.stream_url = data['stream_url']

    def export_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "album_id": self.album_id,
            "stream_url": self.stream_url
        }

    def export_data(self, flag):
        return {
            "id": self.id,
            "name": self.name,
            "album_id": self.album_id,
            "stream_url": self.stream_url,
            "added": flag
        }
