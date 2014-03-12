#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import dbus, os
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject
from subprocess import call
from time import sleep
from xdg.BaseDirectory import *

config_dir = os.path.join(xdg_config_home, 'apply-equalizer')
if not os.path.isdir(config_dir):
	os.mkdir(config_dir)

eq_config_path = os.path.join(xdg_config_home, 'pulse', 'equalizerrc')

def get_bus_address():
	return dbus.SessionBus()\
		.get_object(
			'org.PulseAudio1', 
			'/org/pulseaudio/server_lookup1'
		).Get(
			'org.PulseAudio.ServerLookup1',
			'Address',
			dbus_interface=dbus.PROPERTIES_IFACE
		)


def get_bus(srv_addr=None, restart_pulseaudio=True):
	attempt=1
	while not srv_addr:
		try:
			srv_addr = get_bus_address()
			print('Got pa-server bus from dbus: {}'.format(srv_addr))
		except dbus.exceptions.DBusException as err:
			print(err)
			if err.get_dbus_name() != 'org.freedesktop.DBus.Error.ServiceUnknown':
				raise
		attempt += 1
		if attempt > 10 and restart_pulseaudio:
			call (['pulseaudio', '-k'])
		sleep(1)
	return dbus.connection.Connection(srv_addr)


def on_port_change(port_addr):
	sink_addr = os.path.dirname(port_addr)
	sink = bus.get_object(object_path=sink_addr)
	sink_name = getName(sink, 'Device')
	
	port = bus.get_object(object_path=port_addr)
	port_name = getName(port, 'DevicePort')
	
	print ("change detected! new output port is '{}' on '{}'".format(port_name, sink_name))
	
	activate_profile(sink_name, port_name)


def getName (obj, itf):
	return obj.Get('org.PulseAudio.Core1.{}'.format(itf),
				'Name', dbus_interface=dbus.PROPERTIES_IFACE)

def make_conf_path(sink_name, port_name):
	return os.path.join(config_dir, sink_name, port_name, 'equalizerrc')


def activate_profile(sink_name, port_name):
	""" create symlink to port-specific eq conf """
	# dump old configuration and save content
	os.system('pulseaudio-equalizer interface.getsettings')
	current_conf = open(eq_config_path).read()
	
	# remove old config
	try:
		os.remove(eq_config_path)
	except OSError:
		pass
	
	conf_file = make_conf_path(sink_name, port_name)
	conf_dir = os.path.dirname(conf_file)
	
	# create new config if it does not exist and fill with old config
	if not os.path.isdir(conf_dir):
		os.makedirs(conf_dir)
		open(conf_file, 'w').write(current_conf)
	
	# create symlink
	os.symlink(conf_file, eq_config_path)
	
	# apply new settings
	os.system('pulseaudio-equalizer interface.applysettings')
	

DBusGMainLoop(set_as_default=True)
loop = GObject.MainLoop()

# connect to pulseaudio dbus
bus = get_bus()
core = bus.get_object(object_path='/org/pulseaudio/core1')

# activate profile for current audio device and port
fb_sink_addr = core.Get('org.PulseAudio.Core1', 'FallbackSink', dbus_interface=dbus.PROPERTIES_IFACE)
fb_sink = bus.get_object(object_path=fb_sink_addr)
fb_sink_name = getName(fb_sink, 'Device')
try:
	port_addr = fb_sink.Get('org.PulseAudio.Core1.Device', 'ActivePort', dbus_interface=dbus.PROPERTIES_IFACE)
	port = bus.get_object(object_path=port_addr)
	port_name = port.Get('org.PulseAudio.Core1.DevicePort', 'Name', dbus_interface=dbus.PROPERTIES_IFACE)
	activate_profile(fb_sink_name, port_name)
except dbus.exceptions.DBusException as e:
	print ("current device has no ports!")

# listen for port change events i.e. headphone is plugged in or out
bus.add_signal_receiver(on_port_change, 'ActivePortUpdated')
core.ListenForSignal('org.PulseAudio.Core1.Device.ActivePortUpdated', dbus.Array(signature='o'))

loop.run()
