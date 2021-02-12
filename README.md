# RekordBoxSongExporter
A hack for Rekordbox (Windows 64bit ONLY) to export played tracks for integration with OBS

NOTE: This does **NOT** poll the rekordbox database, this directly hooks rekordbox
      which means your track listings will update in realtime in about ~2 seconds

Simply configure the paths in the program, compile it, and run the Launcher.

The Launcher will launch RekordBox and inject a module which hooks a function,
that function is called anytime the play button is pressed on a track.

The hook will detect anytime one of the two decks has a different song loaded
since the last time the user hit play, it will log that song to two files.

One file is simply a track log which will append each song you play to the
played_tracks.txt file.

The other file contains the last 10 songs played in reverse order, where the 
newest song is always at the top of the file and older songs are pushed down 
the file to a maximum of 10 lines.

The second file is the trick to integrating with OBS, you create a GDI text
object in OBS and point it at that file then enable chatlog mode and adjust
the max lines to 10 (or however many you want)

There is plans in the future to hook into fader controls to be able to 
determine when a track is being faded into, which would in turn trigger
the track logging. This would be preferable to the track being logged
the moment it is cueud or played.
