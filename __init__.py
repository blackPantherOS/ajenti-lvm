from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title           = 'LVM',
    description     = 'Logical Volume Management',
    icon            = 'hdd',
    dependencies    = [
        PluginDependency( 'main' ),
        PluginDependency( 'mdadm' ), # for
        BinaryDependency( 'lvm' ),
    ],
)

def init():
    import api
    import main
    import widget
    return
# end def
