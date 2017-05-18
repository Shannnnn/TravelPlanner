from app import db
db.create_all()

from app.trips.model import City, Country

# cnt1 = Country('Philippines', '1122')
# cnt2 = Country('United States of America', '3344')
#
# db.session.add(cnt1)
# db.session.add(cnt2)
# db.session.commit()

ct1 = City('1111', 'Iligan City', '1')
ct2 = City('2222', 'Ozamis City', '1')
ct3 = City('3333', 'New York City', '2')
ct4 = City('4444', 'Oklahoma City', '2')

db.session.add(ct1)
db.session.add(ct2)
db.session.add(ct3)
db.session.add(ct4)
db.session.commit()
