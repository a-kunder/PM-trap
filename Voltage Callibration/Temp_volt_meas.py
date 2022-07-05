# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 17:17:52 2022

@author: stepadm
"""

import pyvisa as py
import numpy as np
import pandas as pd
import time
from datetime import datetime
rm = py.ResourceManager()

    
voltage_source = rm.open_resource('ASRL10::INSTR', baud_rate=115200, read_termination='\r', write_termination='\r')
print(voltage_source.query('IDN'))

multimeter = rm.open_resource('USB0::0x0957::0x0607::MY53003342::0::INSTR')
print(multimeter.query('*IDN?'))


'''converts DC voltage between -30V and 30V to a number between 0 and 1'''
def voltage_to_percent(volts=0):
    abs_range = 60
    if abs(volts) > 0.5*abs_range:
        raise Exception("Invalid input")
    else:
        return format((volts + 0.5*abs_range)/abs_range, '.6f')

'''sets a given channel of the supply to the given DC voltage'''
def set_voltage(channel, volts):
    percent = voltage_to_percent(volts)
    channel = f'CH0{channel} ' if channel < 10 else f'CH{channel} '
    cmd = 'HV259 ' + channel + percent
    voltage_source.query(cmd)


num_points = 55000
output_voltages = np.array([])
times = np.array([])
for i in range(num_points):
    set_voltage(channel=1, volts=-1)
    now = datetime.now().time()
    output_voltages = np.append(output_voltages, multimeter.query("MEAS:VOLT:DC?"))
    times = np.append(times, now)
    stacked = np.column_stack([times, output_voltages])
    if num_points % (num_points/100) == 0:
        pd.DataFrame(stacked).to_csv("temperature.csv") 
    time.sleep(1)
    
