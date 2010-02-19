# Enthought library imports
from enthought.traits.api import HasTraits, Instance, Str
from enthought.units.unit import unit
from enthought.units.unit_parser import unit_parser

class Variable(HasTraits):
    """ Variable contains information about an input/output to a function

        They are used on by the component decorator function's that wrap
        standard python functions to handle unit conversion and other such
        things.
    """

    # The name of the variable.
    name= Str

    # A description of the variable.
    desc = Str

    # Units associated with the variable.
    units = Instance(unit)

    @classmethod
    def from_string(cls, string):
        """ Create a Variable object from a colon (':') delimited string.  The
            first field is the name.  The 2nd is the description.  After
            that, are xyz=abc fields.  Currently, only units is handled.

            fixme: this is woefully simple...  We should report/log more
                   failure information...
        """
        name = ''
        desc = ''
        units=None

        fields = string.split(':')

        # Get the name variable.
        if len(fields) > 0:
            name = fields[0].strip()
        else:
            #  fixme: We should probably log an error here...
            pass

        # Now the description
        if len(fields) > 1:
            desc = fields[1].strip()


        # Finally handle any 'keyword' attributes.
        for extra_attributes in fields[2:]:
            var, value = [x.strip() for x in extra_attributes.split('=')]
            if var.lower()=='units':
                units = unit_parser.parse_unit(value)
            else:
                # fixme: raise some sort of error here?
                pass

        return cls(name=name,desc=desc,units=units)
