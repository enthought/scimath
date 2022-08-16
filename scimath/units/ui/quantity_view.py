# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Default Traits View for Quantity objects. """

from traits.api import Instance, TraitError
from traitsui.api import View, Item, InstanceEditor, Handler

from scimath.units.quantity import Quantity
from scimath.units.unit_parser import unit_parser
from scimath.units.unit_manager import unit_manager


class QuantityView(View):
    """ Default Traits View for Quantity objects. """

    def __init__(self, **traits):
        """ Create a new QuantityView. """

        super(QuantityView, self).__init__(
            Item(name='name', style='readonly'),
            Item(name='units'),
            Item(name='family_name', label='Measure of'),
            Item(name='data', label='Value'),
            handler=QuantityViewHandler(),
            buttons=['OK', 'Cancel'],
            width=300,
            height=200
        )


class QuantityViewHandler(Handler):
    """ Handler for the QuantityView.
    It validates the consistency of the units and family_name and
    rolls back the changes if the control is canceled when closed.

    info.ui.context['naming_context'] when not None is a context in which
    the Quantity object is bound.
    """
    original = Instance(Quantity)

    def init(self, info):
        qty = info.ui.context['object']
        self.original = qty.clone()

        return super(QuantityViewHandler, self).init(info)

    def close(self, info, is_ok):
        return True

    def closed(self, info, is_ok):
        """ Handles a dialog-based user interface being closed by the user.
        """
        if not is_ok:
            qty = info.ui.context['object']
            qty.copy_traits(self.original)

    def setattr(self, info, object, name, value):
        """ Handles setting a specified object trait's value.

        Parameters
        ----------
        object : object
            The object whose attribute is being set
        name : string
            The name of the attribute being set
        value
            The value to which the attribute is being set
        """
        if not info.initialized:
            return

        if name == 'units':
            # Convert units label to units object.
            if not unit_manager.is_compatible(value, object.family_name):
                raise TraitError()

            value = unit_parser.parse_unit(value, suppress_warnings=False)

        super(QuantityViewHandler, self).setattr(info, object, name, value)

    def object_family_name_changed(self, info):
        """ Family name has changed, force the units to re-validate. """
        if info.initialized:

            # The previous family name may have been incompatible with the
            # units.  Poke the units to have it reevaluated with the new family.
            # In that case, the units string value in the UI control will not
            # match with the current value of the qty.units.  Thus, we need to
            # poke the ui control to have the control's value tested.
            for editor in info.ui._editors:
                if editor.name == 'units':
                    editor.update_object(None)
                    break
