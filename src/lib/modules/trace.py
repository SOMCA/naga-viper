import datetime
import subprocess
import time
import os

from ..network.websocket_client import SocketClient


class Tracker:

    def __init__(self, name):
        self.app_name = name
        self.start = 0
        self.trace_name = ''

    def cmd(chaine):
        tab = chaine.split()
        subprocess.Popen(tab)

    def start_tracking(self):
        #adb command to start the app : will be useless
        Tracker.cmd('adb shell am start '+self.app_name+'/'+self.app_name+'.MainActivity')
        #the name of the created files will contain the date
        self.trace_name = datetime.date.today().ctime().replace(':','').replace(' ','_')+'.trace'
        Tracker.cmd('adb shell am profile start '+self.app_name+' /mnt/sdcard/'+self.trace_name)
        self.start = 1
        print('Starting ...')
        time.sleep(1)
        self.stop_tracking()

    def stop_tracking(self):
        if self.start:
            Tracker.cmd('adb shell am profile stop '+self.app_name+'/'+self.app_name+'MainActivity')
            print('Ending ... '+'Your file is : '+self.trace_name)
            time.sleep(1)
            Tracker.cmd('adb pull /mnt/sdcard/'+self.trace_name)
            time.sleep(10)
            #We convert the file into a readable file
            os.system('/home/Android/Sdk/tools/traceview -r '+self.trace_name+' > '+self.trace_name+'.txt')
            #Waiting the conversion of the file
            time.sleep(20)

    def send(self):
        connection = SocketClient()
        connection.connect('127.0.0.1', 33333)
        #Opening the file which contains the data
        fr = open(self.trace_name+'.txt','r')
        ch = ''
        #Skiping the useless data
        while(ch != 'Call Times\n'):
            ch = fr.readline()
        fr.readline()
        #We send the interessting data
        while(ch != '' or ch != 'b' or ch != 'b\'\''):
            ch=fr.readline()
            #time.sleep(1)
            connection.send(ch)
        fr.close()

if __name__ == '__main__':
    t=Tracker('org.bottiger.podcast')
    t.start_tracking()
    t.send()

