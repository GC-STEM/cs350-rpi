#
# Milestone1.py - This is the Python code template that will be used
# for Milestone 1, demonstrating the use of PWM to fade an LED in and
# out.
#
# This code works with the test circuit that was built for Assignment 1-4.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Development
#------------------------------------------------------------------

# Load the GPIO interface from the Raspberry Pi Python Module
# The GPIO interface will be available through the GPIO object
import RPi.GPIO as GPIO

# Load the time module so that we can utilize the sleep method to 
# inject a pause into our operation
import time

# Setup the GPIO interface
#
# 1. Turn off warnings for now - they can be useful for debugging more
#    complex code.
# 2. Tell the GPIO library we are using Broadcom pin-numbering. The 
#    Raspberry Pi CPU is manufactured by Broadcom, and they have a 
#    specific numbering scheme for the GPIO pins. It does not match
#    the layout on the header. However, the Broadcom pin numbering is
#    what is printed on the GPIO Breakout Board, so this should match!
# 3. Tell the GPIO library that we are using GPIO line 18, and that 
#    we are using it for Output. When this state is configured, setting
#    the GPIO line to true will provide positive voltage on that pin.
#    Based on the circuit we have built, positive voltage on the GPIO
#    pin will flow through the LED, through the resistor to the ground
#    pin and the LED will light up. 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Configure a PWM instance on GPIO line 18, with a frequency of 60Hz
pwm18 = GPIO.PWM(18, 60)

# Start the PWM instance on GPIO line 18 with 0% duty cycle
pwm18.start(0)

#
# Configure the loop variable so that we can exit cleanly when the user
# issues a keyboard interrupt (CTRL-C)
#
repeat = True
while repeat:
    try:
        # Loop from 0 to 100 in increments of 5, and update the dutyCycle
        # accordingly, pausing 1/10th of a second between each update

        ##
        ## TODO: Add a for loop that changes the duty cycle for the LED
        ## beginning at 0 and ending at 100. You should increment the duty
        ## cycle by 5 each pass through the loop. Each pass shoult have a
        ## 1/10th of a second interval between succeeding passes. This should
        ## take no more than 3 lines of code. Remove this TODO comment block
        ## when complete.
        ##

        # Loop from 100 to 0 in increments of -5, and update the dutyCycle
        # accordingly, pausing 1/10th of a second between each update
            
        ##
        ## TODO: Add a for loop that changes the duty cycle for the LED
        ## beginning at 100 and ending at 0. You should decrement the duty
        ## cycle by 5 each pass through the loop. Each pass shoult have a
        ## 1/10th of a second interval between succeeding passes. This should
        ## take no more than 3 lines of code. Remove this TODO comment block
        ## when complete.
        ##

    except KeyboardInterrupt:
        # Stop the PWM instance on GPIO line 18
        print('Stopping PWM and Cleaning Up')
        pwm18.stop()
        GPIO.cleanup()
        repeat = False

# Cleanup the GPIO pins used in this application and exit
GPIO.cleanup()