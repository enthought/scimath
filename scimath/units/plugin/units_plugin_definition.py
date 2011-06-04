""" Unit Sytem Plugin """

###############################################################################
#
#
# THIS UNITS PLUGIN IS DEPRECATED.
#
# You should be using: units_resource_plugin_definition and
# either units_ui_plugin_defintion or units_workbench_plugin_definition.
#
#
###############################################################################


from envisage.core.core_plugin_definition \
    import PluginDefinition, Preferences

from envisage.ui.ui_plugin_definition \
    import Action, UIActions

from envisage.resource.resource_plugin_definition \
    import ResourceManager, ResourceType, INSTANCE_RESOURCE_TYPE

from envisage.resource.resource_ui_plugin_definition \
    import ResourceWizard, ResourceWizards, \
           CookieImplementation, CookieImplementations

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "Units"

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

### Cookies ###################################################################

cookies = CookieImplementations(
    implementations = [
        CookieImplementation(
            resource_type = QUANTITY_RESOURCE_TYPE,

            cookie_interface = "envisage.project.action" \
                + ".open_cookie.OpenCookie",

            cookie_implementation = 'scimath.units.plugin' \
                + ".quantity_resource_open_cookie.QuantityResourceOpenCookie"
        ),
    ]
)

### Resource Wizards ##########################################################
resource_wizards = ResourceWizards(
    resource_wizards = [
        ResourceWizard(
            category    = 'Data Resources',
            name        = 'Quantity',
            class_name  = 'scimath.units.plugin.new_quantity_wizard.NewQuantityWizard'
        ),
        ResourceWizard(
            category    = 'Data Resources',
            name        = 'Scalar',
            class_name  = 'scimath.units.plugin.new_scalar_wizard.NewScalarWizard'
        )
    ]
)

#### Menus/Actions ############################################################
set_unit_system = Action(
    id              = 'action.SetUnitSystem',
    class_name      = \
         'scimath.units.plugin.action.set_unit_system_action.SetUnitSystem',
    name            = 'Set Unit System...',
    description     = 'Set the system-wide default unit system',
    image           = '',
    tooltip         = 'Set the system-wide default unit system',
    menu_bar_path   = 'ToolsMenu/',
    tool_bar_path   = '',
)

ui_actions = UIActions(
    actions = [
        set_unit_system,
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
    name          = "Units Plugin",
    version       = "1.0.0",
    provider_name = "Enthought Inc",
    provider_url  = "www.enthought.com",
    enabled       = True,
    autostart     = True,

    # The Id's of the plugins that this plugin requires.
    requires = [
        "envisage.core",
        "envisage.ui",
        "envisage.resource"
    ],

    # The extension points offered by this plugin,
    extension_points = [],

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [ui_actions,
                  preferences,
                  resource_manager,
                  resource_wizards,
                  cookies
                 ]
)

#### EOF ######################################################################
