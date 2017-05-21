from flask_login import AnonymousUserMixin

#this class was created for the purpose of handling unregisterd user in the landing page and its associated templates
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

    def isAuthenticated(self):
        return False
 
    def is_active(self):
        return False
 
    def is_anonymous(self):
        return True