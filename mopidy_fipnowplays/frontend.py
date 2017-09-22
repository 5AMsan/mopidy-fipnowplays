from __future__ import unicode_literals

import logging
import time

from mopidy.core import CoreListener

import pykka


logger = logging.getLogger(__name__)


class FipnowplaysFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(FipnowplaysFrontend, self).__init__()
        self.config = config

    def on_start(self):
        # test if FIP streams are configured and list the used ones
        logger.info('Discovered %s playlist(s) from FIP', '0')

    def track_playback_started(self, tl_track):
        track = tl_track.track
        logger.debug('Now playing stream: %s', track.name)

    def track_playback_ended(self, tl_track, time_position):
        pass
