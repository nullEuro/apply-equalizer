apply-equalizer
===============

A python programm that activates or deactivates pulseaudio-equalizer based on output port (headphones or speakers).

## Why ? ##

It started on [pulseaudio - Automatically switch equalizer preset based on audio output (internal speaker or external) - Ask Ubuntu](http://askubuntu.com/questions/402275/automatically-switch-equalizer-preset-based-on-audio-output-internal-speaker-or)

* **Problem:** laptop speakers have "highly unequal frequency response" as audio professional would say.  Normal people say: "they sound very bad".
* **Theory:** equalizing provides a valuable workaround, dramatically improving sound quality with a one-time effort.  Laptop speakers needs heavy equalization, which is not needed by regular stereo or headphones.
* **Practical (partial) solution:** use [pulseaudio-equalizer](https://launchpad.net/~nilarimogard/+archive/webupd8)
* **Remaining problem:** when switching between laptop speakers and audio line out (concretely, plugging your external stereo or headphones on the jack), equalization needs to be switched on and off or adjusted.
* **Solution:** this program automatically switches equalization profile based on active output.

## Installation ##
To use it you have to add the following line to `/etc/pulse/default.pa`:

    load-module module-dbus-protocol

Restart pulseaudio: `pulseaudio -k` (as user)

Then disable the equalizer via `pulseaudio-equalizer-gtk` and click on "Apply settings", now close the GUI.

Download this repository, change to the directory and run

    sudo make install
	apply-equalizer

Maybe you need to install some additional python modules.

To uninstall, change to the directory where you downloaded the repository and run

    sudo make clean

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
