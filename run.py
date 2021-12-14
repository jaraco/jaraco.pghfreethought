__requires__ = ['keyring', 'requests_toolbelt']


from requests_toolbelt import sessions
import keyring


session = sessions.BaseUrlSession('https://api.wildapricot.org/v2.1/')
auth_session = sessions.BaseUrlSession('https://oauth.wildapricot.org/')

client_id = 'jaraco'
client_secret = keyring.get_password('https://api.wildapricot.org/', client_id)
client_auth = client_id, client_secret

username = 'jaraco@jaraco.com'
user_password = keyring.get_password('https://pghfreethought.org/', username)
auth_request = dict(
    grant_type='password', username=username, password=user_password,
    scope='auto',
)
resp = auth_session.post('auth/token', auth=client_auth, data=auth_request)
resp.raise_for_status()

session.headers['Authorization'] = f'Bearer {resp.json()["access_token"]}'
account, = session.get('accounts').json()

contacts_url = next(
    res for res in account['Resources'] if res['Name'] == 'Contacts')['Url']

members_query = {'$filter': 'member eq true', '$async': 'false'}
members_resp = session.get(contacts_url, data=members_query).json()
members = session.get(members_resp['ResultUrl']).json()['Contacts']
