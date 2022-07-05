# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 12:13:40 2021

@author: stepadm
"""

# import pyvisa and create a list of all connected instruments
import pyvisa as py

print("1")
# import time
# print("2")
print(py.__file__)
print("3")
rm = py.ResourceManager()
print("4")
print(rm.list_resources())

# Communication with VS
# instrument_v = rm.open_resource('ASRL3::INSTR', baud_rate=9600, read_termination='\r', write_termination='\r')
# print(instrument_v)
# print(instrument_v.query('IDN'))

# def trans_volt_in_perc(x):
#     return (x+10.00000)/20.00000

# vtest = 0.00000

# valuew = format(trans_volt_in_perc(vtest), '.5f')
# print(valuew)


# #Set Voltages
# time.sleep(1)
# instrument_v.write('HV043 CH01 {0}'.format(valuew))
# time.sleep(1)
# instrument_v.write('HV043 CH02 {0}'.format(valuew))
# time.sleep(1)
# instrument_v.write('HV043 CH03 {0}'.format(valuew))
# time.sleep(1)
# instrument_v.write('HV043 CH04 {0}'.format(valuew))
# time.sleep(1)
# instrument_v.write('HV043 CH05 {0}'.format(valuew))

# print(instrument_precision_v.query('HV043 Q02'))
