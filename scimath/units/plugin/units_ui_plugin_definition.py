""" Unit System UI Plugin """

from envisage.core.core_plugin_definition \
    import PluginDefinition, Preferences

from envisage.ui.ui_plugin_definition \
    import Action, UIActions

from envisage.resource.resource_ui_plugin_definition \
    import ResourceWizard, ResourceWizards, \
    CookieImplementation, CookieImplementations

# Import the id of the resource for which this plugin provides UI extenstions.
from scimath.units.plugin.units_resource_plugin_definition \
    import QUANTITY_RESOURCE_TYPE

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
BASE = "scimath.units.plugin"
ID = BASE + ".units_ui"

###############################################################################
# Extensions.
###############################################################################

### Cookies ###################################################################

cookies = CookieImplementations(
    implementations=[
        CookieImplementation(
            resource_type=QUANTITY_RESOURCE_TYPE,

            cookie_interface="envisage.project.action"
            + ".open_cookie.OpenCookie",

            cookie_implementation=BASE
            + ".quantity_resource_open_cookie.QuantityResourceOpenCookie"
        ),
    ]
)

### Resource Wizards ##########################################################
resource_wizards = ResourceWizards(
    resource_wizards=[
        ResourceWizard(
            category='Data Resources',
            name='Quantity',
            class_name=BASE + '.new_quantity_wizard.NewQuantityWizard'
        ),
        ResourceWizard(
            category='Data Resources',
            name='Scalar',
            class_name=BASE + '.new_scalar_wizard.NewScalarWizard'
        )
    ]
)

#### Menus/Actions ############################################################
set_unit_system = Action(
    id='action.SetUnitSystem',
    class_name=BASE + '.action.set_unit_system_action.SetUnitSystem',
    name='Set Unit System...',
    description='Set the system-wide default unit system',
    image='',
    tooltip='Set the system-wide default unit system',
    menu_bar_path='ToolsMenu/',
    tool_bar_path='',
)

ui_actions = UIActions(
    actions=[
        set_unit_system,
    ]
)

###############################################################################
# The plugin definition!
###############################################################################

PluginDefinition(
    # The plugin's globally unique identifier.
    id=ID,

    # The name of the class that implements the plugin.
    class_name="",

    # General information about the plugin.
    name="Units UI Plugin",
    version="1.0.0",
    provider_name="Enthought Inc",
    provider_url="www.enthought.com",
    enabled=True,
    autostart=True,

    # The Id's of the plugins that this plugin requires.
    requires=[
        "envisage.core",
        "envisage.ui",
        "envisage.resource",
        "scimath.units.plugin.units_resource"
    ],

    # The extension points offered by this plugin,
    extension_points=[],

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions=[ui_actions,
                resource_wizards,
                cookies
                ]
)
