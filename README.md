# kindle-panel

another toy project: a LAN updatable kindle status panel

Heavily based on [Matt Healy's web-to-kindle-heroku project](https://github.com/lankybutmacho/web-to-kindle-heroku) (original article [here](https://matthealy.com/kindle).)

Basically, there's two components:
1. the "status-server": a small flask server which keeps track of the current status (and which is remotely updatable over the LAN.) I ran mine on a local RaspberryPi in my home.
2. an update script which lives on the kindle and via a cronjob periodically polls the status-server for a screenshot of the latest status message and displays it on the kindle screen

This was just a fun project to build but not something I intend to use
