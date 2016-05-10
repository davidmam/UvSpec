# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:55:38 2016

Class library for the spec

@author: dmamartin
"""
import serial, time

class Spectrometer():
    '''Class to interface with a Jenway 6305 spectrometer'''
    def __init__(self, serialport=None, **kwarg):
        if serial:
            self.port = serialport
            self.serial = serial.Serial(self.port, 
                                        baudrate = 1200, 
                                        bytesize = 7, 
                                        parity = serial.PARITY_ODD, 
                                        stopbits = 1,
                                        timeout = 1 
                                        )
        else:
            raise Exception("A serial port must be specified")
        
        
            
    def printout(self):
        '''equivlaent to pressing the PRINT key on the spec.
        Return is the output text'''
        self.serial.write(b'D\n')
        output=''
        line = self.serial.readline()
        while line:
            output += line
            line = self.serial.readline()
        return output

    def transmission(self):
        '''retrieves transmission information from the spec
        Return is a tuple (transmission, wavelength)'''
        self.serial.write(b'SO\n')
        self.serial.write(b'T\n')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def absorbance(self):
        '''retrieves absorbance information from the spec
        Return is a tuple (absorbance, wavelength)'''
        self.serial.write(b'SO\n')
        self.serial.write(b'A\n')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def concentration(self):
        '''retrieves concentration information from the spec
        Return is a tuple (concentration, wavelength)'''
        self.serial.write(b'SO\n')
        self.serial.write(b'C\n')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def voltage(self):
        '''retrieves voltage information from the spec
        Return is a tuple (voltage, wavelength)'''
        self.serial.write(b'SO\n')
        self.serial.write(b'V\n')
        vals = self.serial.readline().strip().split('\t')
        return (float(vals[0]), int(vals[1]))
        
    def calibrate(self, trans=False):
        '''set a zero value for absorbance (trans = False) or
        transmission (trans = True)'''
        if trans:
            self.serial.write(b'SC\n')
        else:
            self.serial.write(b'SO\n')
        self.serial.write(b'Z\n')
        time.sleep(1)
        self.serial.write(b'SO\n')
        
        
    def set_wavelength(self, wavelength=540):
        '''Set the spec to a specific wavelength specified by 
        wavelentgth = <integer>'''
        if wavelength <198 or wavelength > 1000:
            raise Exception('invalid wavelength')
        self.serial.write(b'G%i\n'%wavelength)
        
        
    def set_conc_factor(self, factor=1):
        '''Sets the concentration factor for the spec to automatically
        determine concentration from absorbance'''
        self.serial.write(b'F%i\n'%factor)
    
    def scan(self, start=198, end=1000, interval=10):
        '''Performs an absorbance scan starting at start,
        ending at end, and taking a measurement every interval.
        Returns an array of (abs, wavelength) tuples'''
        data=[]
        for wl in range(start, end, interval):
            data.append(self.absorbance)
        return data

    def timeseries(self, reads=1, delay=0, file=None):
        '''takes reads measurements of absorbance spaced delay seconds apart.
        If file is specified then opens and writes data to that file, 
        otherwise returns data as an array of tuples of 
        (time, absorbance, wavelength)'''
        
        
    