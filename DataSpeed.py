import serial.tools.list_ports
import time

def receive_signal():
            times = []
            data=[]
            serial_ports = serial.tools.list_ports.comports()
            try:
                generator_name = 'COM3'
                for port in serial_ports:
                    if generator_name == port.name:
                        print("Found serial port")
                        if 'serial' in port.description.lower() or 'VCP' in port.description.lower():
                            # init serial port and bound
                            # bound rate on two ports must be the same
                            #was 9600
                            generator_ser = serial.Serial(generator_name, 115200, timeout=1)
                            generator_ser.flushInput()
                            #print(generator_ser.portstr)

                            #data = []

                            #print('stop flag', self.stop_flag)

                            start_time = time.time()
                            point_time = start_time
                            stop_flag = 0   
                            
                            while not stop_flag: # чтение байтов с порта 
                                point_time = time.time()
                                ser_bytes = generator_ser.read(2)
                                # print('huint', ser_bytes[0], ser_bytes[1] )
                                if len(ser_bytes) != 0:
                                    try:
                                        # print('ping', time.time() - point_time)

                                        cur_byte = int.from_bytes(ser_bytes, "little", signed=False) / 1024 * 5
                                        data.append(cur_byte)
                                  
                                        cur_time = float(time.time() - point_time)
                                        times.append(cur_time)
                                        
                                      
                                        
                                    except Exception as e:
                                        print('error in input', str(e))
                                if point_time - start_time >=20:
                                    stop_flag = 1
                                    
                                # self.reDraw(self.data[-50:])

                            else:
                                print("Stop flag:", stop_flag)
                                
                                
    #----------------------------------------------------------------------
                               
    #----------------------------------------------------------------------
                                print("Times", times)
                                print("Avg", sum(times)/len(times), 1 / (sum(times)/len(times)), 'Hz')

                                print("data: ", data)
                                print("min/max: ", min(data), max(data))

                                #print("Inds", self.data_ind)
                                
                              
                                return
                        else:
                            print("Error, no ports")
                            return    
            except Exception as e:
                print('error in common input', str(e))   

receive_signal() 