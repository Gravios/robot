import socket,sys
import pygame
from PIL import Image

# Create a var for storing an IP address:

conf = json5.load(open("conf.json5"))
remote_host = conf["servers"]['vis']['ip']
remote_port = conf["servers"]['vis']['port']


WIDTH = 1280
HEIGHT = 720

# Start PyGame:
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Remote Webcam Viewer')
font = pygame.font.SysFont("Arial", 14)
clock = pygame.time.Clock()
timer = 0
previousImage = ""
image = ""
data = 0

# Main program loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Receive data
    if timer < 1:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((remote_host, remote_port))
        data = client_socket.recv(1024000)
        timer = 30

    else:
        timer -= 1
    previousImage = image

    # Convert image
    try:
        image = Image.fromstring("RGB", (WIDTH, HEIGHT), data)
        image = image.resize((WIDTH, HEIGHT))
        image = pygame.image.frombuffer(image.tostring(), (WIDTH, HEIGHT), "RGB")

    # Interupt
    except:
        image = previousImage
    output = image
    screen.blit(output, (0, 0))
    clock.tick(60)
    pygame.display.flip()
