""" Unit System Resource Plugin """

from __future__ import absolute_import
from envisage.core.core_plugin_definition \
    import PluginDefinition, Preferences

from envisage.resource.resource_plugin_definition \
    import ResourceManager, ResourceType, INSTANCE_RESOURCE_TYPE

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "scimath.units.plugin.units_resource"

###############################################################################
# Extensions.
###############################################################################

#### Preferences ##############################################################

preferences = Preferences(
    defaults = {
        'default_unit_system' : 'KGS'
    }
)

#### Resource Types ###########################################################
QUANTITY_RESOURCE_TYPE = \
    'scimath.units.plugin.quantity_resource_type.QuantityResourceType'

resource_manager = ResourceManager(
    resource_types = [
        ResourceType(
            class_name = QUANTITY_RESOURCE_TYPE,
            precedes   = [INSTANCE_RESOURCE_TYPE]
        ),
    ]
)


###############################################################################
# The plugin definition!
###############################################################################

PluginDefinition(
    # The plugin's globally unique identifier.
    id = ID,

    # The name of the class that implements the plugin.
    class_name = "scimath.units.plugin.units_plugin.UnitsPlugin",

    # General information about the plugin.
    name          = "Units Resource Plugin",
    version       = "1.0.0",
    provider_name = "Enthought Inc",
    provider_url  = "www.enthought.com",
    enabled       = True,
    autostart     = True,

    # The Id's of the plugins that this plugin requires.
    requires = [
        "envisage.core",
        "envisage.resource"
    ],

    # The extension points offered by this plugin,
    extension_points = [],

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [preferences,
                  resource_manager,
                 ]
)

#### EOF ######################################################################
