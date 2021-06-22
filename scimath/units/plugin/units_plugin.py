# Enthought library imports.
from envisage import Plugin
from scimath.units import unit_manager

DEFAULT_UNIT_SYSTEM = 'default_unit_system'


class UnitsPlugin(Plugin):
    """ The Units plugin. """
    # The shared plugin instance.
    instance = None

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new plugin. """

        # Base-class constructor.
        super(UnitsPlugin, self).__init__(**traits)

        # Set the shared instance.
        UnitsPlugin.instance = self

        return

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def start(self, application):
        """ Starts the plugin.

        Can be called manually, but is usually called exactly once when the
        plugin is first required.

        """
        unit_system_name = self.preferences.get(DEFAULT_UNIT_SYSTEM)
        unit_system = unit_manager.lookup_system(unit_system_name)
        unit_manager.set_default(unit_system)

    def stop(self, application):
        """ Stops the plugin.

        Can be called manually, but is usually called exactly once when the
        application exits.

        """

        self.save_preferences()

    def set_default_unit_system(self, system):
        self.preferences.set(DEFAULT_UNIT_SYSTEM, system.name)
        return
