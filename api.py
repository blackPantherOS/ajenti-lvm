import copy
import time
import subprocess
import logging

class BaseLvmObject( object ):
    def __init__( self, owner ):
        self.log    = logging.getLogger()
        self.Owner  = owner
        return
    # end def

    def _execute( self, args ):
        process = subprocess.Popen( args, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        out, err = process.communicate()
        if 'error' in out:
            tmp = err
            err = out
            out = tmp
        # end if
        self.log.debug( "out: %s\nerr: %s" % ( out, err ) )
        return ( out, err )
    # end def

    def SetValue( self, name, value ):
        name = name.strip( ' ' )
        if name <> "":
            name = name.replace( '#', 'No' ).replace( '-', '_' )
            name = name.replace( ' ', '_' ).replace( '/', '' ).replace( ',', '' ).replace( '__', '_' )
            value = value.strip( ' ' )
            print( "SetValue( '%s', '%s' )" % ( name, value ) )
            if value.isdigit():
                setattr( self, name, int( value ) )
            else:
                setattr( self, name, value )
            # end def
        else:
            # error
            pass
        # end if
        return
    # end def

    def Update( self ):
        return
    # end def
# end class

class LogicalVolume( BaseLvmObject ):
    """
        --- Logical volume ---
        LV Path                /dev/testvg/DATA00
        LV Name                DATA00
        VG Name                testvg
        LV UUID                blsJG2-pLs5-dyEy-0Fdw-xm0r-lATl-ht4eb2
        LV Write Access        read/write
        LV Creation host, time enzo, 2015-03-24 20:28:55 +0100
        LV Status              available
        # open                 0
        LV Size                1,00 GiB
        Current LE             256
        Segments               1
        Allocation             inherit
        Read ahead sectors     auto
        - currently set to     256
        Block device           252:0
    """
    def __init__( self, owner ):
        BaseLvmObject.__init__( self, owner )
        self.LV_Path                = ''
        self.LV_Name                = ''
        self.VG_Name                = ''
        self.LV_UUID                = ''
        self.LV_Write_Access        = ''
        self.LV_Creation_host_time  = ''
        self.LV_Status              = ''
        self.No_open                = 0
        self.LV_Size                = ''
        self.Current_LE             = 0
        self.Segments               = 0
        self.Allocation             = ''
        self.Read_ahead_sectors     = ''
        self._currently_set_to      = ''
        self.Block_device           = ''
        return
    # end if

    def Dump( self ):
        print( '  Logical volume name  : %s' % ( self.LV_Name ) )
        print( '    Size               : %s' % ( self.LV_Size ) )
        print( '    Path               : %s' % ( self.LV_Path ) )

        print( '    Volume Group Name  : %s' % ( self.VG_Name ) )
        print( '    UUID               : %s' % ( self.LV_UUID ) )
        print( '    Write Access       : %s' % ( self.LV_Write_Access ) )
        print( '    Creation host time : %s' % ( self.LV_Creation_host_time ) )
        print( '    Status             : %s' % ( self.LV_Status ) )
        print( '    No open            : %s' % ( self.No_open ) )
        print( '    Current LE         : %s' % ( self.Current_LE ) )
        print( '    Segments           : %s' % ( self.Segments ) )
        print( '    Allocation         : %s' % ( self.Allocation ) )
        print( '    Read_ahead_sectors : %s' % ( self.Read_ahead_sectors ) )
        print( '    _currently_set_to  : %s' % ( self._currently_set_to ) )
        print( '    Block_device       : %s' % ( self.Block_device ) )
        print( '    path               : %s' % ( self.LV_Path ) )
        print( '' )
        return
    # end def
# end class

class VolumeGroup( BaseLvmObject ):
    def __init__( self, owner ):
        BaseLvmObject.__init__( self, owner )

        self.LogicalVolumes         = []
        self.VG_Name                = ''
        self.System_ID              = ''
        self.Format                 = ''
        self.Metadata_Areas         = 0
        self.Metadata_Sequence_No   = 0
        self.VG_Access              = ''
        self.VG_Status              = ''
        self.MAX_LV                 = 0
        self.Cur_LV                 = 0
        self.Open_LV                = 0
        self.Max_PV                 = 0
        self.Cur_PV                 = 0
        self.Act_PV                 = 0
        self.VG_Size                = ''
        self.PE_Size                = ''
        self.Total_PE               = 0
        self.Alloc_PE_Size          = ''
        self.Free_PE_Size           = ''
        self.VG_UUID                = ''
        return
    # end def

    def Dump( self ):
        print( 'VolumeGroup            : %s' % ( self.VG_Name ) )
        print( '  System_ID            : %s' % ( self.System_ID ) )
        print( '  Format               : %s' % ( self.Format ) )
        print( '  Metadata_Areas       : %s' % ( self.Metadata_Areas ) )
        print( '  Metadata_Sequence_No : %s' % ( self.Metadata_Sequence_No ) )
        print( '  VG_Access            : %s' % ( self.VG_Access ) )
        print( '  VG_Status            : %s' % ( self.VG_Status ) )
        print( '  MAX_LV               : %s' % ( self.MAX_LV ) )
        print( '  Cur_LV               : %s' % ( self.Cur_LV ) )
        print( '  Open_LV              : %s' % ( self.Open_LV ) )
        print( '  Max_PV               : %s' % ( self.Max_PV ) )
        print( '  Cur_PV               : %s' % ( self.Cur_PV ) )
        print( '  Act_PV               : %s' % ( self.Act_PV ) )
        print( '  VG_Size              : %s' % ( self.VG_Size ) )
        print( '  PE_Size              : %s' % ( self.PE_Size ) )
        print( '  Total_PE             : %s' % ( self.Total_PE ) )
        print( '  Alloc_PE_Size        : %s' % ( self.Alloc_PE_Size ) )
        print( '  Free_PE_Size         : %s' % ( self.Free_PE_Size ) )
        print( '  VG_UUID              : %s' % ( self.VG_UUID ) )
        for logVol in self.LogicalVolumes:
            logVol.Dump()
            print( '' )
        # next
        return
    # end def

    def Update( self ):
        lv = None
        out, err = self._execute( [ 'lvdisplay' ] )
        print( out, err )
        lines = out.splitlines( False )
        for line in lines:
            line = line.strip( ' \n\t' )
            if "--- Logical volume ---" in line:
                lv = LogicalVolume( self )
                self.LogicalVolumes.append( lv )
            else:
                print( line )
                lv.SetValue( line[0:22], line[22:] )
            # end if
        # next
        if not lv is None:
            lv.Update()
        # end if
        return
    # end def
# end class

class PhysicalVolume( BaseLvmObject ):
    """
        --- NEW Physical volume ---
        PV Name               /dev/sdb1
        VG Name
        PV Size               23.29 GB
        Allocatable           NO
        PE Size (KByte)       0
        Total PE              0
        Free PE               0
        Allocated PE          0
        PV UUID               G8lu2L-Hij1-NVde-sOKc-OoVI-fadg-Jd1vyU
    """
    def __init__( self, owner ):
        BaseLvmObject.__init__( self, owner )
        self.PV_Name            = ''
        self.VG_Name            = ''
        self.PV_Size            = 0
        self.Allocatable        = False
        self.PE_Size_KByte      = 0
        self.Total_PE           = 0
        self.Free_PE            = 0
        self.Allocated_PE       = 0
        self.PV_UUID            = ''
        return
    # end def

    def Dump( self ):
        print( 'PhysicalVolume         : %s' % ( self.PV_Name ) )
        print( '  Group                : %s' % ( self.VG_Name ) )
        print( '  Size                 : %s' % ( self.PV_Size ) )
        print( '  Allocatable          : %s' % ( self.Allocatable ) )
        print( '  PE_Size_KByte        : %s' % ( self.PE_Size_KByte ) )
        print( '  Total_PE             : %s' % ( self.Total_PE ) )
        print( '  Free_PE              : %s' % ( self.Free_PE ) )
        print( '  Allocated_PE         : %s' % ( self.Allocated_PE ) )
        print( '  PV_UUID              : %s' % ( self.PV_UUID ) )

        return
    # end def

    def Update( self ):
        return
    # end def

# end class

class LvmStatus( BaseLvmObject ):
    def __init__( self ):
        BaseLvmObject.__init__( self, None )
        self.PhysicalVolumes    = []
        self.VolumeGroups       = []
        return
    # end def

    def getVersion( self ):
        out, err = self._execute( [ 'lvm', 'version' ] )
        lines = out.splitlines( False )
        """
            LVM version:     2.02.98(2) (2012-10-15)
            Library version: 1.02.77 (2012-10-15)
            Driver version:  4.27.0
        """
        return lines[ 0 ].split( ':' )[ 1 ].strip( ' ' )
    # end def

    def Update( self ):
        pv = None
        out, err = self._execute( [ 'pvdisplay' ] )
        print( out, err )
        lines = out.splitlines( False )
        for line in lines:
            line = line.strip( ' \n\t' )
            if "--- Physical volume ---" in line:
                if not pv is None:
                    pv.Update()
                # end def
                pv = PhysicalVolume( self )
                self.PhysicalVolumes.append( pv )
            else:
                pv.SetValue( line[0:22], line[22:] )
            # end if
        # next
        if not pv is None:
            pv.Update()
        else:
            print( 'No more actions' )
            return
        # end def
        out, err = self._execute( [ 'vgdisplay' ] )
        print( out, err )
        vg = None
        lines = out.splitlines( False )
        for line in lines:
            line = line.strip( ' /n/t' )
            print( line )
            if "--- Volume group ---" in line:
                if not vg is None:
                    vg.Update()
                # end def
                vg = VolumeGroup( self )
                self.VolumeGroups.append( vg )
            else:
                vg.SetValue( line[0:22], line[22:] )
            # end def
        # next
        if not vg is None:
            vg.Update()
        return
    # end def

    def Dump( self ):
        print( 'LvmStatus' )
        for group in self.VolumeGroups:
            group.Dump()
        # next
        print( '' )

        for physical in self.PhysicalVolumes:
            physical.Dump()
        # next
        print( '' )

        return
    # end def

# end class

lvm = LvmStatus()

def getLvmStatus():
    global lvm
    return lvm
# end if

if __name__ == '__main__':
    test_lvm = getLvmStatus()
    while ( True ):
        test_lvm.Update()
        test_lvm.Dump()
        #time.sleep( 5 )
        break
    # end while
# end if