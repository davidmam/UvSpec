# UvSpec
Code for controlling a UV-Vis spectrometer from a raspberry Pi

This code implements the protocol used to control a [Jenway 6305 UV Visible spectrometer](http://www.jenway.com/product.asp?dsl=289) from the command line.

Set up your Raspberry Pi with Serial interface ON and Serial terminal OFF. 
You will need to enable full hardware control with the RS232 interface. On the D9 interface, connect pin 7 (RTS) to pin 8 (CTS)
and tie pin 4 (DTR) to 5V (high). Pin 6 does not need to be set but could be used in a later implementation to detect when the 
spec is ready to send data, avoiding the need for software to guess how long it needs to wait.

### Key implementation:

    from J6305 import Spectrometer
    spec=Spectrometer()
    spec.set_wavelength(540)
    (absorbance, wavelength) = spec.absorbance()
    data = spec.scan(start=300, end=900, interval=10)
    # turn the lamp off 
    spec.set_shutter(False)
    # read raw voltage - by default with the lamp on
    (voltage, wavelength) = spec.voltage()
    # setting luminosity to True turns the lamp off to read the voltage.
    help(spec) # to see all the commands. 
    
   
