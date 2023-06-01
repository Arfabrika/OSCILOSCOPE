import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
from PySide6.QtCore import QThreadPool

def receive_signal():
            times = []
            data=[]
            datadict = dict()
            serial_ports = serial.tools.list_ports.comports()
            
            try:
                generator_name = 'COM10'
                for port in serial_ports:
                    if generator_name == port.name:
                        print("Found serial port")
                        if 'serial' in port.description.lower() or 'VCP' in port.description.lower():
                            # init serial port and bound
                            generator_ser = serial.Serial(generator_name, 76800, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
                            generator_ser.write(b"M1")
                            ser_bytes = generator_ser.read(2)
                            
                            while 1:
                                generator_ser.write(b"R0")
                                ser_bytes = generator_ser.read(2)
                                print(ser_bytes)

                                if (len(ser_bytes)):
                                    if ser_bytes[0] == ord("A") and ser_bytes[1] == ord("0"):
                                        break                                      

                            start_time = time.perf_counter()
                            point_time = start_time
                            stop_flag = 0   
                            
                            while not stop_flag: # чтение байтов с порта 
                                point_time = time.perf_counter()
                                ser_bytes = generator_ser.read(2)
                                if len(ser_bytes) != 0:
                                    try:
                                        # print('ping', time.time() - point_time)

                                        cur_byte = int.from_bytes(ser_bytes[::-1], "little", signed=False) /1023.0*5.0
                                        data.append(cur_byte)
                                  
                                        cur_time = float(point_time - start_time)
                                        #data[cur_time] = cur_byte
                                        #times.append(cur_time)
                                        datadict[cur_time] = cur_byte                                    
                                      
                                    except Exception as e:
                                        print('error in input', str(e))
                                if point_time - start_time >= 5:
                                    stop_flag = 1
                            else:
                                print("Stop flag:", stop_flag)
                                generator_ser.write(b"C0")
                                ser_bytes = generator_ser.read(2)
                                print("In close protocol", ser_bytes)
                                if (len(ser_bytes)):
                                    if ser_bytes[0] == ord("C") and ser_bytes[1] == ord("0"):
                                        break
                                generator_ser.send_break(0)
                                
                                print(data, len(data), len(datadict.keys()))
                                # print("Times", datadict.keys())
                                # print("Len: ", len(datadict.keys()))
                                print("Avg", len(datadict.keys()) / list(datadict.keys())[-1],  'Hz')

                                # print("data: ", datadict)
                                # print("min/max: ", min(datadict.values()), max(datadict.values()))
                                plt.plot(datadict.keys(), datadict.values())
                                plt.show()

                                #print("Inds", self.data_ind)
                                return
                        else:
                            print("Error, no ports")
                            return    
            except Exception as e:
                print('error in common input', str(e))   

receive_signal() 