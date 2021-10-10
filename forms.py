import area_code_nanp
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Regexp, ValidationError
from models import *
import seeds


def validate_artist_id(form, artist_id):
    if not artist_id.data.isnumeric():
        raise ValidationError("You must enter an Artist ID number")
    elif not Artist.query.filter_by(id=artist_id.data).first():
        raise ValidationError("You must enter an existing Artist ID number")


def validate_venue_id(form, venue_id):
    if not venue_id.data.isnumeric():
        raise ValidationError("You must enter a Venue ID number")
    elif not Venue.query.filter_by(id=venue_id.data).first():
        raise ValidationError("You must enter an existing Venue ID number")


def validate_phone(form, phone):
    catch_phone = phone.data
    region = int(catch_phone[0:3])
    if area_code_nanp.get_region(region) is None:
        raise ValidationError("You must enter a valid phone code area")


def validate_genres(form, genres):
    for genre in genres.data:
        if genre not in seeds.genres_list:
            raise ValidationError("You must select a valid genre")


def validate_facebook_link(form, facebook_link):
    check_facebook = any(n in facebook_link.data for n in seeds.facebook_list)
    if not check_facebook:
        raise ValidationError("You must enter a Facebook link")


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired(), validate_artist_id]
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired(), validate_venue_id]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(),
                             Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', message="Invalid phone number format"),
                             validate_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        coerce=int, choices=[(g[0], g[1]) for g in seeds.genres_list.items()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL(require_tld=True),
                                     validate_facebook_link]
    )
    website_link = StringField(
        'website_link'
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[DataRequired(),
                             Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', message="Invalid phone number format"),
                             validate_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        coerce=int, choices=[(g[0], g[1]) for g in seeds.genres_list.items()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL(require_tld=True),
                                     validate_facebook_link]
    )
    website_link = StringField(
        'website_link'
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description'
    )
