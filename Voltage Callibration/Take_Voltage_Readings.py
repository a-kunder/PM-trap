# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:16:11 2022

@author: stepadm
"""

import pyvisa as py
import numpy as np
import pandas as pd

rm = py.ResourceManager()
print(rm.list_resources())
    
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
    
'''initializes all 16 channels to 0V'''
def init_supply():
    for i in range(0, 17):
        set_voltage(channel=i, volts=0)

init_supply()
# set_voltage(channel=1, volts=0.15) #channels: 1 to 16, volts: -30 to 30

# measurement = multimeter.query("MEAS:VOLT:DC?")
# print(measurement)

def take_readings(channel, num_points=600, repetitions=10):
    input_voltages = np.linspace(-30, 30, num_points)
    output_voltages, percentages = [], []
    for i in range(num_points):
        measured = []
        for j in range(repetitions):
            set_voltage(channel, volts=input_voltages[i])
            measured.append(float(multimeter.query("MEAS:VOLT:DC?")))
        output_voltages.append([np.mean(measured), np.std(measured)])
        percentages.append(voltage_to_percent(input_voltages[i]))
        
    stacked = np.column_stack([percentages, input_voltages, output_voltages])
    print(stacked)
    #pd.DataFrame(stacked).to_csv(f"supply_callib_ch0{channel}.csv")
    
take_readings(channel=3, num_points=6)