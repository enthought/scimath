# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Bool, TraitError
from traitsui.api import EnumEditor, Handler, Item, List, View


class MetaQuantityView(View):
    """ Default Traits View for MetaQuantity objects. """

    def __init__(self, *args, **traits):
        """ Create a new MetaQuantityView. """

        handler = traits.setdefault('handler', MetaQuantityViewHandler())
        handler.known_names = traits.pop('known_names', [])
        handler.any_name = traits.pop('any_name', True)

        if handler.any_name:
            evaluate = handler.validate_name
        else:
            evaluate = None

        name_editor = EnumEditor(name="known_names", object='handler',
                                 evaluate=evaluate)

        name_item = Item(name='name', label='Name',
                         editor=name_editor, id='name_item')

        super(MetaQuantityView, self).__init__(
            Item(name='name', editor=name_editor),
            Item(name='family_name', label='Measure of'),
            Item(name='units'),
            *args,
            **traits
        )


class MetaQuantityViewHandler(Handler):
    """ The MetaQuantityViewHandler manages the optional limiting of name
    to selection from a predefined list.
    """

    # User is limited to selecting the name of a known Quantities.
    known_names = List

    # When True, user is not limited to the known names list.
    any_name = Bool(True)

    def validate_name(self, name):
        """ Validate name against the known names and any_name flag.
        Returns name if validation passes.
        Raises TraitError otherwise.
        """
        name = name.strip()

        if self.any_name and len(name) == 0:
            raise TraitError('name must be specified')

        if not (self.any_name or name in self.known_names):
            raise TraitError('invalid name %s' % name)

        return name
