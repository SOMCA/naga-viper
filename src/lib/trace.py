import datetime
import subprocess
import time
import os

class Tracker:

    def __init__(self, name):
        self.app_name = name
        self.debute = 0
        self.nom_trace = ''

    def cmd(chaine):
        tab = chaine.split()
        subprocess.Popen(tab)

    def start_tracking(self):
        #subprocess.Popen(Tracker.cmd('adb shell am start '+self.app_name+'/'+self.app_name+'.MainActivity'))
        self.nom_trace = datetime.date.today().ctime().replace(':','').replace(' ','_')+'.trace'
        Tracker.cmd('adb shell am profile start '+self.app_name+' /mnt/sdcard/'+self.nom_trace)
        self.debute = 1
        print('Starting ...')

    def sta(self):
        self.start_tracking()

    def stop_tracking(self):
        if self.debute:
            Tracker.cmd('adb shell am profile stop '+self.app_name+'/'+self.app_name+'MainActivity')
            print('Ending ... '+'Your file is : '+self.nom_trace)
            time.sleep(5)
            Tracker.cmd('adb pull /mnt/sdcard/'+self.nom_trace)
            time.sleep(5)
            print('../../../../Android/Sdk/tools/traceview -r '+self.nom_trace+' > '+self.nom_trace+'.txt')
            #subprocess.Popen(Tracker.cmd('../../../../Android/Sdk/tools/traceview -r '+self.nom_trace+' > '+self.nom_trace+'.txt'))
            os.system('../../../../Android/Sdk/tools/traceview -r '+self.nom_trace+' > '+self.nom_trace+'.txt')
            time.sleep(20)
        else:
            print('Vous n\'avez pas encore commencé le tracking')

    def sto(self):
        self.stop_tracking()

    def pause(self,temps):
        time.sleep(temps)
