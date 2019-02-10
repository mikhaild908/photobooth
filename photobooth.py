#!/usr/bin/env python
import os
import glob
import time
import traceback
from time import sleep, strftime
import RPi.GPIO as GPIO
import picamera
import atexit
import sys
import socket
import pygame
import webbrowser
from signal import alarm, signal, SIGALRM, SIGKILL

BUTTON_PIN = 21

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480
#DISPLAY_WIDTH = 360
#DISPLAY_HEIGHT = 240

#PREVIEW_WIDTH = 266
#PREVIEW_HEIGHT = 160

PREVIEW_WIDTH = 300
PREVIEW_HEIGHT = 300

PREVIEW_X = 50
PREVIEW_Y = 100

OFFSET_X = 0
OFFSET_Y = 0

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]

PRINTER = "Canon_SELPHY_CP1300"

REAL_PATH = os.path.dirname(os.path.realpath(__file__))

crashed = False

def initBoard():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def initPygame():
    print("initializing...")
    pygame.init()
    #size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_caption("- Lauren's 3rd Birthday -")
    pygame.mouse.set_visible(False) 
    return pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    #return pygame.display.set_mode(size, pygame.FULLSCREEN)

def showImage(imagePath):
    img = pygame.image.load(imagePath)
    img = pygame.transform.scale(img,(DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen.blit(img,(OFFSET_X, OFFSET_Y))
    #screen.blit(img, img.get_rect())
    pygame.display.flip()

def getFileName():
    fileName = time.strftime("%Y%m%d-%H%M%S.png")
    return fileName

def flash():
    screen.fill(WHITE)
    pygame.display.update()
    
def countdown():
    showImage(REAL_PATH + "/five.png")
    time.sleep(1)
    showImage(REAL_PATH + "/four.png")
    time.sleep(1)
    showImage(REAL_PATH + "/three.png")
    time.sleep(1)
    showImage(REAL_PATH + "/two.png")
    time.sleep(1)
    showImage(REAL_PATH + "/one.png")
    time.sleep(1)

def takePhoto():
    try:
        fileName = REAL_PATH + "/Pictures/" + getFileName()
        camera.hflip = True
        camera.start_preview(fullscreen = False, window = (PREVIEW_X, PREVIEW_Y, PREVIEW_WIDTH, PREVIEW_HEIGHT))
        countdown()
        camera.stop_preview()
        camera.hflip = False
        flash()
        camera.capture(fileName)
        return fileName
    finally:
        print("Done taking photo")

def displayThankYou():
    showImage(REAL_PATH + "/thank-you.png")
    time.sleep(5)
    
def displayTransitionAndGiveUserChanceToPrintPhoto(fileName):
    showImage(REAL_PATH + "/transition.png")
    
    timeNow = time.time()
    startTime = timeNow
    printButtonPressed = False
    
    while not printButtonPressed or timeNow - startTime <= 10:
        isPressed = GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING, timeout=100)
        timeNow = time.time()
        
        if isPressed is None:
            continue

        print("Button pressed")
        printButtonPressed = True
        isPressed = None
        printPhoto(fileName)
    
def displayInstructions():
    showImage(REAL_PATH + "/press-the-button.png")
    
def takeNPhotos(numberOfPhotos):
    files = [None] * numberOfPhotos
    
    for x in range(0, numberOfPhotos):
        files[x] = takePhoto()
    
    # TODO: add photos to template
    
    return REAL_PATH + "/Pictures/template-" + getFileName()

def processImage(fileName):
    putBorderToImage(fileName)
    addLogo(fileName)
    addPinkiePie(fileName)
    addAppleJack(fileName)
    addRarity(fileName)

def putBorderToImage(fileName):
    graphicsmagick = "gm convert " + fileName + " -trim -bordercolor lightpink -border 85x85 " + fileName
    os.system(graphicsmagick)

def addLogo(fileName):
    graphicsmagick = "gm composite -geometry +25+375 mll-logo-300.png " + fileName + " " + fileName
    os.system(graphicsmagick)
    
def addPinkiePie(fileName):
    graphicsmagick = "gm composite -geometry +775+15 pinkie-pie-250.png " + fileName + " " + fileName
    os.system(graphicsmagick)

def addAppleJack(fileName):
    graphicsmagick = "gm composite -geometry +815+425 apple-jack-200.png " + fileName + " " + fileName
    os.system(graphicsmagick)
    
def addRarity(fileName):
    graphicsmagick = "gm composite -geometry +25+15 rarity-200.png " + fileName + " " + fileName
    os.system(graphicsmagick)
    
def printPhoto(fileName):
    printPhotoCommand = "lp -d " + PRINTER + " " + fileName
    print("printing...")
    os.system(printPhotoCommand)
    time.sleep(5)

initBoard()
camera = picamera.PiCamera()
screen = initPygame()
displayInstructions()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
    isPressed = GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING, timeout=100)

    if isPressed is None:
        continue

    print("Button pressed")
    
    isPressed = None
    
    fileName = takePhoto()
    #fileName = takeNPhotos(3)
    print(fileName)
    processImage(fileName)
    showImage(fileName)
    time.sleep(5)
    displayTransitionAndGiveUserChanceToPrintPhoto(fileName)
    displayInstructions()

print("quitting photobooth...")
camera.close()
GPIO.cleanup()
pygame.quit()
quit()
