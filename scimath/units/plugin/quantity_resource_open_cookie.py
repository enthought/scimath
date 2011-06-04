""" The open cookie for Quantity resources. """


# Enthought library imports.

from enthought.envisage import get_application
from enthought.envisage.project.action.open_cookie import OpenCookie

class QuantityResourceOpenCookie(OpenCookie):
    """ The open cookie for Quantity resources. """

    ###########################################################################
    # 'OpenCookie' interface.
    ###########################################################################

    def open(self, window, binding, **kw):
        """ Opens a resource referenced by the binding. """

        context = binding.context

        qty = binding.obj

        qty.edit_traits( parent=window.control, naming_context=context )
        return

##### EOF #####################################################################
