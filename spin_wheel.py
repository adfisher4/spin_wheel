"""
spin_wheel

Description:
"""

names = ["Charlie", "Lucy", "Linus", "Sally", "Snoopy", "Pattie", "Marcy", "Woodstock", "Pig-Pen", "Schroeder"]

#### ---- SETUP ---- ####

import tsapp
import tsk
import os
import pp
import math
import random
import pygame
import pygame.freetype
from math import radians as rad
pygame.init()

## -- Window and clock stuff -- ##
window = pygame.display.set_mode([850, 850])
center = 425, 425
window.fill((186, 225, 247))
clock = pygame.time.Clock()

## -- Text objects -- ##
font = pygame.freetype.Font("Rancho-Regular.ttf", 50 - len(names))
announce_winner = pygame.freetype.Font("Rancho-Regular.ttf", 100)
announce_winner.size = 100
announce_winner.fgcolor = (164, 57, 153)


## -- Sound objects -- ##
whoosh = pygame.mixer.Sound(os.path.join("sound", "Whoosh.mp3"))
win_sound = pygame.mixer.Sound(os.path.join("sound", "TahDah2.mp3"))
win_sound.set_volume(0.3)

## -- Spin button -- ##
spin_button = tsk.Sprite(os.path.join("image", "SoundPanelOff.png"), 730, 65)
spin_text = pygame.freetype.Font("Archivo-SemiBold.ttf", 25)
spin_text.fgcolor = (255, 255, 255)
box = spin_text.get_rect("SPIN")
text_width = box.width
spin_text_edge = spin_button.center_x - 0.5 * text_width

    
## -- Names/arc range dictionary -- ## 
arc = int(360 / len(names))
last_i = len(names) - 1
arc_list = []
for i in range(len(names)):
    if i == last_i:
        arc_range = (last_i * arc, 360)
    else:
        arc_range = (i * arc, (i + 1) * arc)
    
    arc_list.append((names[i], arc_range))


## -- Radius variables -- ##
r1 = 20
r2 = 800
em_radius = 310 + len(names)*2


#### ---- EMOTE MANAGEMENT ---- ####    
  
emotes = {
    "pink" : {
        "spin" : ["EmoteHappyPink.png", "EmoteNeutralPink.png"],
        "win" : "EmoteVeryHappyPink.png",
        "lose" : ["EmoteVeryUnhappyPink.png", "EmoteUnhappyPink.png", "EmoteNeutralPink.png", "EmoteHappyPink.png"]
            },
    "blue" : {
        "spin": ["EmoteHappyBlue.png", "EmoteNeutralBlue.png"],
        "win" : "EmoteVeryHappyBlue.png",
        "lose" : ["EmoteVeryUnhappyBlue.png", "EmoteUnhappyBlue.png", "EmoteNeutralBlue.png", "EmoteHappyBlue.png"]
             },
    "yellow" : {
        "spin": ["EmoteHappyYellow.png", "EmoteNeutralYellow.png"],
        "win" : "EmoteVeryHappyYellow.png",
        "lose" : ["EmoteVeryUnhappyYellow.png", "EmoteUnhappyYellow.png", "EmoteNeutralYellow.png", "EmoteHappyYellow.png"]
               }
     }

contestant_emotes = []
for i in range(len(arc_list)):
    radian = rad(arc * (i + 0.5))
    
    em_x = int(center[0] + em_radius * math.cos(radian))
    em_y = int(center[1] + em_radius * math.sin(radian))
    if i % 3 == 0:
        color = "pink"
    elif i % 2 == 0:
        color = "blue"
    else:
        color = "yellow"
    image = os.path.join("image", random.choice(emotes[color]["spin"]))
    new_emot = tsk.Sprite(image, 0, 0)
    new_emot.scale = 0.2
    new_emot.center = (em_x, em_y)
    new_emot.draw()
    
    name_index = -1 - i
    contestant_emotes.append((new_emot, color, names[name_index]))

contestant_emotes.reverse()    


#### ---- FUNCTIONS ---- ####
    
def _write_names(emotes_list):
    for i in range(len(emotes_list)-1, -1, -1):
        box = font.get_rect(names[i])
        name_width = box.width
        
        edge = emotes_list[i][0].center_x - 0.5 * name_width
        font.render_to(window, (edge, emotes_list[i][0].center_y + 30), names[i]) 
        
def _draw_lines():
    for i in range(len(names)):
        radian = rad(arc * i)
        radian2 = rad(arc * (i + 1))
        
        x1 = int(center[0] + r2 * math.cos(radian))
        y1 = int(center[1] + r2 * math.sin(radian))
        x2 = int(center[0] + r2 * math.cos(radian2))
        y2 = int(center[1] + r2 * math.sin(radian2))
        pygame.draw.line(window, (48, 57, 138), center, (x1, y1), 3)


def _make_edge():
    pygame.draw.circle(window, (224, 224, 224), center, 600, 380)
    pygame.draw.circle(window, (48, 57, 138), center, 412, 3)
    spin_button.draw()
    spin_text.render_to(window, (spin_text_edge, spin_button.y + 15), "SPIN")
    
def set_wheel():
    _draw_lines()
    _write_names(contestant_emotes)
    _make_edge()
    
def new_round(contestants, start_angle=225):
    window.fill((186, 225, 247))
    for contestant in contestants:
        contestant[0].image = os.path.join("image", random.choice(emotes[contestant[1]]["spin"]))
        contestant[0].draw()
    arrow.angle = start_angle
    set_wheel()

def get_winner():
    winner = random.choice(names)
    for entry in arc_list:
        if winner == entry[0]:
            low = entry[1][0] + int(.33 * arc)
            high = entry[1][1] - int(.33 * arc)
            winning_angle_360 = random.randint(low, high)
            #print(low, high)
            break
    winning_angle = random.choice([1080, 1440, 1800]) + winning_angle_360
    
    return (winner, winning_angle, winning_angle_360)
    
set_wheel()

## -- Hub and arrow sprites -- ##

hub_image = os.path.join("image", "OrbGreen.png")
hub = tsk.Sprite(hub_image, 0, 0)
hub.center = center
hub.draw()
arrow_image = os.path.join("image", "MouseCursorShadow.png")
arrow = tsk.Sprite(arrow_image, 0, 0)
arrow.center = center
arrow.angle = 225
arrow.draw() 
pygame.display.flip()

# Loop variables
running = True
spinning = False
last_winning_angle = arrow.angle

#### ---- MAIN LOOP ---- ####
while running:
    x, y = pygame.mouse.get_pos()
    
    ## -- Pre-spin event loop -- ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and spin_button.rect.collidepoint(x, y):
            spinning = True
            winner, winning_angle, winning_angle_360 = get_winner()
            new_round(contestant_emotes, last_winning_angle)
            last_winning_angle = winning_angle_360 - 131
            whoosh.play()
            
    ## -- Spin loop -- ##
    while spinning:
        while arrow.angle < winning_angle - 131:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    
            arrow.angle += 8 - 8 * (arrow.angle / winning_angle)
            hub.draw()
            arrow.draw()
            pygame.display.flip()
            clock.tick(60)
            
        ## -- Draw losers -- ##
        winning_contestant = contestant_emotes[names.index(winner)]
        for contestant in contestant_emotes:
            if contestant != winning_contestant:
                contestant[0].image = os.path.join("image", random.choice(emotes[contestant[1]]["lose"]))
                contestant[0].draw()
    
        ## -- Spin ends / winner revealed -- ##
        winning_contestant[0].image = os.path.join("image", emotes[winning_contestant[1]]["win"])
        winning_contestant[0].draw()
        win_sound.play() 
        box = announce_winner.get_rect(winner + " wins!!")
        announce_winner_edge = center[0] - 0.5 * box.width
        announce_winner.render_to(window, (announce_winner_edge, center[1] - 150), winner + " wins!!")
        pygame.display.flip()      
        spinning = False
         