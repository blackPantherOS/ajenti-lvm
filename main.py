import logging

from ajenti.api                 import *
from ajenti.plugins.main.api    import SectionPlugin
#from ajenti.plugins.mdadm.api   import PluginHeader
#from ajenti.ui                  import on, p, UIElement
from ajenti.ui.binder           import Binder
from api                        import getLvmStatus

@plugin
class RAID( SectionPlugin ):
    def init( self ):
        self.log        = logging.getLogger()
        self.title      = _( 'LVM' )
        self.icon       = 'hdd'
        self.category   = _( 'System' )
        self.lvm        = getLvmStatus()

        self.append( self.ui.inflate( 'lvm:main' ) )
        header          = self.find( 'header' )
        header.version  = self.lvm.getVersion()
        header.title    = 'LVM'
        header.plugin   = 'disks'
        header.author   = 'PE2MBS - Marc Bertens'
        header.email    = '<aplugins@pe2mbs.nl>'
        return
    # end def
# end class