#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from os import abort
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
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
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    genres = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def details (self):
      past_shows=[]
      upcoming_shows=[]
      for show in self.shows:
        if show.start_time>=datetime.today():
          upcoming_shows.append(show)
        else:
          past_shows.append(show)

      past_shows_list=list(map(lambda x:x.artist_details(),past_shows))    
      upcoming_shows_list=list(map(lambda x:x.artist_details(),upcoming_shows))  

      return{
        'id': self.id,
        'name':self.name,
        'city':self.city,
        'state':self.state,
        'address':self.address,
        'phone':self.phone,
        'image_link':self.image_link,
        'facebook_link':self.facebook_link,
        'seeking_talent':self.seeking_talent,
        'seeking_description':self.seeking_description,
        'genres':self.genres,
        'website':self.website,
        'past_shows': past_shows_list,
        'upcoming_shows':upcoming_shows_list,
        'past_shows_count':len(past_shows_list),
        'upcoming_shows_count':len(upcoming_shows_list)
      }

      def short (self):
        return{
          'id':self.id,
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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String() , nullable=False)
    shows = db.relationship('Show', backref='artist', lazy=True)

    def details (self):
      past_shows=[]
      upcoming_shows=[]
      for show in self.shows:
        if show.start_time>=datetime.today():
          upcoming_shows.append(show)
        else:
          past_shows.append(show)

      past_shows_list=list(map(lambda x:x.venue_details(),past_shows))    
      upcoming_shows_list=list(map(lambda x:x.venue_details(),upcoming_shows))  

      return{
        'id': self.id,
        'name':self.name,
        'city':self.city,
        'state':self.state,
        'phone':self.phone,
        'image_link':self.image_link,
        'facebook_link':self.facebook_link,
        'seeking_venue':self.seeking_venue,
        'seeking_description':self.seeking_description,
        'genres':self.genres,
        'website':self.website,
        'past_shows': past_shows_list,
        'upcoming_shows':upcoming_shows_list,
        'past_shows_count':len(past_shows_list),
        'upcoming_shows_count':len(upcoming_shows_list)
      }

    def short (self):
        return{
          'id':self.id,
          'name':self.name
        }

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime,default= datetime.utcnow , nullable=False)
  venues = db.relationship('Venue', backref='Show')
  artists = db.relationship('Artist', backref='Show')
  
  def details(self):
    return{
      'venue_id':self.venue_id,
      'venue_name':self.venues.name,
      'artist_id':self.artist_id,
      'artist_name':self.artists.name,
      'artist_image_link':self.artists.image_link,
      'start_time':self.start_time.strftime('%A %d-%m-%Y, %H:%M:%S')
    }

  def artist_details(self):
    return{
      'artist_id':self.artist_id,
      'artist_name':self.artists.name,
      'artist_image_link':self.artists.image_link,
      'start_time':self.start_time.strftime('%A %d-%m-%Y, %H:%M:%S')
    }

  def venue_details(self):
    return{
      'venue_id':self.venue_id,
      'venue_name':self.venues.name,
      'start_time':self.start_time.strftime('%A %d-%m-%Y, %H:%M:%S'),
      'venue_image_link':self.venues.image_link
    }
    

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  for v in venues:
    upcomping_shows = list(map(lambda x:x.venue_details(), v.shows))
    data.append({
      'city': v.city,
      "state": v.state,
      "venues": [{
        "id": v.id,
        "name": v.name,
        "num_upcoming_shows": len(upcomping_shows)
      }]
    })
    print(data)

  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  result = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  venue_list = list(map(lambda x:x.short(), result))
  response = {
    "count": len(venue_list),
    "data": venue_list
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  if venue:
      data = venue.details()
  else:
      return render_template('errors/404.html')
  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
  try:
      venue=Venue()
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.phone = request.form['phone']
      venue.facebook_link = request.form['facebook_link']
      venue.image_link = request.form['image_link']
      venue.website = request.form['website_link']
      venue.seeking_description = request.form['seeking_description']
      temp_list =request.form.getlist('genres')
      venue.genres=','.join(temp_list)
      if hasattr(request.form,'seeking_artist'):
        venue.seeking_artist = True if request.form['seeking_artist'] =='y' else False
      else:
          venue.seeking_venue = False
      db.session.add(venue)
      db.session.commit()
  except():
        error = True
        db.session.add.rollbac()
        print(sys.exc_info)
  finally:
      db.session.close()
      if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      else:

  # on successful db insert, flash success
       flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    abort(500)
  else:
    return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  result = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
  artist_list = list(map(lambda x:x.short(), result))
  response = {
    "count": len(artist_list),
    "data": artist_list
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.get(artist_id)
  if artist:
    data = artist.details()
  else:
    return render_template('errors/404.html')
  return render_template('pages/show_artist.html', artist=data)
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.website_link.data = artist.website
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.genres.data = artist.genres

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  print(request.form)
  artist = Artist.query.get(artist_id)
  error = False
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website_link']
    if hasattr(request.form, 'seeking_venue'):
     artist.seeking_venue = True if request.form['seeking_venue'] == 'y' else False
    else:
      artist.seeking_venue = False
    artist.seeking_description = request.form['seeking_description']
    temp_list = request.form.getlist('genres')
    artist.genres = ','.join(temp_list)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.address.data = venue.address
  form.website_link.data = venue.website
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.genres.data = venue.genres

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  venue = Venue.query.get(venue_id)
  error = False
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.address = request.form['address']
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website = request.form['website_link']
    if hasattr(request.form, 'seeking_talent'):
      venue.seeking_talent = True if request.form['seeking_talent'] == 'y' else False
    else:
      venue.seeking_talent = False  
    venue.seeking_description = request.form['seeking_description']
    temp_list = request.form.getlist('genres')
    venue.genres = ','.join(temp_list)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
  try:
    artist=Artist()
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website_link']
    artist.seeking_description = request.form['seeking_description']
    temp_list =request.form.getlist('genres')
    artist.genres=','.join(temp_list)
    if hasattr(request.form,'seeking_venue'):
      artist.seeking_venue = True if request.form['seeking_venue'] =='y' else False
    else:
        artist.seeking_venue = False
    db.session.add(artist)
    db.session.commit()
  except():
      error = True
      db.session.add.rollbac()
      print(sys.exc_info)
  finally:
    db.session.close()
    if error:
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
  # on successful db insert, flash success
     flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows =Show.query.all()
  data =list(map(lambda x:x.details(),shows))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    show = Show()
    show.artist_id = request.form['artist_id']
    show.venue_id = request.form['venue_id']
    show.start_time = request.form['start_time']
    db.session.add(show)
    db.session.commit()
  except():
     error = True
     db.session.rollback()
     print(sys.exc_info)
  finally:
     db.session.close()
     if error:
       flash('An error occurred. Show could not be listed.')
     else:
       flash('Show was successfully listed!')
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
