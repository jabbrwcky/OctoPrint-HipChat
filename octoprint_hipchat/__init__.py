# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin

from hypchat import HypChat

class HipchatPlugin(octoprint.plugin.StartupPlugin,
					octoprint.plugin.SettingsPlugin,
					octoprint.plugin.ProgressPlugin,
					octoprint.plugin.EventHandlerPlugin,
					#octoprint.plugin.AssetPlugin,
					octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			token=None,
			room=None,
			api_url="https://api.hipchat.com"
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/hipchat.js"],
			css=["css/hipchat.css"],
			less=["less/hipchat.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			hipchat=dict(
				displayName="Hipchat Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jabbrwcky",
				repo="OctoPrint-HipChat",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/jabbrwcky/OctoPrint-HipChat/archive/{target_version}.zip"
			)
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False, name="HipChat")
		]

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self,data)
		self.connect_to_hipchat()

	def on_after_startup(self):
		token = self._settings.get(["token"])
		endpoint= self._settings.get(["api_url"])
		room = self._settings.get(["room"])

		self.connect_to_hipchat()

		if self.hc:
			self.room().notification(color="gray", message="OctoPrint started.")

		self._logger.info("HipChat notification plugin started.")

	def on_event(self, event, payload):
		if event == "PrintStarted":
			job = self._printer.get_current_job()
			self.room().notification(color="green", message="Printing of file %s started. EPT: %f.2" % (job["name"], payload["estimatedPrintTime"]))
		elif event == "PrintFailed":
			self.room().notification(color="red", message="Printing of file %s from %s failed." % (payload["file"], payload["origin"]))
		elif event == "PrintDone":
			self.room().notification(color="green", message="Printing of file %s from %s has finished. Printing time: %f.2" % (payload["file"], payload["origin"], payload["time"]))
		elif event == "PrintCancelled":
			self.room().notification(color="red", message="Printing of file %s from %s has been cancelled." % (payload["file"], payload["origin"]))
		elif event == "PrintResumed":
			self.room().notification(color="greed", message="Printing of file %s from %s has been resumed." % (payload["file"], payload["origin"]))
		elif event == "PrintPaused":
			self.room().notification(color="yellow", message="Printing of file %s from %s has been paused." % (payload["file"], payload["origin"]))
		else:
			self._logger.debug("Event: %s => %s" % ( event, payload ))

	def on_print_progress(self, location, path, progress):
		self._logger.info(progress)
		if progress % 25 == 0:
			self._logger.info(self._printer.get_current_job())
			self.room().notification(color="gray", message="Printjob (%s from %s): %d%% complete." % (path, location, progress))

	def on_slicing_progress(self, slicer, source_location, source_path, destination_location, destination_path, progress):
		pass

	def connect_to_hipchat(self):
		token = self._settings.get(["token"])
		endpoint= self._settings.get(["api_url"])
		room = self._settings.get(["room"])
		if token && room:
			self.hc = HypChat(token, endpoint=endpoint)
			self.room = lambda: self.hc.get_room(room)
			self._logger.info("Publishing to room %s via API endpoint %s" % (room, endpoint))
		else:
			self.logger.warning("Token and/or Room not set! Not connecting to HipChat. Please configure API TOken and HipChat room in the plugin settings.")

__plugin_name__ = "Hipchat Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = HipchatPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
