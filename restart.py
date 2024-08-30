import sys
import subprocess
import pygame

python = sys.executable

def restart_game_no():
    pygame.quit()  
    subprocess.run([python] + sys.argv)
    sys.exit()

def restart_game(successful_parkings):
    pygame.quit()  
    subprocess.run([python] + sys.argv + [str(successful_parkings)])
    sys.exit()
