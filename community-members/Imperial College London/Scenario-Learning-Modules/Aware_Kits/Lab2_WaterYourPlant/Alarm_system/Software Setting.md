## **Setting Software:**

First install the **Grove** module.

```
curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -
```

Still, we start up with the **GHT11**.

- Download the source file by cloning the grove.py library.

```
cd ~
git clone https://github.com/Seeed-Studio/Seeed_Python_DHT.git
```

- Excute below commands to run the code.

```
cd Seeed_Python_DHT
sudo python setup.py install
cd ~/Seeed_Python_DHT/examples
python dht_simpleread.py 
```

- Now try to detect the atmosphere temperature and moisture with the following **dht_simpleread.py** code.

```python
import time
import seeed_dht
def main():
 
    # for DHT11/DHT22
    sensor = seeed_dht.DHT("11", 12)
    # for DHT10
    # sensor = seeed_dht.DHT("10")
 
    while True:
        humi, temp = sensor.read()
        if not humi is None:
            print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
        time.sleep(1)
 
 
if __name__ == '__main__':
    main()
```
Then we switch to the **moisture sensor**.

- Excute below commands.

```
cd grove.py/grove
python grove_moisture_sensor.py 0
```

- Following is the **grove_moisture_sensor.py** code.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
'''
This is the code for
    - Grove - Moisture Sensor <https://www.seeedstudio.com/Grove-Moisture-Sensor-p-955.html>`_
 
Examples:
 
    .. code-block:: python
 
        import time
        from grove.grove_moisture_sensor import GroveMoistureSensor
 
        # connect to alalog pin 2(slot A2)
        PIN = 2
 
        sensor = GroveMoistureSensor(PIN)
 
        print('Detecting moisture...')
        while True:
            m = sensor.moisture
            if 0 <= m and m < 300:
                result = 'Dry'
            elif 300 <= m and m < 600:
                result = 'Moist'
            else:
                result = 'Wet'
            print('Moisture value: {0}, {1}'.format(m, result))
            time.sleep(1)
'''
import math
import sys
import time
from grove.adc import ADC
 
__all__ = ["GroveMoistureSensor"]
 
class GroveMoistureSensor:
    '''
    Grove Moisture Sensor class
 
    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def moisture(self):
        '''
        Get the moisture strength value/voltage
 
        Returns:
            (int): voltage, in mV
        '''
        value = self.adc.read_voltage(self.channel)
        return value
 
Grove = GroveMoistureSensor
 
 
def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()
 
    sensor = GroveMoistureSensor(pin)
 
    print('Detecting moisture...')
    while True:
        m = sensor.moisture
        if 0 <= m and m < 300:
            result = 'Dry'
        elif 300 <= m and m < 600:
            result = 'Moist'
        else:
            result = 'Wet'
        print('Moisture value: {0}, {1}'.format(m, result))
        time.sleep(1)
 
if __name__ == '__main__':
    main()
```

Also test with the **red led**.

- Excute below commands.
```
cd ~/GrovePi/Software/Python
python grove_led_blink.py
```

- **grove_led_blink.py** code is shown below, remember to check if all sensors are working!
```python
import time
from grovepi import *
 
# Connect the Grove LED to digital port D4
led = 4
 
pinMode(led,"OUTPUT")
time.sleep(1)
 
print ("This example will blink a Grove LED connected to the GrovePi+ on the port labeled D4. If you're having trouble seeing the LED blink, be sure to check the LED connection and the port number. You may also try reversing the direction of the LED on the sensor.")
print (" ")
print ("Connect the LED to the port labele D4!" )
 
while True:
    try:
        #Blink the LED
        digitalWrite(led,1)     # Send HIGH to switch on LED
        print ("LED ON!")
        time.sleep(1)
 
        digitalWrite(led,0)     # Send LOW to switch off LED
        print ("LED OFF!")
        time.sleep(1)
 
    except KeyboardInterrupt:   # Turn LED off before stopping
        digitalWrite(led,0)
        break
    except IOError:             # Print "Error" if communication error encountered
        print ("Error")
 ```
