apply-equalizer
===============

python programm that activates or deactivates pulseaudio-equalizer based on output port (headphones or speakers)

## Installation ##
To use it you have to add the following line to `/etc/pulse/default.pa`:

    load-module module-dbus-protocol

Then disable the equalizer via `pulseaudio-equalizer-gtk` and click on "Apply settings", now close the GUI.

Execute `apply-equalizer.py` it as user (!). Maybe you need to install some additional python modules. Also you may want to automatically start it on login (I dont know what is the best way to do that).

## Usage ##
The script creates per-port [1] equalizer-configurations under `~/.config/apply-equalizer` and symlinks them if a device changes the output port (i.e. headphones plugged in or out).

[1]: many sound cards have different *ports*, e.g. one speaker-port and one headphone-port

So:

 1. Unplug headphones.
 2. Open pulseaudio-equalizer GUI
 3. Customize equalizer-settings until it sounds good
 4. "Apply Settings" will then assign the configuration you made (including if the equalizer is enabled at all) to the *current port* (speakers in this case)
 5. **close the GUI** and repeat from step 2 for every port you want to assign (headphones not plugged in)

Now the equalizer settings get automatically adjusted whenever your switch between speakers and headphones.
