import falcon
from IG_api import InstagramAPI

username= 'arnoldchatbot'
password= 'arnold@instagram'
api = InstagramAPI(username,password )
api.login()
class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        if api.direct_message('hi|how|are|you',463647202):
            resp.body=('sent!')

        # resp.body = ('\nTwo things awe me most, the starry sky '
        #              'above me and the moral law within me.\n'
        #              '\n'
        #              '    ~ Immanuel Kant\n\n')

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
