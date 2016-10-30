from requests import Session
from betamax import Betamax

with Betamax.configure() as config:
  config.cassette_library_dir = 'tests/fixtures/cassettes'

session  = Session()
base_url = 'https://api.nasa.gov'
api_key  = '5xiMKrACVWNUcmXU4TwNdzv22V5xq7wF4gkhV5nJ'

def request(path, params = {}, cassette = 'asteroids'):
  with Betamax(session) as vcr:
    # vcr.use_cassette(cassette, record = 'new_episodes')
    vcr.use_cassette(cassette, record = 'none')

    params['api_key'] = api_key
    request  = session.get(base_url + path, params = params)
    return request.json()
