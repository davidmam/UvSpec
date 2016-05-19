# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:55:38 2016

Class library for the spec

@author: dmamartin
"""
import serial, time

class Spectrometer():
    '''Class to interface with a Jenway 6305 spectrometer'''
    def __init__(self, serialport='/dev/ttyAMA0', **kwarg):
        if serial:
            self.port = serialport
            self.sleepinterval=0.1
            self.shutter=None
            self.serial = serial.Serial(self.port, 
                                        baudrate = 1200, 
                                        bytesize = 7, 
                                        parity = serial.PARITY_ODD, 
                                        stopbits = 1,
                                        timeout = 1 
                                        )
        else:
            raise Exception("A serial port must be specified")
        
    def set_shutter(self, isopen=True):
        if self.shutter == None or self.shutter != isopen:
            if isopen == True:
                self.serial.write(b'SO\r')
            else:
                self.serial.write(b'SC\r')
            self.shutter = isopen
            time.sleep(self.sleepinterval)     
                
    def printout(self):
        '''equivlaent to pressing the PRINT key on the spec.
        Return is the output text'''
        self.serial.write(b'D\r')
        output=''
        line = self.serial.readline()
        while line:
            output += line
            line = self.serial.readline()
        return output

    def transmission(self):
        '''retrieves transmission information from the spec
        Return is a tuple (transmission, wavelength)'''
        self.set_shutter(True)
        time.sleep(0.1)
        self.serial.write(b'T\r')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def absorbance(self):
        '''retrieves absorbance information from the spec
        Return is a tuple (absorbance, wavelength)'''
        self.set_shutter(True)
        self.serial.write(b'A\r')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def concentration(self):
        '''retrieves concentration information from the spec
        Return is a tuple (concentration, wavelength)'''
        self.set_shutter(True)
        self.serial.write(b'C\r')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def voltage(self):
        '''retrieves voltage information from the spec
        Return is a tuple (voltage, wavelength)'''
        self.set_shutter(True)
        self.serial.write(b'V\r')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def calibrate(self, trans=False):
        '''set a zero value for absorbance (trans = False) or
        transmission (trans = True)'''
        if trans:
            self.set_shutter(False)
        else:
            self.set_shutter(True)
        time.sleep(self.sleepinterval)
        self.serial.write(b'Z\r')
        time.sleep(self.sleepinterval)
        self.set_shutter(True)
        
        
    def set_wavelength(self, wavelength=540):
        '''Set the spec to a specific wavelength specified by 
        wavelentgth = <integer>'''
        if wavelength <198 or wavelength > 1000:
            raise Exception('invalid wavelength')
        comm = 'G%i\r'%wavelength
        self.serial.write(bytes(comm, 'ascii'))
        time.sleep(self.sleepinterval)
        
    def set_conc_factor(self, factor=1):
        '''Sets the concentration factor for the spec to automatically
        determine concentration from absorbance'''
        comm = 'F%i\r'%factor
        self.serial.write(bytes(comm, 'ascii'))
        time.sleep(self.sleepinterval)
    
    def scan(self, start=198, end=1000, interval=10):
        '''Performs an absorbance scan starting at start,
        ending at end, and taking a measurement every interval.
        Returns an array of (abs, wavelength) tuples'''
        data=[]
        for wl in range(start, end, interval):
            self.set_wavelength(wl)
            data.append(self.absorbance())
        return data


        
    