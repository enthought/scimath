""" The resource type plugin. """

# Plugin definition imports.
from envisage.core.core_plugin_definition import PluginDefinition

from envisage.resource.resource_plugin_definition \
    import ResourceType, ResourceManager

from envisage.resource.resource_ui_plugin_definition \
    import ResourceWizard, ResourceWizards, \
    CookieImplementation, CookieImplementations

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "pyface.resource_type"


###############################################################################
# Extensions.
###############################################################################


#### Resource types ###########################################################

BASE = 'envisage.resource'

# fixme: put these 'built-in' resource types into a separate resource plugin?
INSTANCE_RESOURCE_TYPE = BASE + '.instance_resource_type.InstanceResourceType'

QUANTITY_RESOURCE_TYPE = ID \
    + '.quantity_resource_type.QuantityResourceType'


resource_manager = ResourceManager(
    resource_types=[
        ResourceType(
            class_name=QUANTITY_RESOURCE_TYPE,
            precedes=[INSTANCE_RESOURCE_TYPE]
        )
    ]
)

### Cookies ###################################################################

cookies = CookieImplementations(
    implementations=[
        CookieImplementation(
            resource_type=QUANTITY_RESOURCE_TYPE,

            cookie_interface="envisage.project.action"
            + ".open_cookie.OpenCookie",

            cookie_implementation=ID
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
            class_name=ID + '.new_quantity_wizard.NewQuantityWizard'
        ),
        ResourceWizard(
            category='Data Resources',
            name='Scalar',
            class_name=ID + '.new_scalar_wizard.NewScalarWizard'
        )
    ]
)


###############################################################################
# The plugin definition.
###############################################################################

PluginDefinition(
    # The plugin's globally unique identifier.
    id=ID,

    # The name of the class that implements the plugin.
    class_name="",

    # General information about the plugin.
    name="Resource Plugin",
    version="1.0.0",
    provider_name="Enthought Inc",
    provider_url="www.enthought.com",
    enabled=True,
    autostart=False,

    # The Id's of the plugins that this plugin requires.
    requires=[
        "envisage.core",
        "envisage.project",
        "envisage.resource",
        "envisage.resource_ui"
    ],

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions=[
        resource_manager,
        resource_wizards,
        cookies,
    ]
)
