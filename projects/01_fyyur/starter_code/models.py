
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String)
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    created_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def details(self):
        past_shows = db.session.query(Show)\
        .join('venues').filter(Show.artist_id == self.id)\
        .filter(Show.start_time<datetime.now()).all()
        upcoming_shows = db.session.query(Show)\
        .join('venues').filter(Show.artist_id == self.id)\
        .filter(Show.start_time>=datetime.now()).all()
        past_shows_list = list(map(lambda x:x.artist_details(), past_shows))
        upcoming_shows_list = list(map(lambda x:x.artist_details(), upcoming_shows))
        return{
        'id': self.id,
        'name': self.name,
        'genres': self.genres,
        'city': self.city,
        'address': self.address,
        'state':self.state,
        'phone': self.phone,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description,
        'image_link': self.image_link,
        'past_shows':past_shows_list,
        'upcoming_shows': upcoming_shows_list,
        'past_shows_count':len(past_shows_list),
        'upcoming_shows_count': len(upcoming_shows_list)
        }
    def short(self):
      return {
        'id': self.id,
        'name':self.name
      }
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    created_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    shows = db.relationship('Show', backref='artist', lazy=True)

    def details(self):
      past_shows = db.session.query(Show)\
      .join('venues').filter(Show.artist_id == self.id)\
      .filter(Show.start_time<datetime.now()).all()
      upcoming_shows = db.session.query(Show)\
      .join('venues').filter(Show.artist_id == self.id)\
      .filter(Show.start_time>=datetime.now()).all()

      past_shows_list = list(map(lambda x:x.venue_details(), past_shows))
      upcoming_shows_list = list(map(lambda x:x.venue_details(), upcoming_shows))
      return{
          'id': self.id,
          'name': self.name,
          'genres': self.genres,
          'city': self.city,
          'state':self.state,
          'phone': self.phone,
          'website': self.website,
          'facebook_link': self.facebook_link,
          'seeking_venue': self.seeking_venue,
          'seeking_description': self.seeking_description,
          'image_link': self.image_link,
          'past_shows':past_shows_list,
          'upcoming_shows': upcoming_shows_list,
          'past_shows_count':len(past_shows_list),
          'upcoming_shows_count': len(upcoming_shows_list)
         
      }
    def short(self):
      return {
        'id': self.id,
        'name':self.name
      }
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    venues = db.relationship('Venue', backref="Show" )  
    artists = db.relationship('Artist', backref="Show")                      
    def details(self):
      return{
        'venue_id' :self.venue_id,
        'venue_name' :self.venues.name,
        'artist_id' :self.artist_id,
        'artist_name' :self.artists.name,
        'artist_image_link' :self.artists.image_link,
        'start_time' :self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }

    def artist_details(self):
      return {
        'artist_id' : self.artist_id,
        'artist_name' : self.artists.name,
        'artist_image_link' :self.artists.image_link,
        'start_time' :self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }

    def venue_details(self):
      return{
      'venue_id' :self.venue_id,
      'venue_name' :self.venues.name,
      'venue_image_link' :self.venues.image_link,
      'start_time' :self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }