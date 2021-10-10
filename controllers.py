# ----------------------------------------------------------------------------#
# Imports.
# ----------------------------------------------------------------------------#
import datetime
import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for
from flask import current_app as app
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
import seeds


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    venue_list = Venue.query.add_columns(Venue.name).order_by(Venue.id.desc()).limit(10).all()
    artist_list = Artist.query.add_columns(Artist.name).order_by(Artist.id.desc()).limit(10).all()
    venue_data = []
    artist_data = []

    for venue in venue_list:
        new_venue = {
            "index": int(venue_list.index(venue) + 1),
            "name": venue.name
        }
        venue_data.append(new_venue)

    for artist in artist_list:
        new_artist = {
            "index": int(artist_list.index(artist) + 1),
            "name": artist.name
        }
        artist_data.append(new_artist)

    return render_template('pages/home.html', venues=venue_data,
                           artists=artist_data)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venue_list = Venue.query.all()
    venue_dict = {}
    data = []

    for venue in venue_list:
        venue_index = venue.city + "-" + venue.state
        num_upcoming_shows = 0
        if venue_index not in venue_dict:
            venue_dict[venue_index] = {
                "city": venue.city,
                "state": venue.state,
                "venues": []
            }

        for show_list in venue.shows:
            if show_list.start_time >= datetime.now():
                num_upcoming_shows += 1
        venue_dict[venue_index]["venues"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })

    for data_copy in venue_dict.values():
        data.append(data_copy)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search = "%" + request.form.get('search_term', '') + "%"
    search_venue = Venue.query.filter(Venue.name.ilike(search)).all()
    count = len(search_venue)
    response = {
        "count": count,
        "data": []
    }

    for venue in search_venue:
        num_upcoming_shows = 0

        for show in venue.shows:
            if show.start_time >= datetime.now():
                num_upcoming_shows += 1
        response["data"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows,
        })

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    data = []
    genres = []
    past_shows_count = 0
    upcoming_shows_count = 0

    for genre_id in venue.genre["id"]:
        genres.append(seeds.genres_list[genre_id])

    venue_dict = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [],
        "upcoming_shows": [],
    }

    for show in venue.shows:
        if show.start_time < datetime.now():
            past_shows_count += 1
            venue_dict["past_shows"].append({
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": show.start_time
            })
        else:
            upcoming_shows_count += 1
            venue_dict["upcoming_shows"].append({
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": format_datetime(show.start_time)
            })

    venue_dict["past_shows_count"] = past_shows_count
    venue_dict["upcoming_shows_count"] = upcoming_shows_count
    data.append(venue_dict)

    return render_template('pages/show_venue.html', venue=data[0])


#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue():
    form = VenueForm()

    try:
        if form.validate_on_submit():
            name = form.name.data
            city = form.city.data
            state = form.state.data
            address = form.address.data
            phone = form.phone.data
            genre = {"id": form.genres.data}
            facebook_link = form.facebook_link.data
            image_link = form.image_link.data
            website_link = form.website_link.data
            seeking_talent = form.seeking_talent.data
            seeking_description = form.seeking_description.data
            new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone,
                              genre=genre, facebook_link=facebook_link, image_link=image_link,
                              website_link=website_link, seeking_talent=seeking_talent,
                              seeking_description=seeking_description)
            db.session.add(new_venue)
            db.session.commit()
            flash('Venue ' + form.name.data + ' was successfully listed!')

            return redirect(url_for('index'))

    except():
        db.session.rollback()
        flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')

    finally:
        db.session.close()

    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<int:venue_id>/delete')
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)

    try:
        for show in venue.shows:
            db.session.delete(show)

        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully deleted!')

        return redirect(url_for('index'))

    except():
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')

    finally:
        db.session.close()


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = "%" + request.form.get('search_term', '') + "%"
    search_artist = Artist.query.filter(Artist.name.ilike(search)).all()
    count = len(search_artist)
    response = {
        "count": count,
        "data": []
    }

    for artist in search_artist:
        num_upcoming_shows = 0

        for show in artist.shows:
            if show.start_time >= datetime.now():
                num_upcoming_shows += 1
        response["data"].append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": num_upcoming_shows,
        })

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    data = []
    genres = []
    past_shows_count = 0
    upcoming_shows_count = 0

    for genre_id in artist.genre["id"]:
        genres.append(seeds.genres_list[genre_id])

    artist_dict = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": [],
        "upcoming_shows": [],
    }

    for show in artist.shows:
        if show.start_time < datetime.now():
            past_shows_count += 1
            artist_dict["past_shows"].append({
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": show.start_time
            })
        else:
            upcoming_shows_count += 1
            artist_dict["upcoming_shows"].append({
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": show.start_time
            })

    artist_dict["past_shows_count"] = past_shows_count
    artist_dict["upcoming_shows_count"] = upcoming_shows_count
    data.append(artist_dict)

    return render_template('pages/show_artist.html', artist=data[0])


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    data = {
        "id": artist.id,
        "name": artist.name
    }

    if request.method == "GET":
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.genres.data = [g for g in artist.genre["id"]]
        form.website_link.data = artist.website_link
        form.facebook_link.data = artist.facebook_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
        form.image_link.data = artist.image_link

    try:
        if form.validate_on_submit():
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.website_link = form.website_link.data
            artist.facebook_link = form.facebook_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data
            artist.image_link = form.image_link.data
            artist.genre = {
                "id": form.genres.data
            }
            db.session.commit()
            flash('Artist ' + form.name.data + ' was successfully updated!')

            return redirect(url_for('show_artist', artist_id=artist_id))

    except():
        db.session.rollback()
        flash('An error occurred. Artist could not be updated.')

    finally:
        db.session.close()

    return render_template('forms/edit_artist.html', form=form, artist=data)


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    data = {
        "id": venue.id,
        "name": venue.name
    }

    if request.method == "GET":
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.address.data = venue.address
        form.phone.data = venue.phone
        form.genres.data = [g for g in venue.genre["id"]]
        form.website_link.data = venue.website_link
        form.facebook_link.data = venue.facebook_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
        form.image_link.data = venue.image_link

    try:
        if form.validate_on_submit():
            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.website_link = form.website_link.data
            venue.facebook_link = form.facebook_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data
            venue.image_link = form.image_link.data
            venue.genre = {
                "id": form.genres.data
            }
            db.session.commit()
            flash('Venue ' + form.name.data + ' was successfully updated!')

            return redirect(url_for('show_venue', venue_id=venue_id))

    except():
        db.session.rollback()
        flash('An error occurred. Venue could not be updated.')

    finally:
        db.session.close()

    return render_template('forms/edit_venue.html', form=form, venue=data)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist():
    form = ArtistForm()

    try:
        if form.validate_on_submit():
            name = form.name.data
            city = form.city.data
            state = form.state.data
            phone = form.phone.data
            genre = {"id": form.genres.data}
            facebook_link = form.facebook_link.data
            image_link = form.image_link.data
            website_link = form.website_link.data
            seeking_venue = form.seeking_venue.data
            seeking_description = form.seeking_description.data
            new_artist = Artist(name=name, city=city, state=state, phone=phone, genre=genre,
                                facebook_link=facebook_link, image_link=image_link, website_link=website_link,
                                seeking_venue=seeking_venue, seeking_description=seeking_description)
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + form.name.data + ' was successfully listed!')

            return redirect(url_for('index'))

    except():
        db.session.rollback()
        flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')

    finally:
        db.session.close()

    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    num_shows = Show.query.filter(Show.start_time >= datetime.now()).order_by(Show.venue_id).all()
    data = []

    for show in num_shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venues.name,
            "artist_id": show.artist_id,
            "artist_name": show.artists.name,
            "artist_image_link": show.artists.image_link,
            "start_time": show.start_time
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['GET', 'POST'])
def create_show_submission():
    form = ShowForm()

    try:
        if form.validate_on_submit():
            artist_id = form.artist_id.data
            venue_id = form.venue_id.data
            start_time = form.start_time.data
            new_show = Show(artist_id=artist_id, venue_id=venue_id,
                            start_time=start_time)
            db.session.add(new_show)
            db.session.commit()
            flash('Show was successfully listed!')

            return redirect(url_for('index'))

    except():
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')

    return render_template('forms/new_show.html', form=form)


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
