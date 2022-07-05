# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:20:48 2022

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
    print(f"Uncorrected %: {percent}")
    channel = f'CH0{channel} ' if channel < 10 else f'CH{channel} '
    cmd = 'HV259 ' + channel + percent
    voltage_source.query(cmd)
    
'''initializes all 16 channels to 0V'''
def init_supply():
    for i in range(0, 17):
        set_voltage(channel=i, volts=0)
        
'''sets corrected voltage according to the linear fit of each channel'''
def set_corrected_voltage(channel, volts):
    fit_coeff = {
        1: [-0.0009250011066591374, 1.00387710],
        2: [-2.203615840814592e-05, 1.00386631],
        3: [-0.0010780255567561562, 1.00389198]
        }
    intercept, slope = fit_coeff[channel][0], fit_coeff[channel][1]
    
    corrected_voltage = slope*volts + intercept
    corrected_percent = voltage_to_percent(corrected_voltage)
    print(f"Corrected %: {corrected_percent}")
    channel = f'CH0{channel} ' if channel < 10 else f'CH{channel} '
    cmd = 'HV259 ' + channel + str(corrected_percent)
    voltage_source.query(cmd)
        
def main():
    #init_supply()
    channel = 3
    voltage = -1
    set_voltage(channel, volts=voltage)
    meas_wo_corr = multimeter.query("MEAS:VOLT:DC?")
    set_corrected_voltage(channel, volts=voltage)
    meas_corr = multimeter.query("MEAS:VOLT:DC?")
    print(f"Measurement without correction: {meas_wo_corr}, Difference: {abs(float(meas_wo_corr) - voltage)}")
    print(f"Measurement with correction: {meas_corr}, Difference: {abs(float(meas_corr) - voltage)}")
    # num_points, repetitions = 600, 10
    # input_voltages = np.linspace(-30, 30, num_points)
    # output_voltages, percentages = [], []
    # for i in range(num_points):
    #     measured = []
    #     for j in range(repetitions):
    #         set_corrected_voltage(channel, volts=input_voltages[i])
    #         measured.append(float(multimeter.query("MEAS:VOLT:DC?")))
    #     output_voltages.append([np.mean(measured), np.std(measured)])
    #     percentages.append(voltage_to_percent(input_voltages[i]))
        
    # stacked = np.column_stack([percentages, input_voltages, output_voltages])
    # pd.DataFrame(stacked).to_csv(f"supply_corrected_ch0{channel}.csv")
    

if __name__ == "__main__":
    main()