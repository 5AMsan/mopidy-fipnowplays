import requests
import logging
import pykka

from mopidy.models import Album, Artist, Track
from mopidy.audio import Audio

logger = logging.getLogger(__name__)	

class Fipnowplays(Audio):
	stream_uris = {'FIP':''}
	metadata_uris = {'FIP':'http://www.fipradio.fr/livemeta/7'}
	
	
	def __init__(self):
		super(Audio, self).__init__(self, config=None, mixer=None)
		#self._pending_uri = None
		#self._playbin = super(Fipnowplays, self)._playbin
		self.current_stream = 'FIP'
		self.update_metadata()
	
	def update_metadata(self):
		r = requests.post(Fipnowplays.metadata_uris[self.current_stream])
		
		if (r.status_code == 200):
			self.metadatas = r.json();
		else:
			raise Exception('Error while fetching metadata from server: %s' % r.status_code)
		
		level = self.metadatas['levels'][0]
		uid = level['items'][level['position']]
		step = self.metadatas['steps'][uid]	
		l_title = step.get('title').title()
		l_date = str(step.get('anneeEditionMusique'))
		l_visual = step.get('visual')
		l_album_title = step.get('titreAlbum').title()
		l_label = step.get('label').title()
		l_artists_names = step.get('authors').title()
		l_artists = Artist(name=l_artists_names)
		l_album = Album(name=l_album_title,
					    artists=[l_artists],
					    date=l_date,
					    images=[l_visual]
					    )
		self.track = Track(name=l_title,
						   album=l_album,
						   artists=[l_artists],
						   date=l_date,
						   comment=l_label
						   )
		super(Fipnowplays, self).set_metadata(self.track)
		

fip = Fipnowplays()
print(fip.track)
