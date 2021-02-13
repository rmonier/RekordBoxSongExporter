# RekordBoxSongExporter
A hack for Rekordbox 6.5.0 (Windows 64bit ONLY) to export played tracks for integration with OBS

This does **NOT** poll the rekordbox database, this directly hooks rekordbox which 
means your track listings will update in realtime in about ~2 seconds.

At the moment this will is designed to work with (and tested with) **two decks**, it is 
highly likely it will not work with four decks, the very least it will probably ignore
decks three and four. There may be updates in the future to handle this.

The 2 second delay is a result of OBS polling the chatlog file, the file is updated
instantaneously by the Song Exporter module as soon as you fade into the track.

The Launcher will launch RekordBox and inject a module which hooks two functions,
one function is called anytime the play/cue button is pressed on a track, and
the other function is called anytime the 'master' deck switches in Rekordbox.

The hook will detect anytime one of the two decks has a different song loaded
since the last time the user hit play, it will cache that song and artist for later.

The other hook will detect anytime the 'master' switches to another deck, when
this happens it will log the cached track and artist to the output files.

So the expected flow is to load a track, play/cue it, then eventually fade into 
the track. When you fade from one deck into the other Rekordbox will update the 
'master', this will trigger the hack to log the new track title and artist.

There are four output files:

```
   played_tracks.txt - this is a full log of all songs played in the entire session,
                       the oldest song will be at the top and newest at bottom
                       
  current_tracks.txt - this is the last X songs (configurable), newest song at top and
                       older songs under it
                       
   current_track.txt - this is only the current track playing, nothing else
   
      last_track.txt - this is only the last track to play, nothing else
```                    

The trick to integrating with OBS is to create a Text GDI object and select the 
'read from file' option.

Point the text GDI object at any of the four files and turn on 'chatlog' mode to
ensure the object is refreshed anytime the file changes content.
