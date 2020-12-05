#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


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
    Genres = db.Column(db.ARRAY(db.String()))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref=db.backref('venues', lazy=True), cascade="all, delete")
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
      return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref=db.backref('artist', lazy=True), cascade="all, delete")
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format,locale='en')
migrate = Migrate(app, db)
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
  locations = Venue.query.distinct('city','state').all()
  records =  Venue.query.all()
  data = []
  venuesInLocation = {}
  for loc in locations:
    venuesInLocation = {}
    venues =[]
    city = loc.city
    state = loc.state
    venuesInLocation ["city"] = loc.city
    venuesInLocation ["state"] = loc.state
    for record in records:
        if record.city == city and record.state == state:
            venue = {}
            venue ["id"] = record.id
            venue ["name"] = record.name
            venue ["num_upcoming_shows"] = len(db.session.query(Show).filter(Show.venue_id == record.id).all())
            venues.append(venue)
            venuesInLocation['venues'] = venues
    data.append(venuesInLocation)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  result = db.session.query(Venue).filter(Venue.name.ilike(f"%{request.form.get('search_term', '')}%")).all()
  response = {}
  data = []
  response["count"] = len(result)
  for r in result:
    record={}
    record ["id"] = r.id
    record["name"] = r.name
    record["num_upcoming_shows"] = len(db.session.query(Show).filter(Show.venue_id == r.id).filter(Show.start_time > datetime.now()).all())
    data.append(record)
  response["data"] = data
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  upcoming_shows_result = db.session.query(Show).join(Artist).filter (Show.id == venue.id).filter(Show.start_time > datetime.now())
  past_shows_result = db.session.query(Show).join(Artist).filter (Show.id == venue.id).filter(Show.start_time < datetime.now())
  
  data = {}
  data ["id"] = venue.id 
  data ["name"] = venue.name
  data["genres"] = venue.Genres
  data["address"] = venue.address
  data["city"] = venue.city
  data["state"] = venue.state
  data["phone"] = venue.phone
  data ["website"] = venue.website
  data["facebook_link"] =venue.facebook_link
  data["seeking_talent"]= venue.seeking_talent
  data["seeking_description"]= venue.seeking_description
  data["image_link"]= venue.image_link

  upcoming_shows = []
  for r in  upcoming_shows_result:
    record = {}
    record ["artist_id"] = r.id
    record ["artist_name"] = r.artist.name
    record ["artist_image_link"] = r.artist.image_link
    record ["start_time"]= r.start_time.strftime('%Y-%m-%d %H:%M:%S')
    upcoming_shows.append(record)
  data["upcoming_shows"] = upcoming_shows
  past_shows = []
  for r in  past_shows_result:
    record = {}
    record ["artist_id"] = r.id
    record ["artist_name"] = r.artist.name
    record ["artist_image_link"] = r.artist.image_link
    record ["start_time"]= r.start_time.strftime('%Y-%m-%d %H:%M:%S')
    past_shows.append(record)
  
  data["past_shows"] = past_shows
  data["past_shows_count"]= len(past_shows)
  data["upcoming_shows_count"]= len(upcoming_shows)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    venue = Venue(
      name = name,
      city = city,
      state = state,
      address = address,
      phone = phone,
      Genres = genres,
      facebook_link = facebook_link,
    )
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('The Venue has been successfully deleted!')
    return render_template('pages/home.html')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('The Venue can not be deleted deleted!')
    return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  records =  Artist.query.all()
  data = []
  for record in records:
    artist = {}
    artist["id"] = record.id 
    artist["name"] = record.name
    data.append(artist)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  result = db.session.query(Artist).filter(Artist.name.ilike(f"%{request.form.get('search_term', '')}%")).all()
  response = {}
  data = []
  response["count"] = len(result)
  for r in result:
    record={}
    record ["id"] = r.id
    record["name"] = r.name
    record["num_upcoming_shows"] = len(db.session.query(Show).filter(Show.venue_id == r.id).all())
    data.append(record)
  response["data"] = data
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  upcoming_shows_result = db.session.query(Show).join(Venue).filter (Show.id == artist.id).filter(Show.start_time > datetime.now())
  past_shows_result = db.session.query(Show).join(Venue).filter (Show.id == artist.id).filter(Show.start_time < datetime.now())
  data = {}
  data ["id"] = artist.id 
  data ["name"] = artist.name
  data["genres"] = artist.genres
  data["city"] = artist.city
  data["state"] = artist.state
  data["phone"] = artist.phone
  data ["website"] = artist.website
  data["facebook_link"] =artist.facebook_link
  data["seeking_talent"]= artist.seeking_talent
  data["seeking_description"]= artist.seeking_description
  data["image_link"]= artist.image_link

  upcoming_shows = []
  for r in  upcoming_shows_result:
    record = {}
    record ["venue_id"] = r.id
    record ["venue_name"] = r.artist.name
    record ["venue_image_link"] = r.artist.image_link
    record ["start_time"] = r.start_time.strftime('%Y-%m-%d %H:%M:%S')
    upcoming_shows.append(record)
  data["upcoming_shows"] = upcoming_shows
  past_shows = []
  for r in  past_shows_result:
    record = {}
    record ["artist_id"] = r.id
    record ["artist_name"] = r.artist.name
    record ["artist_image_link"] = r.artist.image_link
    record ["start_time"] =  r.start_time.strftime('%Y-%m-%d %H:%M:%S')
    past_shows.append(record)
  
  data["past_shows"] = past_shows
  data["past_shows_count"]= len(past_shows)
  data["upcoming_shows_count"]= len(upcoming_shows)
  return render_template('pages/show_artist.html', artist=data)
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])

def edit_artist(artist_id):
  form = ArtistForm()
  result_artist = Artist.query.get(artist_id)
  artist={
    "id": result_artist.id,
    "name": result_artist.name,
    "genres": result_artist.genres,
    "city": result_artist.city,
    "state": result_artist.state,
    "phone": result_artist.phone,
    "website": result_artist.website,
    "facebook_link": result_artist.facebook_link,
    "seeking_venue": result_artist.seeking_venue,
    "seeking_description": result_artist.seeking_description,
    "image_link": result_artist.image_link
    }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  artist = Artist.query.get(artist_id)
  try:
    artist.name = request.form['name'],
    artist.genres = request.form['genres']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.website = request.form['website']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venue = True if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  result_venue = Venue.query.get(venue_id)
  venue={
    "id": result_venue.id,
    "name": result_venue.name,
    "genres": result_venue.Genres,
    "address": result_venue.address,
    "city": result_venue.city,
    "state": result_venue.state,
    "phone": result_venue.phone,
    "website": result_venue.website,
    "facebook_link": result_venue.facebook_link,
    "seeking_talent": result_venue.seeking_talent,
    "seeking_description": result_venue.seeking_description,
    "image_link": result_venue.image_link
    }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False  
  venue = Venue.query.get(venue_id)
  try: 
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False 
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()

  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')

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
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('Genres')
    facebook_link = request.form['facebook_link']
    artist = Artist(
      name = name,
      city = city,
      state = state,
      phone = phone,
      genres = genres,
      facebook_link = facebook_link
    )
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else: 
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
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
  shows = Show.query.all()
  data=[]
  for show in shows:
    record = {}
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    record["venue_id"] = venue.id
    record["venue_name"] = venue.name
    record["artist_id"] = artist.id
    record["artist_name"] = artist.name
    record["artist_image_link"] = artist.image_link
    record["start_time"] = show.start_time
    data.append(record)
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
    venue_id = request.form["venue_id"]
    artist_id = request.form["artist_id"]
    start_time = request.form["start_time"]
    show = Show (
      venue_id =venue_id,
      artist_id=artist_id,
      start_time=start_time
    )
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # on successful db insert, flash success
  if not error:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  
  
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

'''
@app.route('/quizzes', methods=['POST'])
    def play_trivia():
        try:
            body = request.get_json()

            valid_categories = [0, 1, 2, 3, 4, 5, 6]
            if 'quiz_category' not in body or 'previous_questions' not in body:
                abort(400)
            elif int(body.get('quiz_category')['id']) not in valid_categories:
                abort(422)

            questions = [question.format() for question in
                         Question.query.filter(Question.id.notin_(
                             body.get('previous_questions'))).all()]

            if body.get('quiz_category')['id'] != 0:
                questions = [question.format() for question in
                             Question.query.filter_by(category=body.get(
                                 'quiz_category')['id']).filter(
                                 Question.id.notin_(body.get(
                                     'previous_questions'))).all()]

            if questions:
                next_question = random.choice(questions)
            else:
                next_question = None

            return jsonify({
                'success': True,
                'question': next_question
            })
'''

