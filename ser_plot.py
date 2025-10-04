class sers:
#
  def __init__(self):
    #read serials#    from read_m5b_class import m5logger
    import serial,time
    self.ser0=serial.Serial("/dev/ttyACM0",115200) 
    self.ser1=serial.Serial("/dev/ttyACM1",115200) 
    self.ser2=serial.Serial("/dev/ttyACM2",115200)
    self.ser3=serial.Serial("/dev/ttyACM3",115200)
#   
  def read(self):
#    global data1,data2,data3,data4
    data1=data2=data3=data4=[]
    while True:
      line01 = self.ser0.readline()
      line02 = self.ser1.readline()
      line03 = self.ser2.readline()
      line04 = self.ser3.readline()
      try:
        line01s=line01.strip().decode('utf-8')
        line02s=line02.strip().decode('utf-8')
        line03s=line03.strip().decode('utf-8')
        line04s=line04.strip().decode('utf-8')
      except UnicodeDecodeError:
        continue
      data1s=line01s.split(",")
      data2s=line02s.split(",")
      data3s=line03s.split(",")
      data4s=line04s.split(",")
      if data1s[0]=="01": data1=data1s[3:13]
      if data1s[0]=="02": data2=data1s[3:13]
      if data1s[0]=="A1": data3=data1s[1:9]
      if data1s[0]=="A2": data4=data1s[1:9]
      if data2s[0]=="01": data1=data2s[3:13]
      if data2s[0]=="02": data2=data2s[3:13]
      if data2s[0]=="A1": data3=data2s[1:9]
      if data2s[0]=="A2": data4=data2s[1:9]
      if data3s[0]=="01": data1=data3s[3:13]
      if data3s[0]=="02": data2=data3s[3:13]
      if data3s[0]=="A1": data3=data3s[1:9]
      if data3s[0]=="A2": data4=data3s[1:9]
      if data4s[0]=="01": data1=data4s[3:13]
      if data4s[0]=="02": data2=data4s[3:13]
      if data4s[0]=="A1": data3=data4s[1:9]
      if data4s[0]=="A2": data4=data4s[1:9]
#     
      return data1+data2+data3+data4
  def close(self):
   self.ser0.close()
   self.ser1.close()
   self.ser2.close()
   self.ser3.close()

ser=sers()
import time
from datetime import date
import matplotlib.pyplot as plt
#
current_time = time.strftime("_H%H_M%M_S%S", time.localtime())
fn = "TAD_" + str(date.today()) + current_time + ".csv"
f=open(fn, 'w', encoding="utf-8")
start=time.time()
core_timer_start=start
tc=[[0.0]*100]*20
ad=[[0.0]*100]*16
x=range(0,100)
fig = plt.figure(figsize=(11,4))
ax1 = fig.add_subplot(121)
ax1.set_title("Tc")
ax2 = fig.add_subplot(122)
ax2.set_title("ADC")
while 1:
 try:
  a=ser.read()
  if len(a)==36:
    now = time.time()
    st = time.strftime("%Y %b %d %H:%M:%S", time.localtime())
    ss = str(time.time() - int(time.time()))
    row=st + ss[1:5] + "," + str(round(time.time()-start, 2)) + ","
    for i in range(0,35):
      row=row+a[i]+","
    row=row+a[35]
    f.write(row+"\n")
# plot
    #plt.clf()
    for i in range(0,20):
      tc[i].pop(-1)
      try:
        tc[i].insert(0,float(a[i]))
      except:
        continue
    for i in range(0,16):
      ad[i].pop(-1)
      try:
        ad[i].insert(0,float(a[i+20]))
      except:
        continue 
    for i in range(0,20):
      try:
        ax1.plot(x,tc[i])
      except:
        continue
    for i in range(0,16):
      try:
        ax2.plot(x,ad[i])
      except:
        continue
    plt.pause(0.1)
 except KeyboardInterrupt:
  print("KeyboardInterrupt:")
  ser.close()
  f.close()
  exit()