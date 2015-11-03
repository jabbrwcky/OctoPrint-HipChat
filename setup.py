# coding=utf-8
from setuptools import setup
import versioneer

plugin_identifier = "hipchat"
plugin_package = "octoprint_hipchat"
plugin_name = "OctoPrint-HipChat"
plugin_version = "0.1.0"
plugin_description = """A plugin that reports Status and progress to a HipChat room"""
plugin_author = "Jens Hausherr"
plugin_author_email = "jabbrwcky@gmail.com"
plugin_url = "https://github.com/jabbrwcky/OctoPrint-HipChat"
plugin_license = "MIT"
plugin_requires = ["hypchat"]
plugin_additional_data = []
plugin_additional_packages = []
plugin_ignored_packages = []
additional_setup_parameters = { "cmdclass": versioneer.get_cmdclass() }

try:
	import octoprint_setuptools
except:
	print("Could not import OctoPrint's setuptools, are you sure you are running that under "
	      "the same python installation that OctoPrint is installed under?")
	import sys
	sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
	identifier=plugin_identifier,
	package=plugin_package,
	name=plugin_name,
	version=versioneer.get_version(),
	description=plugin_description,
	author=plugin_author,
	mail=plugin_author_email,
	url=plugin_url,
	license=plugin_license,
	requires=plugin_requires,
	additional_packages=plugin_additional_packages,
	ignored_packages=plugin_ignored_packages,
	additional_data=plugin_additional_data
)

if len(additional_setup_parameters):
	from octoprint.util import dict_merge
	setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)

setup(**setup_parameters)
