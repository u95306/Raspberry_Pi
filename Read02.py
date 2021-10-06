import RPi.GPIO as GPIO
import MFRC52202
import signal
import pygame

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC52202
MIFAREReader = MFRC52202.MFRC52202()

# Welcome message
print "Welcome to the MFRC52202 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the uid02 and authenticate
while continue_reading:
    
    # Scan for cards    
    (status02,TagType) = MIFAREReader.MFRC52202_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status02 == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the uid02 of the card
    (status02,uid02) = MIFAREReader.MFRC52202_Anticoll()

    # If we have the uid02, continue
    if status02 == MIFAREReader.MI_OK:

        # Print uid02
        print "Card read uid02: %s,%s,%s,%s" % (uid02[0], uid02[1], uid02[2], uid02[3])
        print "Card read uid02: %s" % (uid02[0]+uid02[1]+uid02[2]+uid02[3])
        a=str(uid02[0])+str(uid02[1])+str(uid02[2])+str(uid02[3])
        print (a)
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC52202_SelectTag(uid02)

        # Authenticate
        status02 = MIFAREReader.MFRC52202_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid02)

        # Check if authenticated
        if status02 == MIFAREReader.MI_OK:
            MIFAREReader.MFRC52202_Read(8)
            MIFAREReader.MFRC52202_StopCrypto1()
        else:
            print "Authentication error"