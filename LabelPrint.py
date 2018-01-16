from PIL import Image
import io
import os
from simple_zpl2 import ZPLDocument, Code128_Barcode, NetworkPrinter
import datetime
import win32api
import win32print
import base64
import tempfile
import sys
import usb.core
import usb.util


class LabelPrint:
    def __init__(self):
        self.barcode_image=None
        self.upc=None
        self.title=None
        self.dcNo=None

    def printPrinterList(self):
        print(win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL))
    def manualLabelPrint(self,img,labelfile):
        pass
    def __getUPCPosition(self,upc):
        n=len(upc)
        if(n<13):
            pos=115+((13-n)*2)
        else:
            pos=115-((n-13)*2)
        return pos
    def generateLabel(self,dcNo='0',upc='0',title='',price='$0',ip_add='10.1.10.155',width=2.25,height=1.25):

        zpl = ZPLDocument()
        zpl.add_comment('DC No')
        zpl.add_field_origin(320, 25)
        zpl.add_font('A', zpl._ORIENTATION_NORMAL, 10)
        zpl.add_field_data(str(dcNo))
        
        
        zpl.add_comment('UPC')
        upcPos=self.__getUPCPosition(upc)
        zpl.add_field_origin(int(upcPos), 50)
        code128_data = str(upc)
        bc = Code128_Barcode(code128_data, 'N', 50, 'Y')
        zpl.add_barcode(bc)

        zpl.add_comment('Date')
        zpl.add_field_origin(30, 180)
        zpl.add_font('S', zpl._ORIENTATION_NORMAL, 16)
        zpl.add_field_data(datetime.datetime.now().strftime('%d/%m/%Y'))

        zpl.add_comment('Price')
        zpl.add_field_origin(290, 180)
        zpl.add_font('G', zpl._ORIENTATION_NORMAL, 18)
        zpl.add_field_data(str('$'+price))
        self.printZPL(zpl)
        

    def printZPL(self,zpl):
        # find our device
        dev = usb.core.find(idVendor=0xa5f, idProduct=0x11c)

        # was it found?
        if dev is None:
            raise ValueError('Device not found')

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert ep is not None
        
        ep.write(zpl.zpl_bytes)
 
    
def main():
    #app = QCoreApplication(sys.argv)
    L=LabelPrint()
    zpl=L.generateLabel('112','B098HJ6X','Hershey''s syrup','32002')
    #print(zpl)

if __name__=='__main__':
    
    main()
