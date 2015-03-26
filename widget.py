from ajenti.api                     import plugin
from ajenti.api.sensors             import Sensor
from ajenti.plugins.dashboard.api   import DashboardWidget
import logging

from api import getLvmStatus

log = logging.getLogger()

@plugin
class LvmSensor( Sensor ):
    id = 'lvm'
    timeout = 5

    def measure( self, variant ):
        mdadm = getLvmStatus()
        mdadm.Update()
        return mdadm
    # end def
# end class

@plugin
class MdadmWidget( DashboardWidget ):
    name = _('LVM status')
    icon = 'hdd'

    def init( self ):
        self.sensor = Sensor.find( 'lvm' )
        self.append(self.ui.inflate( 'lvm:lvm-widget' ) )
        self.find( 'icon' ).icon = 'hdd'
        self.find( 'name' ).text = _( 'LVM status' )

        lvm = self.sensor.value()
        for group in lvm.Groups:
            group_box   = self.ui.inflate( 'lvm:lvm-widget-gline' )
            group_box.find( 'group' ).text  = group.name
            group_box.find( 'lines' ).append( line )
            for volume in group.Volumes:
                line    = self.ui.inflate( 'lvm:lvm-widget-vline' )
                line.find( 'volume' ).text  = volume.name
                progress            = line.find( 'progress' )
                progress.value      = volume.Size
                status              = line.find( 'status' )
                status.text         = device.stateText

                group_box.find( 'lines' ).append( line )

            # next
            self.find( 'lines' ).append( group_box )
        # next
    # end def
# end class