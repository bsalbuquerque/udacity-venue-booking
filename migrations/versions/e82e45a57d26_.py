"""empty message

Revision ID: e82e45a57d26
Revises: 
Create Date: 2021-09-12 12:04:20.469657

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e82e45a57d26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=2), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('website_link', sa.String(length=120), nullable=True),
                    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
                    sa.Column('seeking_description', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    genre = op.create_table('genre',
                            sa.Column('id', sa.SmallInteger(), nullable=False),
                            sa.Column('name', sa.String(), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('name')
                            )
    op.create_table('venue',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=2), nullable=False),
                    sa.Column('address', sa.String(length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('website_link', sa.String(length=120), nullable=True),
                    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
                    sa.Column('seeking_description', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('artist_genre',
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('genre_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
                    sa.PrimaryKeyConstraint('artist_id', 'genre_id')
                    )
    op.create_table('show',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.Column('start_time', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('venue_genre',
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.Column('genre_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
                    sa.PrimaryKeyConstraint('venue_id', 'genre_id')
                    )
    op.bulk_insert(genre,
                   [
                       {'name': 'Alternative'},
                       {'name': 'Blues'},
                       {'name': 'Classical'},
                       {'name': 'Country'},
                       {'name': 'Electronic'},
                       {'name': 'Folk'},
                       {'name': 'Funk'},
                       {'name': 'Hip-Hop'},
                       {'name': 'Heavy Metal'},
                       {'name': 'Instrumental'},
                       {'name': 'Jazz'},
                       {'name': 'Musical Theatre'},
                       {'name': 'Pop'},
                       {'name': 'Punk'},
                       {'name': 'R&B'},
                       {'name': 'Reggae'},
                       {'name': 'Rock n Roll'},
                       {'name': 'Soul'},
                       {'name': 'Swing'},
                       {'name': 'Other'},
                   ]
                   )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_genre')
    op.drop_table('show')
    op.drop_table('artist_genre')
    op.drop_table('venue')
    op.drop_table('genre')
    op.drop_table('artist')
    # ### end Alembic commands ###
