"""empty message

Revision ID: f983474e0d82
Revises: 
Create Date: 2017-05-17 11:28:30.204000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f983474e0d82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trip_Photos')
    op.add_column('itineraries', sa.Column('itineraryDate', sa.Date(), nullable=True))
    op.add_column('itineraries', sa.Column('itineraryTime', sa.Time(), nullable=True))
    op.drop_column('itineraries', 'itineraryTimeTo')
    op.drop_column('itineraries', 'itineraryDateFrom')
    op.drop_column('itineraries', 'itineraryTimeFrom')
    op.drop_column('itineraries', 'itineraryDateTo')
    op.add_column('trips', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('trips', sa.Column('tripCity', sa.String(length=70), nullable=True))
    op.add_column('trips', sa.Column('tripCountry', sa.String(length=70), nullable=True))
    op.add_column('trips', sa.Column('visibility', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trips', 'visibility')
    op.drop_column('trips', 'tripCountry')
    op.drop_column('trips', 'tripCity')
    op.drop_column('trips', 'status')
    op.add_column('itineraries', sa.Column('itineraryDateTo', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('itineraries', sa.Column('itineraryTimeFrom', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('itineraries', sa.Column('itineraryDateFrom', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('itineraries', sa.Column('itineraryTimeTo', postgresql.TIME(), autoincrement=False, nullable=True))
    op.drop_column('itineraries', 'itineraryTime')
    op.drop_column('itineraries', 'itineraryDate')
    op.create_table('trip_Photos',
    sa.Column('id', sa.INTEGER(), server_default=sa.text(u'nextval(\'"trip_Photos_id_seq"\'::regclass)'), nullable=False),
    sa.Column('photoName', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('photoDate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('photoLocation', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('tripID', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['tripID'], [u'trips.tripID'], name=u'trip_Photos_tripID_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'trip_Photos_pkey')
    )
    # ### end Alembic commands ###
