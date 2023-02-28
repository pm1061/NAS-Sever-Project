#!/usr/bin/env python3
import os
import time
import RPi.GPIO as GPIO

buzzer = 13
red = 3
green = 5
blue = 7

pins = [red,green,blue]

#setup GPIO
def setup():
	global pwmRed,pwmGreen,pwmBlue
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	#Set Up
	GPIO.setup(buzzer,GPIO.OUT)
	GPIO.setup(pins,GPIO.OUT)

	#Output
	GPIO.output(pins,GPIO.HIGH)
	pwmRed = GPIO.PWM(pins[0], 2000) # set PWM Frequence to 2kHz
	pwmGreen = GPIO.PWM(pins[1], 2000)
	pwmBlue = GPIO.PWM(pins[2], 2000)
	pwmRed.start(0) # set initial Duty Cycle to 0
	pwmGreen.start(0)
	pwmBlue.start(0)

#sets color value
def setColor(r_val,g_val,b_val): # change duty cycle for three pins to r_val,g_val,b_val
	pwmRed.ChangeDutyCycle(r_val) # change pwmRed duty cycle to r_val
	pwmGreen.ChangeDutyCycle(g_val)
	pwmBlue.ChangeDutyCycle(b_val)

#gets Free Space
def getFreespace(pathname):
    #Get the free space of the filesystem containing pathname
    stat= os.statvfs(pathname)
    # use f_bfree for superuser, or f_bavail if filesystem
    # has reserved space for superuser
    return round(float(stat.f_bfree*stat.f_bsize) * 0.000000001,3)

#gets Total Space
def getTotalspace(pathname):
    stat=os.statvfs(pathname)
    block_size=stat.f_frsize
    total_blocks=stat.f_blocks
    giga=1024*1024*1024
    total_size=total_blocks*block_size/giga
    #print('total_size = %s' % total_size)
    #print('block_size = %s' % block_size)
    #print('total_blocks = %s' % total_blocks)

    return total_size

#Main Function
if __name__ == '__main__':

	#setup GPIO
	setup()

	#Beep when sever is up and running
	GPIO.output(buzzer,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(buzzer,GPIO.LOW)

	#Check Space of Storage Device
	pathname = "/External/"


	#Total Space
	totalSpace = getTotalspace(pathname)

	#LED Values
	stillGood = totalSpace * 0.75 #blue
	half = totalSpace * 0.5 #green
	warn1 = 500 #yellow
	warn2 = 300 #orange
	replace = 100 #red

	#Refreash Delay
	delay = 600
	
	while True:

		spaceLeft = getFreespace(pathname)

		if spaceLeft <= replace:
			setColor(100,0,0)
		elif spaceLeft <= warn2:
                        setColor(100,51,0)
		elif spaceLeft <= warn1:
			setColor(100,100,0)
		elif spaceLeft <= half:
			setColor(0,100,0)
		elif spaceLeft <= stillGood:
                        setColor(0,0,100)
		else:
			setColor(100,0,100)

		time.sleep(delay)

