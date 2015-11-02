/*
 * View model for OctoPrint-HipChat
 *
 * Author: Jens Hausherr
 * License: MIT
 */
$(function() {
    function HipchatViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        HipchatViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        [ /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_hipchat, #tab_plugin_hipchat, ...
        [ /* ... */ ]
    ]);
});
