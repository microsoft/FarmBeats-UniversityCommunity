# **2. Set up an alarm system**

#### **Objective**
Set up a system to alert the user when the plant needs to be watered. 

#### **Learning outcomes**
- Investigate creating rules using Azure IoT Central
  - Send email or push notification when the soil moisture is below a certain threshold.

  - Optional: check if temperature/pressure/light intensity is outside the optimal range.

  - Learn to use Azure Events Hub, Azure Stream Analytics and Azure Functions to process data.
  - Determine the date and time that the plant was last watered.

#### **Key areas to teach**
IoT Azure Services, Data, Microcontroller Programming, AI.


_Optionally a LED indicator can be integrated to indicate if the plant needs watering._

#### **Python example script for sending alarm email with a gmail account**
```python
import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
# import libraries for SMTP and email related functions

def main():

    sensor1 = seeed_dht.DHT("11", 12)
    # sensor1: DHT11

    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()
    sensor2 = GroveMoistureSensor(pin)
    # sensor2: moisture sensor

    alarm_state = False
    # create a default alarm state

    from_email_addr = 'sender_email@gmail.com'
    from_email_password = 'sender_email_password'
    to_email_addr = 'receiver_email@gmail.com'
    # set up the email credentials

    body = 'Farmbeats Alert: Your plants are thirsty!!'
    msg = MIMEText(body)
    # set email message

    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    # set sender and recipient

    msg['Subject'] = 'FARMBEATS ALERT!!!'

    while True:
        humi, temp = sensor1.read()
        m = sensor2.moisture
        if 0 <= m and m < 300 and temp > 25:
            alarm_state = True
            print('Alarm ON')

        if alarm_state == True:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            # connect to server and get ready to send email
            # edit above lines with your email provider's SMTP server details
            server.starttls()
            # comment out this line if provider does not use TLS
            server.login(from_email_addr, from_email_password)
            server.sendmail(from_email_addr, to_email_addr, msg.as_string())
            server.quit()
            print('Email sent')
            alarm_state = False
```
