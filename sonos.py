#!/usr/bin/python3
import soco
import pickle
from os import path, makedirs
import sys
from time import time

class Sonos:
    def __init__(self, name = "Rolands Zimmer"):
        self.sonos = soco.discovery.by_name(name)

    def toggle_TV(self):
        if self.sonos.is_playing_tv:
            # revert boosted volume
            self.volume = 15

            # check previously cached mode to switch back to
            uri = Cache.read('.sonos_track_cache')
            if uri:
                self.sonos.play_uri(uri)
            else:
                # TODO: check how to "stop" playing TV
                #self.sonos.stop() # does not work
                pass
        else:
            # boost volume as line-in seems not very amplified
            self.volume = 50

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
        self.volume += 5

    def volume_down(self):
        self.volume -= 3

    @property
    def volume(self):
        # Cache volume setting for smooth usage with repeated keyboard shortcut
        # invocations, as opposed to
        cache = Cache.read('.sonos_volume_cache')

        if not cache or time() > cache["timestamp"] + 30:
            volume = self.sonos.volume
            Cache.write('.sonos_volume_cache', {
                "volume": volume,
                "timestamp": time()
            })
        else:
            volume = cache["volume"]

        return volume

    @volume.setter
    def volume(self, volume):
        # Cache volume setting for smooth usage with repeated keyboard shortcut
        # invocations, as opposed to
        Cache.write('.sonos_volume_cache', {
            "volume": volume,
            "timestamp": time()
        })
        self.sonos.volume = volume

    def mute(self):
        self.sonos.mute = not self.sonos.mute

    def next(self):
        self.sonos.next()

    def prev(self):
        self.sonos.previous()

    def join(self, name):
        soco.discovery.by_name(name).join(self.sonos)

    def unjoin(self, name):
        soco.discovery.by_name(name).unjoin()

    def join_toggle(self, name):
        s = soco.discovery.by_name(name)
        if s.is_coordinator:
            s.join(self.sonos)
        else:
            s.unjoin()

    def jazz_radio(self):
        self.sonos.play_uri('x-rincon-mp3radio://http://54.38.43.201:8000/stream-128kmp3-101SmoothMellow')

    def sleep_timer(self, duration):
        self.sonos.set_sleep_timer(duration)


class Cache:
    path = '/tmp/'

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
        elif sys.argv[1] == '--next-song':
            Sonos().next()
        elif sys.argv[1] == '--prev-song':
            Sonos().prev()
        elif sys.argv[1] == '--join-move':
            Sonos().join("Move")
        elif sys.argv[1] == '--unjoin-move':
            Sonos().unjoin("Move")
        elif sys.argv[1] == '--join-toggle-move':
            Sonos().join_toggle("Move")
        elif sys.argv[1] == '--bedtime':
            sonos = Sonos()
            sonos.volume = 5
            sonos.jazz_radio()
            sonos.sleep_timer(60*45)
        else:
            print("Usage:")
            print("    sonos.py --toggle-TV | --play | --pause | --volume-up |"
                    + " --volume-down | --mute | --next-song | --prev-song |"
                    + " --join-move | --unjoin-move | --join-toggle-move | --bedtime")
    else:
        print("Error: no argument given.")
        print("Try 'sonos.py --help' for usage information.")
