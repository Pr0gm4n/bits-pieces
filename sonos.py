#!/usr/bin/python3
import soco
import pickle
from os import path, makedirs
import sys

class Sonos:
    def __init__(self):
        url = Cache.read('.sonos_IP_cache')
        if url:
            self.sonos = soco.SoCo(url)
        else:
            self.sonos = soco.discovery.any_soco()
            Cache.write('.sonos_IP_cache', self.sonos.ip_address)

    def toggle_TV(self):
        if self.sonos.is_playing_tv:
            # check previously cached mode to switch back to
            uri = Cache.read('.sonos_track_cache')
            if uri:
                self.sonos.play_uri(uri)
            else:
                # TODO: check how to "stop" playing TV
                #self.sonos.stop() # does not work
                pass
        else:
            # cache current mode to switch back to later
            track = self.sonos.get_current_track_info()
            if 'uri' in track:
                Cache.write('.sonos_track_cache', track['uri'])

            self.sonos.switch_to_tv()

    def play(self):
        self.sonos.play()

    def pause(self):
        self.sonos.pause()

    def volume_up(self):
        # Cache volume setting for smooth usage with repeated keyboard shortcut
        # invocations, as opposed to
        #self.sonos.volume += 5
        volume = Cache.read('.sonos_volume')
        if not volume:
            volume = self.sonos.volume
        volume += 5

        self.sonos.volume = volume
        Cache.write('.sonos_volume', volume)

    def volume_down(self):
        # Cache volume setting for smooth usage with repeated keyboard shortcut
        # invocations, as opposed to
        #self.sonos.volume -= 3
        volume = Cache.read('.sonos_volume')
        if not volume:
            volume = self.sonos.volume
        volume -= 3

        self.sonos.volume = volume
        Cache.write('.sonos_volume', volume)

    def mute(self):
        self.sonos.mute = not self.sonos.mute

    def jazz_radio(self):
        self.sonos.play_uri('x-rincon-mp3radio://http://54.38.43.201:8000/stream-128kmp3-101SmoothMellow')

    def sleep_timer(self, duration):
        self.sonos.set_sleep_timer(duration)


class Cache:
    path = '/home/roland/bin/'

    @staticmethod
    def read(filename):
        if path.exists(Cache.path + filename):
            with open(Cache.path + filename,'rb') as handle:
                return pickle.load(handle)
        return None

    @staticmethod
    def write(filename, content):
        if not path.exists(Cache.path):
            makedirs(Cache.path)
        with open(Cache.path + filename,'wb') as handle:
            pickle.dump(content, handle)


if __name__ == '__main__':
    if len(sys.argv) > 1: # some argument provided
        if sys.argv[1] == '--toggle-TV':
            Sonos().toggle_TV()
        elif sys.argv[1] == '--play':
            Sonos().play()
        elif sys.argv[1] == '--pause':
            Sonos().pause()
        elif sys.argv[1] == '--volume-up':
            Sonos().volume_up()
        elif sys.argv[1] == '--volume-down':
            Sonos().volume_down()
        elif sys.argv[1] == '--mute':
            Sonos().mute()
        elif sys.argv[1] == '--bedtime':
            sonos = Sonos()
            sonos.volume = 5
            sonos.jazz_radio()
            sonos.sleep_timer(60*45)
        else:
            print("Usage:")
            print("    sonos.py --toggle-TV | --play | --pause | --volume-up |"
                    + " --volume-down | --mute | --bedtime")
    else:
        print("Error: no argument given.")
        print("Try 'sonos.py --help' for usage information.")
