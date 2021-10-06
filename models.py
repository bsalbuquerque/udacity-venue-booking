# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

from app import db


venue_genre = db.Table('venue_genre',
                       db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'),
                                 primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'),
                                 primary_key=True))

artist_genre = db.Table('artist_genre',
                        db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True))


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)
    genres = db.relationship('Genre', secondary=venue_genre, backref=db.backref('venue'), lazy=True)
    shows = db.relationship('Show', backref=db.backref('venue'), lazy=True)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)
    genres = db.relationship('Genre', secondary=artist_genre, backref=db.backref('artist'), lazy=True)
    shows = db.relationship('Show', backref=db.backref('artist'), lazy=True)


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    venues = db.relationship('Venue', backref=db.backref('show'), viewonly=True, lazy=True)
    artists = db.relationship('Artist', backref=db.backref('show'), viewonly=True, lazy=True)



