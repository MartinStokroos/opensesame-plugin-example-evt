#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from setuptools import setup

setup(
	# Some general metadata. By convention, a plugin is named:
	# opensesame-plugin-[plugin name]
	name='opensesame-plugin-example_plugin',
	version='0.0.1',
	description='Example plugin for OpenSesame',
	author='Your Name',
	author_email='yourname@domain.com',
	url='https://github.com/your/repository',
	# Classifiers used by PyPi if you upload the plugin there
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	# The important bit that specifies how the plugin files should be installed,
	# so that they are found by OpenSesame. This is a bit different from normal
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files=[
		# First the target folder.
		('share/opensesame_plugins/example_plugin',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'opensesame_plugins/example_plugin/example_plugin.md',
			'opensesame_plugins/example_plugin/example_plugin.png',
			'opensesame_plugins/example_plugin/example_plugin_large.png',
			'opensesame_plugins/example_plugin/example_plugin.py',
			'opensesame_plugins/example_plugin/info.yaml',
			]
		)]
	)
