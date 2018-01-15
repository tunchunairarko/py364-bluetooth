from PyQt5.QtBluetooth import *
from PyQt5.Qt import QApplication


if __name__=='__main__()':
    app=QApplication()
    service=QBluetoothServiceInfo()
    a='00:00:00:00:5a:ad'
    adQ=QBluetoothAddress(a)
    service.registerService(adQ)
    soc=QBluetoothSocket(service.socketProtocol())
    soc.writeData('sadas')
    app.exit()