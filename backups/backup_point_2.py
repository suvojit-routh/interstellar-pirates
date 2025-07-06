import pygame
import random
import json,os
from math import sin
from pygame.locals import *
from scripts.galaxy_planet import *
from scripts.state import *
from scripts.space import *
from time import time, tzname
from datetime import datetime, timedelta
from pypresence import Presence
from tzlocal import get_localzone
import threading
import cv2

# Initialize Pygame
pygame.init()

# Your Discord Client ID for Rich Presence
CLIENT_ID = "1336805715767070740"

# Create an instance of the Presence class
rpc = Presence(CLIENT_ID)

# Function to update the Discord Rich Presence
def update_rich_presence():
    try:
        rpc.connect()
        continent = str(get_localzone()).split('/')[0]  # Get the local timezone
        # Update the rich presence with state and details
        rpc.update(state=continent, details="Exploring The Galaxy", large_image="logo", large_text="Interstellar Pirates", start=time())
    except Exception as e:
        print("Error updating Rich Presence:", e)

# Start the Discord Rich Presence update in a separate thread
threading.Thread(target=update_rich_presence, daemon=True).start()

#GAME DATA
game_data = {
        "spaceship": 0,
        "jade": 0,
        "gold": 0,
        "xeroship_owned": False,
        "zenoship_owned": False,
        "furryship_owned" : False,
        "iron": 0,
        "copper": 0,
        "silver": 0,
        "coal": 0,
        "platinum": 0,
        "frost crystal" : 0,
        "lavastone" : 0,
        "purple gemstone" : 0,
        "emerald" : 0,
        "gold" : 0,
        "iridium" : 0,
        "gold_ore" : 0,
        "fuel" : 0,


  "upgrades" : {
  "plasma_cannon" : 0,
  "laser_beam" : 0,
  "launch_thruster" : 0,
  "life_thruster" : 0
  },
  "defaultship_equipment" : {
  "plasma_cannon" : False,
  "laser_beam" : False,
  "launch_thruster" : False,
  "life_thruster" : False
  },
  "xeroship_equipment" : {
  "plasma_cannon" : False,
  "laser_beam" : False,
  "launch_thruster" : False,
  "life_thruster" : False
  },
  "zenoship_equipment" : {
  "plasma_cannon" : False,
  "laser_beam" : False,
  "launch_thruster" : False,
  "life_thruster" : False
  },
  "furryship_equipment" : {
  "plasma_cannon" : False,
  "laser_beam" : False,
  "launch_thruster" : False,
  "life_thruster" : False
  },
  "exhaust" : {
  "current_exhaust" : 0,
  "blue_flame_exhaust" : False
  },
  "current_song" : 0,
  "nova_core" : 0,
  "celestial_stone" : 0

    }

#SETTINGS DATA
settings_data = {
    "screen_width" : 1280,
    "screen_height" : 720,
    "sound": {
        "sfx": 10,
        "music": 10,
        "width": 400,
        "height": 40
  }
}

#QUEST DATA 
quest_data = {
    "event" : {
        "pirate_killed": 0,
        "pirates_kills": [100000,False],
        "planet_discovered": 0,
        "planet_discover": [1000,False],
        "boss_killed": 0,
        "boss_kills": [100,False],
        "wormhole_discovered": 0,
        "wormhole_discover": [50,False],
        "meteor_destroyed": 0,
        "meteor_destroy": [10000,False],
        "spacestation_founded": 0,
        "spacestation_found": [20,False]},
    "dailies" :{
        "daily_reset": False,
        "last_reset_day": datetime.now().day,
        "playtime": 0,
        "target_playtime" : [900,False],
        "pirate_killed": 0,
        "pirates_kills": [1000,False],
        "lavastone_obtained" : 0,
        "lavastone_needed" : [2,False],
        "emerald_obtained" : 0,
        "emerald_needed" : [2,False],
        "crafted_item" : 0,
        "craft_needed" : [2,False],
        "wish_completed" : 0,
        "wish_needed" : [2,False]
  }
        
}

#EQUIPMENT DATA
equipment_data = {
  "plasma_cannon": {
    "name": "Plasma Cannon",
    "boost": [1.5, 0, 0], 
    "energy_usage": 10
  },
  "laser_beam": {
    "name": "Laser Beam",
    "boost": [1.2, 0, 0],  
    "energy_usage": 5
  },
  "launch_thruster": {
    "name": "Launch Thruster",
    "boost": [1, 1.5, 0],  
    "energy_usage": 8
  },
  "life_thruster": {
    "name": "Regen Thruster",
    "boost": [0, 0, 5],  
    "energy_usage": 12
  }
}


ships_data = {
    "defaultship": {
        "base_damage": 100,
        "base_health": 5,
        "speed": 5,
        "skill_multiplier": 1,
        "ultimate_multiplier": 1,
        "current_xp" : 0,
        "current_level" : 1,
        "current_max_level" : 10,
        "max_level" : 100
    },
    "xeroship": {
        "base_damage": 250,
        "base_health": 8,
        "speed": 5,
        "skill_multiplier": 1,
        "ultimate_multiplier": 4.0,
        "current_xp" : 0,
        "current_level" : 1,
        "current_max_level" : 10,
        "max_level" : 100
    },
    "zenoship": {
        "base_damage": 400,
        "base_health": 10,
        "speed": 5,
        "skill_multiplier": 1,
        "ultimate_multiplier": 5.0,
        "current_xp" : 0,
        "current_level" : 1,
        "current_max_level" : 10,
        "max_level" : 100
    },
    "furryship": {
        "base_damage": 500,
        "base_health": 15,
        "speed": 0,
        "skill_multiplier": 1,
        "ultimate_multiplier": 8.5,
        "current_xp" : 0,
        "current_level" : 1,
        "current_max_level" : 10,
        "max_level" : 100
    }
}

app_name = "Interstellar Pirates"
roaming_path = os.path.join(os.getenv("APPDATA"), app_name)

# Ensure the directory exists
os.makedirs(roaming_path, exist_ok=True)

# Define the file path
data_path = os.path.join(roaming_path, "data.json")
settings_data_path = os.path.join(roaming_path,"settings.json")
quest_data_path = os.path.join(roaming_path,"quest.json")
equipment_data_path = os.path.join(roaming_path,"equipments.json")
ships_data_path = os.path.join(roaming_path,"ships.json")

    


def load_data(path,data):
    try:
        with open(path, 'r') as data_file:
            loaded_data = json.load(data_file)
            data.update(loaded_data)  
    except (FileNotFoundError, json.JSONDecodeError):
        return data

load_data(data_path,game_data)
load_data(settings_data_path,settings_data)
load_data(quest_data_path,quest_data)
load_data(equipment_data_path,equipment_data)
load_data(ships_data_path,ships_data)


#Saving all the data
def save_data(path,data):
    with open(path,'w') as data_file:
        json.dump(data,data_file,indent =2)

def save_all_data():
    save_data(data_path,game_data)
    save_data(settings_data_path,settings_data)
    save_data(quest_data_path,quest_data)
    save_data(equipment_data_path,equipment_data)
    save_data(ships_data_path,ships_data)



#GAME SETTINGS
screen_width = settings_data["screen_width"]
screen_height = settings_data["screen_height"]
screen = pygame.display.set_mode((screen_width, screen_height))               
clock = pygame.time.Clock()
pygame.display.set_caption('Interstellar Pirate')
pygame.display.set_icon(pygame.image.load("icon.png"))
font = pygame.font.Font('font/subatomic.ttf', 12)



#GAME VARRIABLES
start_time = time()
score = 0
loading_time = 0
defaultship_owned = True
scroll_speed = 8
pirate_count = 8
slot_one = game_data['spaceship']
slot_two = None
saved_ship = game_data['spaceship']
fuel_warning_triggered = False
oxygen_warning_triggered = False
radiation_warning_triggered = False
upgrade_instance = None


# SHIP ATTRIBUES
health = 5
speed = 5
aa_damage = 0
skill_damage = 0
ultimate_damage = 0






def health_amount():
    global game_data, health
    ship_keys = ["defaultship_equipment", "xeroship_equipment", "zenoship_equipment", "furryship_equipment"]
    current_ship = game_data["spaceship"]
    current_equipment = game_data[ship_keys[current_ship]]
    data_index = [ships_data["defaultship"]["base_health"],ships_data["xeroship"]["base_health"],ships_data["zenoship"]["base_health"],ships_data["furryship"]["base_health"]]

    # Base health depending on ship
    if current_ship == 0:
        health = data_index[0]
    elif current_ship == 1:
        health = data_index[1]
    elif current_ship == 2:
        health = data_index[2]
    elif current_ship == 3:
        health = data_index[3]

    # If life_thruster is equipped, add its bonus
    if current_equipment.get("life_thruster", False):
        health += equipment_data["life_thruster"]["boost"][2]

def speed_amount():
    global game_data, speed
    ship_keys = ["defaultship_equipment", "xeroship_equipment", "zenoship_equipment", "furryship_equipment"]
    current_ship = game_data["spaceship"]
    current_equipment = game_data[ship_keys[current_ship]]
    data_index = [ships_data["defaultship"]["speed"],ships_data["xeroship"]["speed"],ships_data["zenoship"]["speed"],ships_data["furryship"]["speed"]]

    # Base health depending on ship
    if current_ship == 0:
        speed = data_index[0]
    elif current_ship == 1:
        speed = data_index[1]
    elif current_ship == 2:
        speed = data_index[2]
    elif current_ship == 3:
        speed = data_index[3]

    # If life_thruster is equipped, add its bonus
    if current_equipment.get("launch_thruster", False):
        speed *= equipment_data["launch_thruster"]["boost"][1]






def calculate_damage():
    spaceship_index = game_data["spaceship"]
    ship_names = ["defaultship", "xeroship", "zenoship", "furryship"]
    ship_name = ship_names[spaceship_index]
    ship = ships_data[ship_name]

    # Base damage
    base_damage = ship["base_damage"] + ship["current_level"] * 2

    # Equipment damage multiplier
    equipment = game_data[f"{ship_name}_equipment"]
    damage_multiplier = 1
    for item, equipped in equipment.items():
        if equipped:
            boost = equipment_data[item]["boost"][0]
            if boost > 0:  
                damage_multiplier *= boost
    # Final damages
    aa_damage = base_damage * damage_multiplier

    skill_damage = None
    if ship.get("skill_multiplier") is not None:
        skill_damage = aa_damage * ship["skill_multiplier"]

    ultimate_damage = None
    if ship.get("ultimate_multiplier") is not None:
        ultimate_damage = aa_damage * ship["ultimate_multiplier"]

    return {
        "aa_damage": aa_damage,
        "skill_damage": skill_damage,
        "ultimate_damage": ultimate_damage
    }



def update_all_damage():
    global aa_damage, skill_damage, ultimate_damage
    damage_info = calculate_damage()
    aa_damage = int(damage_info["aa_damage"])   
    skill_damage = int(damage_info["skill_damage"]) 
    ultimate_damage = int(damage_info["ultimate_damage"])   



#PIRATE CLASS PROPERTY
pirate_num = random.randrange(1,26)


#EFFECTS
boom_effect = pygame.image.load('graphics/effects/4.png').convert_alpha()
boom_surf = pygame.transform.scale(boom_effect, (128,128))
boom_effect2 = pygame.image.load('graphics/effects/4.png').convert_alpha()
boom_surf2 = pygame.transform.scale(boom_effect2, (200,200))

# SOUNDS
pygame.mixer.set_num_channels(16) 
laser_sound = pygame.mixer.Sound('Sound/SFX/laser.wav')
laser_channel = pygame.mixer.Channel(0)

click_sound = pygame.mixer.Sound('Sound/SFX/click.flac')
explosion_sound = pygame.mixer.Sound('Sound/SFX/explosion.wav')
teleport_sound = pygame.mixer.Sound('Sound/SFX/teleport.ogg')
planet_sound = pygame.mixer.Sound('Sound/SFX/planet.wav')
chest_opening_sound = pygame.mixer.Sound('Sound/SFX/chest_opening.mp3')
sfx_channel = pygame.mixer.Channel(1)




#WARNING VOICES
fuel_warning = pygame.mixer.Sound('Sound/WARNINGS/fuel_warning.wav')
oxygen_warning = pygame.mixer.Sound('Sound/WARNINGS/oxygen_warning.wav')
radiation_warning = pygame.mixer.Sound('Sound/WARNINGS/radiation_warning.wav')
warning_channel = pygame.mixer.Channel(2)

#BGM
menu_music_list = ["Cosmic Flight","Gravity of Stars","Beyond the Stars","Neon Heartbeat","Chasing Electric Nights","Galaxies Apart"]
menu_music = pygame.mixer.Sound(f'Sound/BGM/Menu Music/{menu_music_list[game_data["current_song"]]}.mp3')
boss_music = pygame.mixer.Sound("Sound/BGM/space_boss.ogg")
music_channel = pygame.mixer.Channel(3)

def volume_adjustment():
    global settings_data
    music_channel.set_volume(settings_data["sound"]["music"]/100)
    sfx_channel.set_volume(settings_data["sound"]["sfx"]/100)
    laser_channel.set_volume(settings_data["sound"]["sfx"]/100)
    warning_channel.set_volume(settings_data["sound"]["sfx"] / 50)





#TAB MENU SPACESHIP
default_ship_tab = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship3.png'), (350,350)).convert_alpha()
xeroship_tab = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship.png'), (350,350)).convert_alpha()
zenoship_tab = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship4.png'), (350,350)).convert_alpha()
furryship_tab = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship5.png'), (350,350)).convert_alpha()

#TEMPLATES
selection_template = pygame.transform.scale(pygame.image.load('graphics/Templates/selection_bg.png'),(400,400)).convert_alpha()

# ASSETS BGS
shop_bg = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/1.png'), (screen_width,screen_height)).convert_alpha()
inventory_bg = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/2.png'), (screen_width,screen_height)).convert_alpha()
pause_bg = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/3.png'), (screen_width,screen_height)).convert_alpha()
settings_bg = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/4.png'), (screen_width,screen_height)).convert_alpha()
gacha_menu_bg = pygame.image.load('graphics/Asset_bg/5.png').convert_alpha()
event_bg = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/7.png'), (screen_width,screen_height)).convert_alpha()
# SHOP OBJECTS 
xeroship_buy_surf = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship.png'), (125,125)).convert_alpha()
blue_exhaust_buy_surf = pygame.transform.scale(pygame.image.load('graphics/exhaust/blue_flame.png'), (125,125)).convert_alpha()
jade_buy_surf = pygame.transform.scale(pygame.image.load('graphics/Objects/crystal.png'), (125,125)).convert_alpha()
gold_buy_surf = pygame.transform.scale(pygame.image.load('graphics/Objects/gold.png'), (125,125)).convert_alpha()
emerald_buy_surf = pygame.transform.scale(pygame.image.load('graphics/Ores/emerald.png'), (125,125)).convert_alpha() 
purple_gemstone_buy_surf = pygame.transform.scale(pygame.image.load('graphics/Ores/purple gemstone.png'), (125,125)).convert_alpha()

#BOTTOMBAR ICONS
jade_icon = pygame.transform.scale(pygame.image.load('graphics/Objects/crystal_red.png'), (50,50)).convert_alpha()
gold_icon = pygame.transform.scale(pygame.image.load('graphics/Objects/gold.png'), (50,50)).convert_alpha()
fuel_icon = pygame.transform.scale(pygame.image.load('graphics/Objects/fuel.png'), (40,50)).convert_alpha()
gold_ore_icon = pygame.transform.scale(pygame.image.load('graphics/Ores/gold.png'), (50,50)).convert_alpha()
emerald_icon = pygame.transform.scale(pygame.image.load('graphics/Ores/emerald.png'), (50,50)).convert_alpha() 
purple_gemstone_icon = pygame.transform.scale(pygame.image.load('graphics/Ores/purple gemstone.png'), (50,50)).convert_alpha()
test = pygame.image.load('graphics/1.png').convert_alpha()

#SPACESHIPS
default_ship = pygame.image.load('graphics/Spaceship/ship3.png').convert_alpha()
xero_ship = pygame.image.load('graphics/Spaceship/ship.png').convert_alpha()
zeno_ship = pygame.image.load('graphics/Spaceship/ship4.png').convert_alpha()
furry_ship = pygame.image.load('graphics/Spaceship/ship5.png').convert_alpha()


#SPACESHIPS INV
default_ship_inv = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship3.png'), (75,75)).convert_alpha()
xeroship_inv = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship.png'), (75,75)).convert_alpha()
zenoship_inv = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship4.png'), (75,75)).convert_alpha()
furryship_inv = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship5.png'), (75,75)).convert_alpha()
# EXHAUST INV
default_exhaust_inv = pygame.transform.scale(pygame.image.load('graphics/exhaust/red_flame.png'), (75,75)).convert_alpha()
blueflame_exhaust_inv = pygame.transform.scale(pygame.image.load('graphics/exhaust/blue_flame.png'), (75,75)).convert_alpha()

#SPACESHIP SELECTION PAGE
default_ship_sel = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship3.png'), (300,300)).convert_alpha()
xeroship_sel = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship.png'), (300,300)).convert_alpha()
zenoship_sel = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship4.png'), (300,300)).convert_alpha()
furryship_sel = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship5.png'), (300,300)).convert_alpha()

# SPACESHIP BUTTON FOR SELECTION
default_ship_bttn = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship3.png'), (150,150)).convert_alpha()
xeroship_bttn = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship.png'), (150,150)).convert_alpha()
zenoship_bttn = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship4.png'), (150,150)).convert_alpha()
furryship_bttn = pygame.transform.scale(pygame.image.load('graphics/Spaceship/ship5.png'), (150,150)).convert_alpha()

#ITEMS INV
copper_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/copper.png'), (100,100)).convert_alpha()
coal_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/coal.png'), (100,100)).convert_alpha()
iron_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/iron.png'), (100,100)).convert_alpha()
silver_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/silver.png'), (100,100)).convert_alpha()
lavastone_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/lavastone.png'), (100,100)).convert_alpha()
platinum_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/platinum.png'), (100,100)).convert_alpha()
frost_crystal_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/frost crystal.png'), (100,100)).convert_alpha()
emerald_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/emerald.png'), (100,100)).convert_alpha()
purple_gemstone_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/purple gemstone.png'), (100,100)).convert_alpha()
iridium_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/iridium.png'), (100,100)).convert_alpha()
gold_inv = pygame.transform.scale(pygame.image.load('graphics/Ores/gold.png'), (100,100)).convert_alpha()
fuel_inv = fuel_craft = pygame.transform.scale(pygame.image.load('graphics/Objects/fuel.png'),(100,120)).convert_alpha()
# CRAFTING INV
fuel_craft = pygame.transform.scale(pygame.image.load('graphics/Objects/fuel.png'),(100,120)).convert_alpha()
coin_craft = pygame.transform.scale(pygame.image.load('graphics/Objects/gold.png'),(100,100)).convert_alpha()

#GACHA PRIZES
furryship_gacha_banner = pygame.transform.smoothscale(pygame.image.load('graphics/Spaceship/ship5.png'), (350,350)).convert_alpha()
zenoship_gacha_banner = pygame.transform.smoothscale(pygame.image.load('graphics/Spaceship/ship4.png'), (350,350)).convert_alpha()

#FONTS
gui_font = pygame.font.Font('font/LM.otf', 20)
item_gui_font = pygame.font.Font('font/LM.otf', 16)

#STATE AND RANDOM THINGS
# state = 'menu'
random_galaxy = "Lisa Galaxy"
random_planet = random.choice(planet_names)



# DISPLAY FUNCTIONS
def display_letters(text,pos_x,pos_y,size,color):
    letters_font = pygame.font.Font('font/LM.otf', size)
    letter_text = letters_font.render(text,True, (color))
    screen.blit(letter_text,(pos_x,pos_y))

def middle_letters(text,pos_x,pos_y,size,color):
    middle_font = pygame.font.Font('font/LM.otf', size)
    middle_text = middle_font.render(text,True, (color))
    middle_x = (screen.get_width()- middle_text.get_width())//2 
    middle_y = (screen.get_height()- middle_text.get_height()) // 2
    screen.blit(middle_text,(middle_x - pos_x,middle_y -  pos_y))


def display_score(score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))


def display_fstring(text,color,pos_x,pos_y):
    new_text = font.render(text,True,(color))
    screen.blit(new_text,(pos_x,pos_y))



def game_modes():
    menu_background_group.draw(screen)
    menu_background_group.update()

def header(text,text_color = 'black',rect_color = 'white',outline_color = 'black',font_size = 40,y_pos = 20):
    font = pygame.font.Font('font/gacha.ttf',font_size)
    text = font.render(text, True, text_color)
    text_width = text.get_width()
    text_height = text.get_height()
    pos_x = (screen.get_width() - text_width)//2
    pos_y = y_pos
    gap = 4
    pygame.draw.rect(screen,rect_color,[pos_x - gap,pos_y - gap,text_width + gap *2,text_height + gap*2],border_radius = 8)
    pygame.draw.rect(screen,outline_color,[pos_x - gap,pos_y - gap,text_width + gap *2,text_height + gap*2],border_radius = 8,width = 2)
    screen.blit(text,(pos_x,pos_y +2))


#LOADING ANIMATION FUNCTION
def loading_animation(update):
    screen.fill('black')
    loading_update = update
    loading_text = font.render(loading_update,True,'white')
    pos_x = (screen.get_width() - loading_text.get_width())//2
    pos_y = (screen.get_height() - loading_text.get_height()) // 2
    loading_rect = loading_text.get_rect(topleft = (pos_x,pos_y))
    screen.blit(loading_text,loading_rect)
    pygame.draw.rect(screen,('red'),loading_rect.inflate(100,30), width = 5 , border_radius = 20)



# LOAD PICTURES FOR BUTTON
backward_btn_img = pygame.transform.scale(pygame.image.load('graphics/Buttons/Backward_BTN.png'), (64,64)).convert_alpha()
forward_btn_img = pygame.transform.scale(pygame.image.load('graphics/Buttons/Forward_BTN.png'), (64,64)).convert_alpha()
music_increase = pygame.transform.scale(pygame.image.load('graphics/Buttons/music_increse.png'), (50,50)).convert_alpha()
music_decrease = pygame.transform.scale(pygame.image.load('graphics/Buttons/music_decrease.png'), (50,50)).convert_alpha()
sfx_increase = pygame.transform.scale(pygame.image.load('graphics/Buttons/sfx_increase.png'), (50,50)).convert_alpha()
sfx_decrease = pygame.transform.scale(pygame.image.load('graphics/Buttons/sfx_decrease.png'), (50,50)).convert_alpha()
o2_refill_button = pygame.transform.scale(pygame.image.load('graphics/Buttons/o2_refill.png'), (200,60)).convert_alpha()
fuel_refill_button = pygame.transform.scale(pygame.image.load('graphics/Buttons/fuel_refill.png'), (200,60)).convert_alpha()
ba_refill_button = pygame.transform.scale(pygame.image.load('graphics/Buttons/ba_refill.png'), (200,60)).convert_alpha()
add_icon =  pygame.transform.scale(pygame.image.load('graphics/Templates/add_icon.png'), (200,200)).convert_alpha()
craft_button_template = pygame.transform.scale(pygame.image.load('graphics/Buttons/btn_template.png'), (160,45)).convert_alpha()

# PICTURE BUTTONS
class Picture_Button:
    def __init__(self,surface,x,y,image):
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))
        self.clicked = False
        self.surface = surface
        self.font = pygame.font.Font('Font/LM.otf',15)

    def hover(self,text,color):
        self.text = text
        self.color = color
        self.text_surf = self.font.render(self.text,True,self.color)
        self.text_width = self.text_surf.get_width()
        self.text_height = self.text_surf.get_height()
        self.gap = 4
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(self.surface,'black',[self.rect.x + 10 - self.gap ,self.rect.y - 25 - self.gap ,self.text_width + self.gap*2,self.text_height + self.gap*2], border_radius = 10)
            self.surface.blit(self.text_surf,(self.rect.x + 10,self.rect.y - 25))

    def below_hover(self,text,color,adjustment):
        self.text = text
        self.color = color
        self.adjustment = adjustment
        self.text_surf = self.font.render(self.text,True,self.color)
        self.text_width = self.text_surf.get_width()
        self.text_height = self.text_surf.get_height()
        self.gap = 4
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(self.surface,'black',[self.rect.x + 10 - self.gap - self.adjustment ,self.rect.y + self.image.get_height() + 10 - self.gap ,self.text_width + self.gap*2,self.text_height + self.gap*2], border_radius = 10)
            self.surface.blit(self.text_surf,(self.rect.x + 10 - self.adjustment,self.rect.y + self.image.get_height() + 10))


    
        
    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                sfx_channel.play(click_sound)
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        self.surface.blit(self.image,(self.rect.x ,self.rect.y ))
        return action

backward_btn = Picture_Button(screen,30,screen_height - 74,backward_btn_img)
forward_btn = Picture_Button(screen,screen.get_width() - 94 ,screen_height - 74,forward_btn_img)
add_icon_btn = Picture_Button(screen,screen.get_width() - (screen.get_width()*0.15 + 200),(screen.get_height()-200)//2,add_icon)



# BUTTONS CLASS
mouse_released = True

class Rect_Button:
    def __init__(self, display, width, height, pos_x, pos_y, text, rect_color, hover_color, text_color, font_size=35, border_color="black", visibility=True):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.display = display
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color
        self.rect_color = rect_color
        self.color = rect_color
        self.border_color = border_color
        self.visibility = visibility
        self.image = pygame.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.font_size = font_size
        self.font = pygame.font.Font('font/gacha.ttf', self.font_size)
        self.hover_font = pygame.font.Font('font/subatomic.ttf', 20)

        

    def draw(self, radius=8):
        global mouse_released

        action = False
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.image.collidepoint(pos):
            pygame.draw.rect(self.display, self.rect_color, self.image, border_radius=radius)
            self.rect_color = self.hover_color
            if mouse_pressed and mouse_released:  # Only trigger if mouse is released
                mouse_released = False  # Lock further clicks
                action = True
                sfx_channel.play(click_sound)
        else:
            self.rect_color = self.color


        if not mouse_pressed:
            mouse_released = True

        if self.visibility:
            pygame.draw.rect(self.display, self.rect_color, self.image, border_radius=radius)
        

        pygame.draw.rect(self.display, self.border_color, self.image, width=1, border_radius=radius)

        text = self.font.render(self.text, True, self.text_color)
        text_pos_x = self.pos_x + (self.width - text.get_width()) // 2
        text_pos_y = self.pos_y + (self.height - text.get_height()) // 2
        self.display.blit(text, (text_pos_x, text_pos_y + 2))
        return action

    def hover(self,hover_text,side,adjustment):
        self.font2 = pygame.font.Font('font/gacha.ttf', 20)
        self.hover_text = self.font2.render(hover_text,True,'white')
        self.text_width = self.hover_text.get_width()
        self.text_height = self.hover_text.get_height()
        self.side = side
        self.below_x = self.pos_x + (self.width - self.text_width) //2
        self.below_y = self.pos_y + (self.height + adjustment)
        self.right_x = self.pos_x + (self.width + adjustment)
        self.right_y = self.pos_y + (self.height - self.text_height)//2
        self.gap = 5
        mouse_pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked condition
        if self.image.collidepoint(mouse_pos):
            if self.side == 'below':
                pygame.draw.rect(screen,'black',[self.below_x - self.gap,self.below_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.below_x - self.gap,self.below_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.below_x,self.below_y+2))
            if self.side == 'right':
                pygame.draw.rect(screen,'black',[self.right_x - self.gap,self.right_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.right_x - self.gap,self.right_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.right_x,self.right_y+2))

# JOUNEY_BUTTONS
dailies_button = Rect_Button(screen,120,30,10,100,"Dailies","#FFFFFF","#FFC107","black",25)
event_button = Rect_Button(screen,120,30,10,200,"Event","#FFFFFF","#FFC107","black",25)
# all the back buttons
menu_btn = Rect_Button(screen,80,30,10,screen_height - 40,"Menu","white","#00ffa6","black",20,"black")
menu_back_button = Rect_Button(screen,80,30,10,screen_height - 40,"Back","white","#00ff79","black",20,"black")
modes_back_button = Rect_Button(screen,80,30,10,screen_height - 40,"Back","white","#00ff79","black",20,"black")
shop_back_button = Rect_Button(screen,80,30,10,screen_height - 40,"Back","white","#00ff79","black",20,"black")
gacha_back_button = Rect_Button(screen,80,30,10,screen_height - 40,"Back","white","#00ff79","black",20,"black")
gacha_button = Rect_Button(screen,80,30,screen_width - 90,screen_height - 40,"Wish","white","#00ff79","black",20,"black")
leave_button = Rect_Button(screen,80,30,10,screen_height - 40,"Leave","white","#00ff79","black",20,"black")
#sound buttons and sound_bar
music_cal_x = (screen.get_width() - settings_data["sound"]["width"])//2
music_cal_y = 250 
music_dec_x = music_cal_x - 60
music_inc_x = (music_cal_x + settings_data["sound"]["width"]) + 20
sfx_y = 450 

music_increase_btn = Rect_Button(screen,40,40,music_inc_x,music_cal_y,'+','lightslateblue','yellow','black')
music_decrease_btn = Rect_Button(screen,40,40,music_dec_x,music_cal_y,'-','lightslateblue','yellow','black')

sfx_increase_btn = Rect_Button(screen,40,40,music_inc_x,sfx_y,'+','lightslateblue','yellow','black')
sfx_decrease_btn = Rect_Button(screen,40,40,music_dec_x,sfx_y,'-','lightslateblue','yellow','black')

#GACHA BUTTONS
single_pull_btn = Rect_Button(screen,200,60,(screen.get_width() - 200)// 2 - 200,(screen.get_height() - 200) ,'WISH x1','red','yellow','black')
multi_pull_btn = Rect_Button(screen,200,60,(screen.get_width() - 200)// 2 + 200,(screen.get_height() - 200) ,'WISH x10','red','yellow','black')



# INVENTORY BUTTONS
default_ship_enable = Rect_Button(screen,100,30,450,220,'ENABLE','green','red','black',20)
xeroship_enable = Rect_Button(screen,100,30,650,220,'ENABLE','green','red','black',20)
zenoship_enable = Rect_Button(screen,100,30,850,220,'ENABLE','green','red','black',20)
furryship_enable = Rect_Button(screen,100,30,1050,220,'ENABLE','green','red','black',20)

default_ship_enabled = Rect_Button(screen,100,30,450,220,'ENABLED','white','cyan','black',20)
xeroship_enabled = Rect_Button(screen,100,30,650,220,'ENABLED','white','cyan','black',20)
zenoship_enabled = Rect_Button(screen,100,30,850,220,'ENABLED','white','cyan','black',20)
furryship_enabled = Rect_Button(screen,100,30,1050,220,'ENABLED','white','cyan','black',20)


xeroship_na = Rect_Button(screen,100,30,650,220,'NA','white','cyan','black',20)
zenoship_na = Rect_Button(screen,100,30,850,220,'NA','white','cyan','black',20)
furryship_na = Rect_Button(screen,100,30,1050,220,'NA','white','cyan','black',20)

#exhaust enable buttons
default_exhaust_enable = Rect_Button(screen,100,30,450,220,'ENABLE','green','red','black',20)
default_exhaust_enabled = Rect_Button(screen,100,30,450,220,'ENABLED','white','cyan','black',20)

blueflame_exhaust_enable = Rect_Button(screen,100,30,650,220,'ENABLE','green','red','black',20)
blueflame_exhaust_enabled = Rect_Button(screen,100,30,650,220,'ENABLED','white','cyan','black',20)
blueflame_exhaust_na = Rect_Button(screen,100,30,650,220,'NA','green','red','black',20)

# SHOP BUTTONS
shop_rect_width = 200
shop_rect_height = 200
item_spacing = (screen.get_width() - 4 * shop_rect_width) // 5
shop_variables = [shop_rect_width,shop_rect_height,item_spacing]
# x pos
first_item_x = item_spacing * 1 + shop_rect_width * 0
second_item_x = item_spacing * 2 + shop_rect_width * 1
third_item_x = item_spacing * 3 + shop_rect_width * 2
forth_item_x = item_spacing * 4 + shop_rect_width * 3

buy_jade_button = Rect_Button(screen,200,60,first_item_x,290,'BUY JADE','yellow','red','black')
buy_gold_button = Rect_Button(screen,200,60,second_item_x,290,"BUY GOLD",'yellow','red','black')
buy_xeroship_button = Rect_Button(screen,200,60,third_item_x,290,'BUY','yellow','red','black')
buy_blue_exxhaust = Rect_Button(screen,200,60,forth_item_x,290,'BUY','yellow','red','black')
exchange_emerald_button = Rect_Button(screen,200,60,first_item_x,290,'EXCHANGE','yellow','red','black')
exchange_gemstone_button = Rect_Button(screen,200,60,second_item_x,290,'EXCHANGE','yellow','red','black')
unavailable_exchange_button = Rect_Button(screen,200,60,first_item_x,290,'UNAVIALABLE','yellow','red','black',30)
unavailable_exchange_button2 = Rect_Button(screen,200,60,second_item_x,290,'UNAVIALABLE','yellow','red','black',30)
unavailable_jade_button = Rect_Button(screen,200,60,first_item_x,290,'UNAVIALABLE','yellow','red','black',30)
unavailable_gold_button = Rect_Button(screen,200,60,second_item_x,290,'UNAVIALABLE','yellow','red','black',30)
# SOLD OUT NA BUTTONS
sold_xeroship_button = Rect_Button(screen,200,60,third_item_x,290,'SOLD OUT','white','red','black',35)
sold_blue_exhaust_button = Rect_Button(screen,200,60,forth_item_x,290,'SOLD OUT','white','red','black',35)
unavailable_xeroship_button = Rect_Button(screen,200,60,third_item_x,290,'UNAVIALABLE','yellow','red','black',30)
unavailable_blue_exhaust_button = Rect_Button(screen,200,60,forth_item_x,290,'UNAVIALABLE','yellow','red','black',30)

#DISPLAY SETTINGS BUTTONS
display_button_x = (screen.get_width() - 200)//2
seven_sixty_eight_button = Rect_Button(screen,200,60,display_button_x,200,'1368 x 768','mediumspringgreen','cyan','black',25)
seven_twenty_button = Rect_Button(screen,200,60,display_button_x,400,'1280 x 720','mediumspringgreen','cyan','black',25)
# SETTING BUTTONS
sound_button = Rect_Button(screen,200,60,50,50,'Sound','yellow','red','black')
display_button = Rect_Button(screen,200,60,50,150,'Display','yellow','red','black')
# INVENTORY BUTTONS
items_button = Rect_Button(screen,200,60,50,50,'Items','yellow','red','black')
ships_button = Rect_Button(screen,200,60,50,150,'Ships','yellow','red','black')
upgrades_button = Rect_Button(screen,200,60,50,250,"Upgrade",'yellow','red','black')
exhaust_button = Rect_Button(screen,200,60,50,350,'Exhaust','yellow','red','black')
crafting_button = Rect_Button(screen,200,60,50,450,'Crafting','yellow','red','black')

#craft buttons
craft_button_x = screen.get_width() * 0.28125
gold_craft_btn = Rect_Button(screen,150,45,craft_button_x,320,"Craft","green",'yellow','black')
fuel_craft_btn = Rect_Button(screen,150,45,craft_button_x*2,320,"Craft","green",'yellow','black')
#item inventory buttons
item_inv_btn_x = (screen.get_width() - 100)//2
item_inv_btn_y = screen.get_height() - 40
next_button = Rect_Button(screen,100,30,item_inv_btn_x,item_inv_btn_y,'Next','yellow','red','black',20)
previous_button = Rect_Button(screen,100,30,item_inv_btn_x,item_inv_btn_y,'Prev','yellow','red','black',20)

# PAUSE MENU BUTTONS
resume_button = Rect_Button(screen, 200 , 60 , 100,100 , 'Resume' , 'pink' , 'magenta' , 'black')
menu_button = Rect_Button(screen, 200 , 60 , 100,200 , 'Menu' , 'pink' , 'magenta' , 'black')
# MAIN MENU BUTTONS
class Button:
    def __init__(self,text,width,height,pos,state,elevation,action,result,bought,sold,original_top,top_color,bottom_color,text_color,hover_color):
        self.state = state
        self.click = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_ypos = pos[1]
        self.action = action
        self.result = result
        self.bought = bought
        self.sold = sold
        self.time = 0
        self.cooldown = 5

        #toprect and rect color
        self.top_rect = pygame.Rect(pos,(width,height))
        self.original_top = original_top
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.text_color = text_color
        self.hover_color = hover_color

        #bottom rect
        self.bottom_rect = pygame.Rect(pos,(width,elevation))

        #text and text rect
        self.text_surf = gui_font.render(text,True,self.text_color)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.original_ypos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(screen,self.bottom_color,self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color,self.top_rect,border_radius = 12)
        screen.blit(self.text_surf,self.text_rect)
        self.clicks()

    def clicks(self):
        global state, game_data
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.hover_color
            self.dynamic_elevation = 0
            if pygame.mouse.get_pressed()[0] and not self.click and self.time == 0:
                sfx_channel.play(click_sound)
                state = self.state
                self.cooldown-=1
                if self.cooldown == self.time:
                    if self.action is not None:
                        self.cooldown = 5
                        game_data[self.sold] -= self.action
                        game_data[self.bought] += self.result
                        self.click = True

                self.click = True
            else:
                if self.click:
                    self.dynamic_elevation = self.elevation
                    self.click = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.original_top




# MENU BUTTONS
game_mode_button = Button('Game Modes',200,60,((screen.get_width() - 200)//2,100),State.MODES,6,None,None,None,None,'magenta','magenta','gray','black','cyan')
journey_button = Button('Journey',200,60,((screen.get_width() - 200)//2,400),State.JOURNEY ,6,None,None,None,None,'magenta','magenta','gray','black','cyan')
inventory_button = Button('Inventory',200,60,((screen.get_width() - 200)//2,300),State.ITEMS_INV,6,None,None,None,None,'magenta','magenta','gray','black','cyan')
shop_button = Button('Shop',200,60,((screen.get_width() - 200)//2,200),State.SHOP,6,None,None,None,None,'magenta','magenta','gray','black','cyan')
settings_button = Button('Settings',200,60,((screen.get_width() - 200)//2,500),State.SETTINGS,6,None,None,None,None,'magenta','magenta','gray','black','cyan')
quit_button = Button('Quit',200,60,((screen.get_width() - 200)//2,600),State.QUIT,6,None,None,None,None,'magenta','magenta','gray','black','cyan')
infinity_button = Button('Infinity Mode',200,60,(100,100),State.SELECTION,6,None,None,None,None,'white','white','gray','black','orangered')
campaign_button = Button('Campaign Mode',200,60,(100,200),State.CAMPAIGN,6,None,None,None,None,'white','white','gray','black','orangered')
research_button = Button('Research',200,60,(100,300),State.RESEARCH,6,None,None,None,None,'white','white','gray','black','orangered')

yes_button = Button('Yes',80,30,((screen.get_width() - 80)//2 - 100,(screen.get_height() - 30)//2),State.PLANETERY_LOADING,6,None,None,None,None,'yellow','yellow','gray','black','red')
no_button = Button('No',80,30,((screen.get_width() - 80)//2  + 100,(screen.get_height() - 30)//2),State.LOADING,6,None,None,None,None,'yellow','yellow','gray','black','red')
#ACTION BUTTONS WITH MENU BUTTON







o2_refill_btn = Rect_Button(screen,200,60,screen_width - 210,(screen.get_height() - 500) // 2 + 40 ,"O2 Refill","white","cyan","black",30)
fuel_refill_btn = Rect_Button(screen,200,60,screen_width - 210,(screen.get_height() - 500) // 2 + 130 ,"FUEL REFILL","white","cyan","black",30)
ba_refill_btn = Rect_Button(screen,200,60,screen_width - 210,(screen.get_height() - 500) // 2 + 220 ,"BA REFILL","white","cyan","black",30)



class MusicDisk:
    def __init__(self, rotation_speed=10):
        self.original_image = pygame.transform.smoothscale(
            pygame.image.load("graphics/Objects/disk.png").convert_alpha(), (50, 50)
        )
        self.image = self.original_image
        self.angle = 0
        self.rotation_speed = rotation_speed
        self.font = pygame.font.Font("font/subatomic.ttf", 20)

        self.panel_x = 10
        self.panel_y = screen_height - 80
        self.panel_height = 70
        self.padding = 20

        self.dropdown_visible = False
        self.mouse_clicked = False  # Prevent multiple toggles on hold

    def update(self, events):
        global game_data, menu_music

        # Rotate disk
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Get current song text width to make panel dynamic
        song_name = menu_music_list[game_data["current_song"]]
        text_surface = self.font.render(song_name, True, "yellow")
        text_width = text_surface.get_width()
        self.panel_width = max(180, 50 + self.padding + text_width + 20)  # Minimum size enforced

        # Calculate dynamic width for dropdown based on song names
        dropdown_width = max(self.panel_width, 50 + self.padding + max(
            (self.font.render(song, True, "white").get_width() for song in menu_music_list), default=0) + 20)

        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_width, self.panel_height)

        # Click toggle dropdown only once per actual click (not on hold)
        if mouse_pressed and not self.mouse_clicked:
            self.mouse_clicked = True
            if panel_rect.collidepoint(mouse_pos):
                self.dropdown_visible = not self.dropdown_visible
            elif self.dropdown_visible:
                # Check if clicked on any dropdown option
                for i, song_name in enumerate(menu_music_list):
                    song_rect = pygame.Rect(
                        self.panel_x,
                        self.panel_y - (i + 1) * self.panel_height,
                        dropdown_width,
                        self.panel_height
                    )
                    if song_rect.collidepoint(mouse_pos):
                        game_data["current_song"] = i
                        menu_music = pygame.mixer.Sound(f"Sound/BGM/Menu Music/{song_name}.mp3")
                        music_channel.stop()
                        music_channel.play(menu_music,loops =-1)
                        self.dropdown_visible = False
                        break
                else:
                    # If clicked outside dropdown, hide it
                    self.dropdown_visible = False

        if not mouse_pressed:
            self.mouse_clicked = False

        # Adjust the panel width based on dropdown visibility
        if self.dropdown_visible:
            self.panel_width = dropdown_width
        else:
            # Reset to the original size based on the text
            self.panel_width = max(180, 50 + self.padding + text_width + 20)

    def draw(self, surface):
        song_name = menu_music_list[game_data["current_song"]]
        text_surface = self.font.render(song_name, True, "yellow")

        # Draw main panel
        pygame.draw.rect(surface, (30, 30, 30), (self.panel_x, self.panel_y, self.panel_width, self.panel_height), border_radius=15)
        pygame.draw.rect(surface, "yellow", (self.panel_x, self.panel_y, self.panel_width, self.panel_height), 2, border_radius=15)

        # Draw spinning disk
        disk_center_x = self.panel_x + 35
        disk_center_y = self.panel_y + self.panel_height // 2
        self.rect = self.image.get_rect(center=(disk_center_x, disk_center_y))
        surface.blit(self.image, self.rect)

        # Draw song name
        text_x = self.panel_x + 50 + self.padding
        text_y = self.panel_y + (self.panel_height - text_surface.get_height()) // 2
        surface.blit(text_surface, (text_x, text_y))

        # Dropdown list
        if self.dropdown_visible:
            # Calculate dynamic dropdown width
            dropdown_width = max(self.panel_width, 50 + self.padding + max(
                (self.font.render(song, True, "white").get_width() for song in menu_music_list), default=0) + 20)

            for i, song_name in enumerate(menu_music_list):
                song_y = self.panel_y - (i + 1) * self.panel_height
                rect = pygame.Rect(self.panel_x, song_y, dropdown_width, self.panel_height)

                # Highlight selected
                bg_color = "purple" if i == game_data["current_song"] else (50, 50, 50)
                pygame.draw.rect(surface, bg_color, rect)
                pygame.draw.rect(surface, "yellow", rect, 1)

                item_text = self.font.render(song_name, True, "white")
                text_pos = (self.panel_x + 50, song_y + (self.panel_height - item_text.get_height()) // 2)
                surface.blit(item_text, text_pos)



music_disk = MusicDisk()


# INVENTORY MAIN TEMPLATE
def inventory_template():
    global state
    screen.blit(inventory_bg,(0,0))
    border_line = pygame.Rect((0,3),(300,screen_height-3))
    pygame.draw.rect(screen,'slateblue',border_line)
    pygame.draw.rect(screen,'white',border_line,2)
    if ships_button.draw():
        state = State.SHIPS_INV
    if items_button.draw():
        state = State.ITEMS_INV
    if crafting_button.draw():
        state = State.CRAFTING
    if exhaust_button.draw():
        state = State.EXHAUST
    if upgrades_button.draw():
       state = State.UPGRADE_INV
    if menu_back_button.draw():
        state = State.MENU



def crafting_inv():
    global state
    value = screen.get_width() * 0.28125
    inventory_template()
    shop_bottombar(gold_icon,game_data["gold"],gold_ore_icon,game_data["gold_ore"],fuel_icon,game_data["fuel"])
    header('Crafting','black','lime','white')
    for i in range(1,3):
        pygame.draw.rect(screen,'black',[value*i,100,150,200],0,16)
        pygame.draw.rect(screen,'white',[value*i,100,150,200],2,16)

    coin_pos_x = value + (150- coin_craft.get_width())//2
    coin_pos_y = 100 + (200- coin_craft.get_height())//2
    screen.blit(coin_craft,(coin_pos_x,coin_pos_y))

    fuel_pos_x = value*2 + (150- fuel_craft.get_width())//2
    fuel_pos_y = 100 + (200- fuel_craft.get_height())//2
    screen.blit(fuel_craft,(fuel_pos_x,fuel_pos_y))
    if menu_back_button.draw():
        state = State.MENU


def exhaust_inv():
    global game_data,state
    inventory_template()
    items_inv_template(450,100,'Choose Exhaust','orangered')
    screen.blit(default_exhaust_inv,(463,110))
    items_inv_template(650,100,'Choose Exhaust','orangered')
    screen.blit(blueflame_exhaust_inv,(663,110))

    if default_exhaust_enable.draw():
        game_data["exhaust"]["current_exhaust"] = 0
    if game_data["exhaust"]["current_exhaust"] == 0:
        default_exhaust_enabled.draw()

    if game_data["exhaust"]["blue_flame_exhaust"] == True:
        if blueflame_exhaust_enable.draw():
            game_data["exhaust"]["current_exhaust"] = 1
    else:
        blueflame_exhaust_na.draw()
    if game_data["exhaust"]["blue_flame_exhaust"] == True and game_data["exhaust"]["current_exhaust"] == 1:
        blueflame_exhaust_enabled.draw()


# INVENTORY ITEM TEMPLATE
def items_inv_template(pos_x,pos_y,text,color):
    middle_pos_x = (screen.get_width() - 200)//2
    ships_temp = pygame.Rect((pos_x,pos_y),(100,100))
    pygame.draw.rect(screen,'black',ships_temp,border_radius = 6)
    pygame.draw.rect(screen,'white',ships_temp,2,border_radius = 6)
    menu_border = pygame.Rect((middle_pos_x,20),(200,40))
    pygame.draw.rect(screen,color,menu_border,border_top_left_radius = 20,border_bottom_right_radius = 40)
    header(text,"black",color,"white")




# MAIN SHIP INVENTORY PROPERTIES
def ships_inv():
    global state,game_data,slot_one,saved_ship,upgrade_instance
    inventory_template()
    items_inv_template(450,100,'Your Ships','red')
    screen.blit(default_ship_inv,(463,110))
    items_inv_template(650,100,'Your Ships','red')
    screen.blit(xeroship_inv,(663,110))
    items_inv_template(850,100,'Your Ships','red')
    screen.blit(zenoship_inv,(863,110))
    items_inv_template(1050,100,'Your Ships','red')
    screen.blit(furryship_inv,(1063,110))

    #SUB MENU 
    upgrade_instance = None
    
# DEFAULT SHIP INV SETUP
    if defaultship_owned == True:
        if default_ship_enable.draw():
            game_data["spaceship"] = 0
    if game_data["spaceship"] == 0:
        default_ship_enabled.draw()
        slot_one = 0
        saved_ship = 0
        update_all_damage()
    else:
        pass

# XERO SHIP INV SETUP
    if game_data["xeroship_owned"] == True:
        if xeroship_enable.draw():
            game_data["spaceship"] = 1
    else:
        xeroship_na.draw()
    if game_data["spaceship"] == 1 and game_data["xeroship_owned"] == True:
        xeroship_enabled.draw()
        slot_one = 1
        saved_ship = 1
        update_all_damage()
    else:
        pass

# ZENO SHIP INV SETUP
    if game_data["zenoship_owned"] == True:
        if zenoship_enable.draw():
            game_data["spaceship"] = 2
    else:
        zenoship_na.draw()
    if game_data["spaceship"] == 2 and game_data["zenoship_owned"] == True: 
        zenoship_enabled.draw()
        slot_one = 2
        saved_ship = 2
        update_all_damage()
    else:
        pass

# FURRY SHIP INV SETUP
    if game_data["furryship_owned"] == True:
        if furryship_enable.draw():
            game_data["spaceship"] = 3
    else:
        furryship_na.draw()
    if game_data["spaceship"] == 3 and game_data["furryship_owned"] == True:
        furryship_enabled.draw()
        slot_one = 3
        saved_ship = 3
        update_all_damage()

class Upgrade:
    def __init__(self, screen, data, image):
        self.screen = screen
        self.image = image
        self.data = data
        self.size = 200
        self.pos_x = 150 + (self.screen.get_width() - self.size) // 2
        self.pos_y = (self.screen.get_height() - self.size) // 2

        center_x = self.pos_x + self.size // 2 - 5
        self.pipe_one = pygame.Rect(center_x, self.pos_y - 100, 10, 100)
        self.pipe_two = pygame.Rect(center_x, self.pos_y + self.size, 10, 100)

        slot_x = self.pos_x + (self.size - 100) // 2
        self.thruster_slot = pygame.Rect(slot_x, self.pipe_two.y + 100, 100, 100)
        self.cannon_slot = pygame.Rect(slot_x, self.pipe_one.y - 100, 100, 100)

        self.upgrades = {
            "plasma_cannon": {
                "image": pygame.transform.scale(pygame.image.load("graphics/upgrades/plasma_cannon.png"), (100, 100)).convert_alpha(),
                "rect": self.cannon_slot,
            },
            "laser_beam": {
                "image": pygame.transform.scale(pygame.image.load("graphics/upgrades/laser_beam.png"), (100, 100)).convert_alpha(),
                "rect": self.cannon_slot,
            },
            "launch_thruster" : {
            "image": pygame.transform.scale(pygame.image.load("graphics/upgrades/launch_thruster.png"), (100, 100)).convert_alpha(),
            "rect": self.thruster_slot,
            },
            "life_thruster" : {
            "image": pygame.transform.scale(pygame.image.load("graphics/upgrades/life_thruster.png"), (100, 100)).convert_alpha(),
            "rect": self.thruster_slot,
            }
        }
        self.celestial_stone = pygame.transform.scale(pygame.image.load("graphics/upgrades/celestial_stone.png"),(100,100)).convert_alpha()
        self.celestial_stone_rect = self.celestial_stone.get_rect()
        self.minus_button = Rect_Button(screen,40,40,320,(screen_height - 170) + 40 ,"-","white","cyan","black",30)
        self.plus_button = Rect_Button(screen,40,40,520,(screen_height - 170) + 40 ,"+","white","cyan","black",30)
        self.enhance_button = Rect_Button(screen,200,40,330,screen_height - 45,"Enhance","cyan","gold","black")
        self.celestial_stone_amount = 0
        self.levelup_stone_needed = 0

        self.nova_core = pygame.transform.scale(pygame.image.load("graphics/upgrades/nova_core.png"),(100,100)).convert_alpha()
        self.nova_core_rect = self.celestial_stone.get_rect()
        self.ascend_button = Rect_Button(screen,200,40,330,screen_height - 45,"Ascend","cyan","gold","black")
        self.nova_core_amount = 0
        self.ascend_core_needed = 0
    def level_up_cap(self):
        ship_names = ["defaultship", "xeroship", "zenoship", "furryship"]
        ship_name = ship_names[self.data["spaceship"]]
        ship = ships_data[ship_name]
        calculation = (ship["current_max_level"] - ship["current_level"]) * 10
        self.levelup_stone_needed = calculation - (ship["current_xp"]/100)

        self.ascend_core_needed = (ship["max_level"] - ship["current_max_level"])/10


    def level_up_func(self):
        font = pygame.font.Font("font/gacha.ttf", 20)
        ship_names = ["defaultship", "xeroship", "zenoship", "furryship"]
        ship_name = ship_names[self.data["spaceship"]]
        ship = ships_data[ship_name]
        self.level_up_cap()
        if ship["current_level"] < ship["max_level"]:       
            if self.celestial_stone_amount < game_data["celestial_stone"] and self.celestial_stone_amount < self.levelup_stone_needed:
                if self.plus_button.draw():
                    self.celestial_stone_amount += 1
            if self.celestial_stone_amount > 0:
                if self.minus_button.draw():
                    self.celestial_stone_amount -= 1

            if self.celestial_stone_amount > 0:
                if self.enhance_button.draw():
                    game_data["celestial_stone"] -= self.celestial_stone_amount
                    ship["current_xp"] += (100 * self.celestial_stone_amount)
                    self.celestial_stone_amount = 0
                    while ship["current_xp"] >= 1000:
                        ship["current_xp"] -= 1000
                        ship["current_level"] += 1


        if ship["current_level"] == ship["current_max_level"]:
            if self.nova_core_amount < game_data["nova_core"] and self.nova_core_amount < self.ascend_core_needed:
                if self.plus_button.draw():
                    self.nova_core_amount += 1
            if self.nova_core_amount > 0:
                if self.minus_button.draw():
                    self.nova_core_amount -= 1
            if self.nova_core_amount > 0:
                if self.ascend_button.draw():
                    game_data["nova_core"] -= self.nova_core_amount
                    ship["current_max_level"] += (self.nova_core_amount * 10)
                    self.nova_core_amount = 0
        # xp bar
        pygame.draw.rect(screen,"white",[320,(screen_height - 170) - 30,240,20],0,10) 
        pygame.draw.rect(screen,"cyan",[320,(screen_height - 170) - 30,ship["current_xp"]/4.166666666666667,20],0,10)    


        

        if ship["current_max_level"] > ship["current_level"]:
            screen.blit(self.celestial_stone,(390,screen_height - 170))
            pygame.draw.rect(screen,"white",[390,screen_height - 170,self.celestial_stone_rect.width,self.celestial_stone_rect.height],2)
            pygame.draw.rect(screen,"white",(390,screen_height - 70,self.celestial_stone_rect.width,20))
            celestial_stone_amount_text = font.render(f"{game_data["celestial_stone"]}",True,"black")
            celestial_stone_amount_x = 390 + (self.celestial_stone_rect.width - celestial_stone_amount_text.get_width())//2
            celestial_stone_amount_y = screen_height - 70 + (20 - celestial_stone_amount_text.get_height())//2
            screen.blit(celestial_stone_amount_text,(celestial_stone_amount_x,celestial_stone_amount_y))

            celestial_stone_selected = font.render(f"{self.celestial_stone_amount}",True,"white")
            screen.blit(celestial_stone_selected,(490 - celestial_stone_selected.get_width() - 4,(screen_height - 170) + 4))

        else:
            screen.blit(self.nova_core,(390,screen_height - 170))
            pygame.draw.rect(screen,"white",[390,screen_height - 170,self.nova_core_rect.width,self.nova_core_rect.height],2)
            pygame.draw.rect(screen,"white",(390,screen_height - 70,self.nova_core_rect.width,20))
            nova_core_amount_text = font.render(f"{game_data["nova_core"]}",True,"black")
            nova_core_amount_x = 390 + (self.nova_core_rect.width - nova_core_amount_text.get_width())//2
            nova_core_amount_y = screen_height - 70 + (20 - nova_core_amount_text.get_height())//2
            screen.blit(nova_core_amount_text,(nova_core_amount_x, nova_core_amount_y))

            nova_core_selected = font.render(f"{self.nova_core_amount}",True,"white")
            screen.blit(nova_core_selected,(490 - nova_core_selected.get_width() - 4,(screen_height - 170) + 4))
        if ship["current_level"] == ship["max_level"]:
            font = pygame.font.Font("font/gacha.ttf", 30)
            max_level_reached_text = font.render("Max Level Reached",True,"white")
            screen.blit(max_level_reached_text,((screen_width + 300 - max_level_reached_text.get_width())//2, (screen_height - max_level_reached_text.get_height()) - 20))

    def draw(self):
        self.clicks()
        for pipe in [self.pipe_one, self.pipe_two]:
            pygame.draw.rect(self.screen, "white", pipe)

        for slot in [self.thruster_slot, self.cannon_slot]:
            pygame.draw.rect(self.screen, "black", slot, 0, 20)
            pygame.draw.rect(self.screen, "red", slot, 2, 20)

        self.screen.blit(self.image, (self.pos_x, self.pos_y))
        self.draw_upgrades()
        self.draw_stats()
        self.level_up_func()

    def draw_stats(self):
        update_all_damage()
        health_amount()
        speed_amount()
        font = pygame.font.Font("font/gacha.ttf", 20)
        ship_names = ["defaultship", "xeroship", "zenoship", "furryship"]
        ship_name = ship_names[self.data["spaceship"]]
        ship = ships_data[ship_name]

        # Use already calculated damage values
        aa = aa_damage
        skill = skill_damage
        ult = ultimate_damage

        stats = [
            f"Ship: {ship_name.capitalize()}",
            f"Current Level : {ship['current_level']}",
            f"Current Xp : {ship["current_xp"]}",
            f"Base Damage: {ship['base_damage'] + ship['current_level'] * 2}",
            f"AA Damage: {round(aa, 2)}",
            f"Ultimate Damage: {round(ult, 2)}",
            f"Health: {health}",
            f"Speed: {int(speed)}",
        ]
        colors = ["white","yellow","red","purple","green","orangered","pink","cyan"]

        # Draw background box
        padding = 10
        line_height = 30
        box_width = 300
        box_height = line_height * len(stats) + padding * 2
        box_x = self.screen.get_width() - box_width - 30
        box_y = 80

        pygame.draw.rect(self.screen, (20, 20, 20), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, "white", (box_x, box_y, box_width, box_height), width=2, border_radius=10)

        # Draw text lines
        for i, line in enumerate(stats):
            text_surface = font.render(line, True, colors[i])
            self.screen.blit(text_surface, (box_x + padding, box_y + padding + i * line_height))



        
    def draw_upgrades(self):
        ship_equipment_keys = ["defaultship_equipment", "xeroship_equipment", "zenoship_equipment", "furryship_equipment"]
        current_equipment = self.data[ship_equipment_keys[self.data["spaceship"]]]

        for name, upgrade in self.upgrades.items():
            if current_equipment.get(name):
                self.screen.blit(upgrade["image"], upgrade["rect"].topleft)
                pygame.draw.rect(self.screen, "white", upgrade["image"].get_rect(topleft=upgrade["rect"].topleft), 2)

    def clicks(self):
        global state
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.thruster_slot.collidepoint(pos):
                state = State.THRUSTER
                sfx_channel.play(click_sound)
            elif self.cannon_slot.collidepoint(pos):
                state = State.CANNON
                sfx_channel.play(click_sound)



def upgrade_menu(spaceship):
    global upgrade_instance  
    inventory_template()

    if upgrade_instance is None:
        ship_images_list = [
            'graphics/Spaceship/ship3.png',
            'graphics/Spaceship/ship.png',
            'graphics/Spaceship/ship4.png',
            'graphics/Spaceship/ship5.png',
        ]
        upgrade_ship_img = pygame.transform.scale(
            pygame.image.load(ship_images_list[spaceship]),
            (200, 200)
        ).convert_alpha()
        upgrade_instance = Upgrade(screen, game_data, upgrade_ship_img)

    upgrade_instance.draw()



def select_thruster():
    inventory_template()
    header("Select Thruster", "black", "orangered", "white")

    draw_option("launch_thruster", 450, 100)
    draw_option("life_thruster", 650,100)



def select_cannon():
    global game_data, state
    inventory_template()
    header("Select Cannon", "black", "orangered", "white")

    draw_option("laser_beam", 450, 100)
    draw_option("plasma_cannon", 650, 100)


def draw_option(upgrade_name, x, y):
    global game_data, state

    font = pygame.font.Font('font/gacha.ttf', 15)
    gap = 4
    image = pygame.transform.scale(pygame.image.load(f"graphics/upgrades/{upgrade_name}.png"), (100, 100)).convert_alpha()
    image_rect = image.get_rect(topleft=(x, y))
    screen.blit(image, image_rect)
    pygame.draw.rect(screen, "white", image_rect, 2)

    ship_key = ["defaultship_equipment", "xeroship_equipment", "zenoship_equipment", "furryship_equipment"][game_data["spaceship"]]
    current_equipment = game_data[ship_key]
    is_equipped = current_equipment.get(upgrade_name, False)
    amount = game_data['upgrades'][upgrade_name]

    # Draw amount text
    amount_text = font.render(f"{upgrade_name.replace('_', ' ').title()} : {amount}", True, "white")
    amount_x = x + (100 - amount_text.get_width()) // 2
    amount_y = y + 110

    pygame.draw.rect(screen, "black", [amount_x - gap, amount_y - gap, amount_text.get_width() + gap * 2, amount_text.get_height() + gap * 2], 0, 4)
    pygame.draw.rect(screen, "white", [amount_x - gap, amount_y - gap, amount_text.get_width() + gap * 2, amount_text.get_height() + gap * 2], 2, 4)
    screen.blit(amount_text, (amount_x, amount_y))

    pos = pygame.mouse.get_pos()
    if image_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
        # figure out category
        is_thruster = upgrade_name in ["launch_thruster", "life_thruster"]
        is_cannon = upgrade_name in ["plasma_cannon", "laser_beam"]

        if is_equipped:
            current_equipment[upgrade_name] = False
            game_data['upgrades'][upgrade_name] += 1
        elif amount >= 1:
            current_equipment[upgrade_name] = True
            game_data['upgrades'][upgrade_name] -= 1

            # unequip other if any
            if is_thruster:
                other = "life_thruster" if upgrade_name == "launch_thruster" else "launch_thruster"
            elif is_cannon:
                other = "laser_beam" if upgrade_name == "plasma_cannon" else "plasma_cannon"
            else:
                other = None

            if other and current_equipment.get(other):
                current_equipment[other] = False
                game_data['upgrades'][other] += 1

        state = State.UPGRADE_INV




# ITEM INVENTORY MENU
def items_inv():
    global state
    inventory_template()
    header('Your Items','black','cyan','white')
    font = pygame.font.Font('font/gacha.ttf',20)
    value = screen.get_width() * 0.28125
    first_row_item = ['Copper','Silver','Coal']
    first_row_amount = [game_data['copper'],game_data['silver'],game_data['coal']]
    first_row_images = [copper_inv,silver_inv,coal_inv]
    gap = 4
    for i in range(1,4):
        base_rect = pygame.Rect((value*i,100),(150,150))
        pygame.draw.rect(screen,'black',base_rect,0,8)
        pygame.draw.rect(screen,'white',base_rect,2,8)
        text = font.render(f"{first_row_item[i-1]} : {first_row_amount[i-1]}",True,'white')
        text_pos_x = value * i + (150-text.get_width())//2
        text_pos_y = 260
        img_pos_x =  value * i + (150-100)//2
        img_pos_y =  100 +(150-100)//2
        pygame.draw.rect(screen,'black',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],0,4)
        pygame.draw.rect(screen,'white',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],2,4)
        screen.blit(first_row_images[i-1],(img_pos_x,img_pos_y))
        screen.blit(text,(text_pos_x,text_pos_y))

    second_row_item = ['Iron','Emerald','Purple Gemstone']
    second_row_amount = [game_data['iron'],game_data['emerald'],game_data['purple gemstone']]
    second_row_images = [iron_inv,emerald_inv,purple_gemstone_inv]
    for i in range(1,4):
        base_rect = pygame.Rect((value*i,300),(150,150))
        pygame.draw.rect(screen,'black',base_rect,0,8)
        pygame.draw.rect(screen,'white',base_rect,2,8)
        text = font.render(f"{second_row_item[i-1]} : {second_row_amount[i-1]}",True,'white')
        text_pos_x = value * i + (150-text.get_width())//2
        text_pos_y = 460
        img_pos_x =  value * i + (150-100)//2
        img_pos_y =  300 +(150-100)//2
        pygame.draw.rect(screen,'black',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],0,4)
        pygame.draw.rect(screen,'white',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],2,4)
        screen.blit(second_row_images[i-1],(img_pos_x,img_pos_y))
        screen.blit(text,(text_pos_x,text_pos_y))

    third_row_item = ['Irridium','lavastone','Platinum']
    third_row_amount = [game_data['iridium'],game_data['lavastone'],game_data['platinum']]
    third_row_images = [iridium_inv,lavastone_inv,platinum_inv]
    for i in range(1,4):
        base_rect = pygame.Rect((value*i,500),(150,150))
        pygame.draw.rect(screen,'black',base_rect,0,8)
        pygame.draw.rect(screen,'white',base_rect,2,8)
        text = font.render(f"{third_row_item[i-1]} : {third_row_amount[i-1]}",True,'white')
        text_pos_x = value * i + (150-text.get_width())//2
        text_pos_y = 660
        img_pos_x =  value * i + (150-100)//2
        img_pos_y =  500 +(150-100)//2
        pygame.draw.rect(screen,'black',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],0,4)
        pygame.draw.rect(screen,'white',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],2,4)
        screen.blit(third_row_images[i-1],(img_pos_x,img_pos_y))
        screen.blit(text,(text_pos_x,text_pos_y))
    if next_button.draw():
        state = State.ITEMS_INV2

def items_inv2():
    global state
    inventory_template()
    header('Your Items','black','cyan','white')
    font = pygame.font.Font('font/gacha.ttf',20)
    value = screen.get_width() * 0.28125
    first_row_item = ['Gold Ore','Frost Crystal','Fuel']
    first_row_amount = [game_data['gold_ore'],game_data['frost crystal'],game_data['fuel']]
    first_row_images = [gold_inv,frost_crystal_inv,fuel_inv]
    gap = 4
    for i in range(1,4):
        base_rect = pygame.Rect((value*i,100),(150,150))
        pygame.draw.rect(screen,'black',base_rect,0,8)
        pygame.draw.rect(screen,'white',base_rect,2,8)
        text = font.render(f"{first_row_item[i-1]} : {first_row_amount[i-1]}",True,'white')
        text_pos_x = value * i + (150-text.get_width())//2
        text_pos_y = 260
        img_pos_x =  value * i + (150-100)//2
        img_pos_y =  100 +(150-100)//2
        if i == 3:
            img_pos_y =  100 +(150-120)//2
        pygame.draw.rect(screen,'black',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],0,4)
        pygame.draw.rect(screen,'white',[text_pos_x - gap,text_pos_y - gap,text.get_width()+gap*2,text.get_height()+gap*2],2,4)
        screen.blit(first_row_images[i-1],(img_pos_x,img_pos_y))
        screen.blit(text,(text_pos_x,text_pos_y))
    
    if previous_button.draw():
        state = State.ITEMS_INV


# LOGO FUNCTION
def draw_logo():
    logo_font = pygame.font.Font('font/Logo.ttf',30)
    logo_text = logo_font.render('Interstellar',True,'red')
    logo_text2 = logo_font.render('Pirates',True,'yellow')
    screen.blit(logo_text,(40,20))
    screen.blit(logo_text2,(110,80))

# DRAW MAIN MENU FUNCTION
def draw_menu():
    draw_logo()
    music_disk.update(pygame.event.get())
    music_disk.draw(screen)
    game_mode_button.draw()
    journey_button.draw()
    shop_button.draw()
    inventory_button.draw()
    settings_button.draw()
    quit_button.draw()


# MAIN SHOP BOTTOMBAR FUNCTION
def shop_bottombar(item_icon,item_amount,item_icon2 = None,item_amount2 = None,item_icon3 = None,item_amount3= None):
    main_x = 90 + 20
    bottom_bar = pygame.Rect((0,screen_height  - 50),(screen_width,50))
    pygame.draw.rect(screen,'black',bottom_bar)
    pygame.draw.rect(screen,'white',bottom_bar,2)
    screen.blit(item_icon,(main_x,screen_height  - 50))
    font = pygame.font.Font("font/gacha.ttf",51)
    first_item_amount = font.render(f"{item_amount}",True,"white")
    screen.blit(first_item_amount,(main_x + 60, screen_height  - 50+5))

    second_x = main_x + 60 + first_item_amount.get_width() + 20
    if item_icon2 is not None and item_amount2 is not None:
        screen.blit(item_icon2,(second_x,screen_height  - 50))
        second_item_amount = font.render(f"{item_amount2}",True,"white")
        screen.blit(second_item_amount,(second_x + 60, screen_height  - 50+5))
    if item_icon2 is not None and item_amount2 is not None:
        third_x = second_x + 60 + second_item_amount.get_width() + 20
    if item_icon3 is not None and item_amount3 is not None:
        screen.blit(item_icon3,(third_x,screen_height  - 50))
        third_item_amount = font.render(f"{item_amount3}",True,"white")
        screen.blit(third_item_amount,(third_x + 60, screen_height  - 50+5))


# SHOP ITEM TEMPLATE
def item_template(pos_x,pos_y,pos1_x,pos1_y,text,text_posx,text_posy):
    buy_jade = pygame.Rect((pos_x,pos_y),(200,200))
    jade_border = pygame.Rect((pos1_x,pos1_y),(200,25))
    text_template = item_gui_font.render(text,True,'black')
    pygame.draw.rect(screen,'steelblue1',buy_jade,border_top_left_radius = 50)
    pygame.draw.rect(screen,'white',jade_border)
    screen.blit(text_template,(text_posx,text_posy))
    

# DRAW TEH SHOP FUNCTION
def shop_menu():
    global game_data,shop_variables,state 
    screen.blit(shop_bg,(0,0))
    header('Your Shop','Black','orange','white')
    first_row_items = [jade_buy_surf,gold_buy_surf,xeroship_buy_surf,blue_exhaust_buy_surf]
    
    for i in range(4):
        x_position = item_spacing * (i + 1) + shop_rect_width * i
        y_position = 80
        image_x = x_position + (200 - 125)//2
        image_y = y_position + (200 - 125)//2
        pygame.draw.rect(screen, 'black', (x_position, y_position, shop_rect_width, shop_rect_height),0,8)
        pygame.draw.rect(screen, 'white', (x_position, y_position, shop_rect_width, shop_rect_height),2,8)
        screen.blit(first_row_items[i],(image_x,image_y))



    shop_bottombar(jade_icon,game_data["jade"],gold_icon,game_data["gold"])
    if menu_back_button.draw():
        state = State.MENU
    if gacha_button.draw():
        state = State.GACHA

    if game_data["gold"] >= 1000:
        if buy_jade_button.draw():
            game_data["gold"] -= 1000
            game_data["jade"] += 10
        buy_jade_button.hover('Buy 10 jade by spending 1000 gold','below',20)
    else:
        unavailable_jade_button.draw()
        unavailable_jade_button.hover(f'Need 1000 (Gold : {game_data["gold"]})','below',20)


    if game_data["jade"] >= 20:
        if buy_gold_button.draw():
            game_data["gold"] += 1000 
            game_data["jade"] -= 20
        buy_gold_button.hover('Buy 1000 gold by spending 20 jade','below',20)
    else:
        unavailable_gold_button.draw()
        unavailable_gold_button.hover(f'Need 20 jade (Jade : {game_data["jade"]})','below',20)

    
    if game_data["jade"] >= 10000 and game_data["xeroship_owned"] == False:
        if buy_xeroship_button.draw():
            game_data["xeroship_owned"] = True
        buy_xeroship_button.hover('Buy Xeroship by spending 10000 jade','below',20)
    if game_data["xeroship_owned"] == True:
        sold_xeroship_button.draw()
    if game_data["jade"] <= 9999 and game_data["xeroship_owned"] == False :
        unavailable_xeroship_button.draw()
        unavailable_xeroship_button.hover(f'Need 10000 jade (Jade : {game_data["jade"]})','below',20)


    if game_data["gold"] >= 100000 and game_data["exhaust"]["blue_flame_exhaust"] == False:
        if buy_blue_exxhaust.draw():
            game_data["exhaust"]["blue_flame_exhaust"] = True
            game_data["gold"] -= 100000
        buy_blue_exxhaust.hover('Buy blue flame exhaust (100000 gold)','below',20)
    if game_data["exhaust"]["blue_flame_exhaust"] == True:
        sold_blue_exhaust_button.draw()
    if game_data["gold"] <= 99999 and game_data["exhaust"]["blue_flame_exhaust"] == False:
        unavailable_blue_exhaust_button.draw()
        unavailable_blue_exhaust_button.hover(f'Need 100000 gold (Jade : {game_data["gold"]})','below',20)


# SPACESTATION SHOP
def spacestation_menu():
    global game_data,shop_variables,state 
    screen.blit(shop_bg,(0,0))
    header(f'{random_galaxy} spacestation shop','Black','orange','white')
    first_row_items = [emerald_buy_surf,purple_gemstone_buy_surf]
    
    for i in range(2):
        x_position = item_spacing * (i + 1) + shop_rect_width * i
        y_position = 80
        image_x = x_position + (200 - 125)//2
        image_y = y_position + (200 - 125)//2
        pygame.draw.rect(screen, 'black', (x_position, y_position, shop_rect_width, shop_rect_height),0,8)
        pygame.draw.rect(screen, 'white', (x_position, y_position, shop_rect_width, shop_rect_height),2,8)
        screen.blit(first_row_items[i],(image_x,image_y))
    shop_bottombar(emerald_icon,game_data["emerald"],purple_gemstone_icon,game_data["purple gemstone"],jade_icon,game_data["jade"]) 
    if leave_button.draw():
        state = State.SPACESTATION_EXIT


    if game_data["emerald"] >= 1:
        if exchange_emerald_button.draw():
            game_data["emerald"] -= 1
            game_data["jade"] += 100
        if exchange_emerald_button.hover("Exchange 1 emerald for 100 jades","below",20):
            pass
    else:
        unavailable_exchange_button.draw()
    if game_data["purple gemstone"] >= 1:
        if exchange_gemstone_button.draw():
            game_data["purple gemstone"] -= 1
            game_data["jade"] += 100
        if exchange_gemstone_button.hover("Exchange 1 purple gemstone for 100 jades","below",20):
            pass
    else:
        unavailable_exchange_button2.draw()


gacha_prize = {
    "iron": [pygame.transform.scale(pygame.image.load("graphics/gemstone/iron.png"), (200, 200)),"iron","black"],
    "copper": [pygame.transform.scale(pygame.image.load("graphics/gemstone/copper.png"), (200, 200)),"copper","black"],
    "silver": [pygame.transform.scale(pygame.image.load("graphics/gemstone/silver.png"), (200, 200)),"silver","black"],
    "coal": [pygame.transform.scale(pygame.image.load("graphics/gemstone/coal.png"), (200, 200)),"coal","black"],
    "gold_ore": [pygame.transform.scale(pygame.image.load("graphics/gemstone/gold_ore.png"), (200, 200)),"gold ore","black"],
    "lavastone": [pygame.transform.scale(pygame.image.load("graphics/gemstone/lavastone.png"), (200, 200)),"lavastone","purple"],
    "platinum": [pygame.transform.scale(pygame.image.load("graphics/gemstone/platinum.png"), (200, 200)),"platinum","purple"],
    "frost crystal": [pygame.transform.scale(pygame.image.load("graphics/gemstone/frost crystal.png"), (200, 200)),"frost crystal","purple"],
    "purple gemstone": [pygame.transform.scale(pygame.image.load("graphics/gemstone/purple gemstone.png"), (200, 200)),"purple gemstone","purple"],
    "emerald": [pygame.transform.scale(pygame.image.load("graphics/gemstone/emerald.png"), (200, 200)),"emerald","purple"],
    "iridium": [pygame.transform.scale(pygame.image.load("graphics/gemstone/iridium.png"), (200, 200)),"iridium","purple"],
    "furryship_owned": [pygame.transform.scale(pygame.image.load("graphics/Spaceship/ship5.png"), (200, 200)),"furry ship","gold"],
    "zenoship_owned": [pygame.transform.scale(pygame.image.load("graphics/Spaceship/ship4.png"), (200, 200)),"zeno ship","gold"],
    "laser_beam" : [pygame.transform.scale(pygame.image.load("graphics/upgrades/laser_beam.png"), (200, 200)),"laser beam","gold"],
    "plasma_cannon" : [pygame.transform.scale(pygame.image.load("graphics/upgrades/plasma_cannon.png"), (200, 200)),"plasma cannon","gold"],
    "launch_thruster" : [pygame.transform.scale(pygame.image.load("graphics/upgrades/launch_thruster.png"), (200, 200)),"launch thruster","gold"],
    "life_thruster" : [pygame.transform.scale(pygame.image.load("graphics/upgrades/life_thruster.png"), (200, 200)),"life thruster","gold"],
    "nova_core" : [pygame.transform.scale(pygame.image.load("graphics/upgrades/nova_core.png"), (200, 200)),"nova core","gold"]
}


#Gacha Section
class Gacha():
    def __init__(self):
        self.font = pygame.font.Font("font/gacha.ttf", 30)
        self.font2 = pygame.font.Font("font/gacha.ttf", 20)
        self.bg_image = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/1.png'), (screen_width,screen_height)).convert_alpha()
        self.limited_button = Rect_Button(screen,150,40,25,40,"Limited","white","cyan","black",font_size =22)
        self.permanent_button = Rect_Button(screen,150,40,25,140,"Permanent","white","cyan","black",font_size =22)
        self.powerups_button = Rect_Button(screen,150,40,25,240,"Powerups","white","cyan","black",font_size =22)
        self.banner_type = "limited"
        self.position = [(screen_width - 800)//2,100]
        self.pos_x = (screen.get_width() - furryship_gacha_banner.get_width()) // 2
        self.pos_y = self.position[1] + (400-furryship_gacha_banner.get_height())//2
        self.video = cv2.VideoCapture("wish.mp4")
        self.powerups_template = pygame.transform.scale(pygame.image.load("graphics/Templates/powerups.png"),(800,400)).convert_alpha()

        self.limited_gacha_table = [
            (15, "iron", (50, 100)),
            (30, "copper", (50, 100)),
            (45, "silver", (50, 100)),
            (60, "coal", (50, 100)),
            (65, "gold_ore", (20, 50)),
            (70, "lavastone", (1, 3)),
            (80, "platinum", (20, 50)),
            (85, "frost crystal", (1, 3)),
            (90, "purple gemstone", (1, 3)),
            (95, "emerald", (1, 3)),
            (99, "iridium", (1, 3)),
            (100, "furryship_owned", None)
                                            ]
        self.permanent_gacha_table = [
            (15, "iron", (50, 100)),
            (30, "copper", (50, 100)),
            (45, "silver", (50, 100)),
            (60, "coal", (50, 100)),
            (65, "gold_ore", (20, 50)),
            (70, "lavastone", (1, 3)),
            (80, "platinum", (20, 50)),
            (85, "frost crystal", (1, 3)),
            (90, "purple gemstone", (1, 3)),
            (95, "emerald", (1, 3)),
            (99, "iridium", (1, 3)),
            (100, "zenoship_owned", None)
                                            ]
        self.powerups_gacha_table = [
            (15, "iron", (50, 100)),
            (30, "copper", (50, 100)),
            (45, "silver", (50, 100)),
            (60, "coal", (50, 100)),
            (65, "gold_ore", (20, 50)),
            (70, "lavastone", (1, 3)),
            (75, "platinum", (20, 50)),
            (80, "frost crystal", (1, 3)),
            (85, "purple gemstone", (1, 3)),
            (90, "emerald", (1, 3)),
            (96, "iridium", (1, 3)),
            (97, "life_thruster",(1,2)),
            (98, "launch_thruster",(1,2)),
            (99, "plasma_cannon", (1,2)),
            (100, "laser_beam", (1,2))
                                            ]                                    
        self.gacha_table = self.limited_gacha_table
        self.random_items = None
        self.amount = None
        self.pull_count = 0
        self.result
    def menu(self):
        global state
        screen.blit(self.bg_image,(0,0))
        if self.banner_type =="limited":
            pygame.draw.rect(screen,"crimson",[0,0,200,screen_height])
            pygame.draw.rect(screen,"white",[0,0,200,screen_height],2)
            header("Furryship Summon","black","crimson","white",font_size = 35)
            img = pygame.Surface((800,400))
            img.fill("crimson")
            img.set_alpha(192)
            screen.blit(img,(self.position[0],self.position[1]))
            for i in range(100):
                pygame.draw.circle(screen,"crimson",(random.randint(self.position[0],self.position[0] + 800),random.randint(self.position[1],self.position[1] + 400)),2)
            pygame.draw.rect(screen,"white",[self.position[0],self.position[1],800,400],2)
            screen.blit(furryship_gacha_banner,(self.pos_x,self.pos_y))

        if self.banner_type == "permanent":
            pygame.draw.rect(screen,"purple",[0,0,200,screen_height])
            pygame.draw.rect(screen,"white",[0,0,200,screen_height],2)
            header("Permanent Banner","black","Purple","white",font_size = 35)
            img = pygame.Surface((800,400))
            img.fill("purple")
            img.set_alpha(192)
            screen.blit(img,(self.position[0],self.position[1]))
            for i in range(100):
                pygame.draw.circle(screen,"purple",(random.randint(self.position[0],self.position[0] + 800),random.randint(self.position[1],self.position[1] + 400)),2)
            pygame.draw.rect(screen,"white",[self.position[0],self.position[1],800,400],2)
            screen.blit(zenoship_gacha_banner,(self.pos_x,self.pos_y))
        if self.banner_type == "powerups":
            pygame.draw.rect(screen,"gold",[0,0,200,screen_height])
            pygame.draw.rect(screen,"white",[0,0,200,screen_height],2)
            header("Powerups Banner","black","gold","white",font_size = 35)
            screen.blit(self.powerups_template,((screen_width - 800)//2,100))

        if self.limited_button.draw():
            self.banner_type ="limited"
            self.gacha_table = self.limited_gacha_table
        if self.permanent_button.draw():
            self.banner_type = "permanent"
            self.gacha_table = self.permanent_gacha_table
        if self.powerups_button.draw():
            self.banner_type = "powerups"
            self.gacha_table = self.powerups_gacha_table
        shop_bottombar(jade_icon,game_data["jade"],None,None)

        if shop_back_button.draw():
            state = State.SHOP

        if game_data["jade"] >=100:
            if single_pull_btn.draw():
                sfx_channel.play(chest_opening_sound)
                self.video = cv2.VideoCapture("wish.mp4")
                game_data['jade'] -= 100
                quest_data["dailies"]["wish_completed"] += 1
                self.pull_count = 1
                state = State.GACHA_ROLL
            single_pull_btn.hover('it cost 100 jades','below',20)
        else:
            if single_pull_btn.draw():
                state = State.GACHA
            single_pull_btn.hover(f'You need 100 jades (jade - {game_data["jade"]})','below',20)
        if game_data["jade"] >= 1000:
            if multi_pull_btn.draw():
                sfx_channel.play(chest_opening_sound)
                self.video = cv2.VideoCapture("wish.mp4")
                game_data['jade'] -= 1000
                quest_data["dailies"]["wish_completed"] += 10
                self.pull_count = 10
                state = State.GACHA_ROLL
            multi_pull_btn.hover('it cost 1000 jades','below',20)
        else:
            if multi_pull_btn.draw():
                state = State.GACHA
            multi_pull_btn.hover(f'You need 1000 jades (jade - {game_data["jade"]})','below',20)

    def gacha_backend(self):
        self.results = []  # Store all results here
        for _ in range(self.pull_count):
            random_items = random.randint(1, 100)
            for threshold, item, amount_range in self.gacha_table:
                if random_items <= threshold:
                    if amount_range:
                        amount = random.randint(*amount_range)
                        if self.banner_type == "limited" or self.banner_type == "permanent":
                            game_data[item] += amount
                        else:
                            try:
                                game_data["upgrades"][item] += amount
                            except:
                                game_data[item] += amount
                        self.results.append((item, amount))
                    else:
                        if game_data[item]:
                            item = "nova_core"
                            game_data["nova_core"] += 1
                        else:
                            game_data[item] = True
                        self.results.append((item, "1"))
                    break

    def roll(self):
        global state
        ret, frame = self.video.read()
        if not ret:
            self.video.release()
            self.gacha_backend()
            planetery_background.generate_random_background()
            state = State.GACHA_RESULT
            return

 

        frame = cv2.resize(frame, (screen_width, screen_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame, (0, 0))


    def result(self):
        planetery_bg_group.draw(screen)
        planetery_bg_group.update()

        if self.pull_count == 1:
            item, amount = self.results[0]
            img = gacha_prize[item][0]

            # Calculate center positions
            img_x = (screen.get_width() - img.get_width()) // 2
            img_y = (screen.get_height() - img.get_height()) // 2 - 30  # lift it a bit to give room for text

            pygame.draw.rect(screen,gacha_prize[item][2],[img_x,img_y,img.get_width(),img.get_height()],0,6)
            screen.blit(img, (img_x, img_y))
            pygame.draw.rect(screen,"white",[img_x,img_y,img.get_width(),img.get_height()],2,6)

            if gacha_prize[item][2] == "gold":
                pygame.draw.rect(screen,"white",[img_x,img_y,img.get_width(),img.get_height()],2,6)



            # Render and center the text under the image
            if amount == "1":
                text = self.font.render(f"{gacha_prize[item][1]} x1", True, "white")
            else:
                text = self.font.render(f"{gacha_prize[item][1]} x{amount}", True, "white")

            text_x = (screen.get_width() - text.get_width()) // 2
            text_y = img_y + img.get_height() + 20

            screen.blit(text, (text_x, text_y))

        else:
            cols = 5
            spacing_x = 60
            spacing_y = 100
            img_size = 200

            total_width = cols * img_size + (cols - 1) * spacing_x
            start_x = (screen.get_width() - total_width) // 2
            start_y = 100

            for idx, (item, amount) in enumerate(self.results):
                row = idx // cols
                col = idx % cols

                x = start_x + col * (img_size + spacing_x)
                y = start_y + row * (img_size + spacing_y)

                img = gacha_prize[item][0]
                pygame.draw.rect(screen,gacha_prize[item][2],[x,y,img.get_width(),img.get_height()],0,6)
                screen.blit(img, (x, y))
                pygame.draw.rect(screen,"white",[x,y,img.get_width(),img.get_height()],2,6)

                text = self.font2.render(f"{gacha_prize[item][1]} x{amount}", True, "white")
                text_x = x + (img.get_width() - text.get_width()) // 2
                screen.blit(text, (text_x, y + img.get_height() + 10))



gacha = Gacha()



# BACKGROUND CLASS
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bg_images = []

        for i in range(1, 24):
            img = pygame.image.load(f'graphics/Backgrounds/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (screen_width,screen_height))
            self.bg_images.append(img)

        self.image = random.choice(self.bg_images)
        self.rect = self.image.get_rect()
        self.pos_x = 0
        self.pos_y = 0
        self.rect.topleft = [self.pos_x, self.pos_y]


    def update(self):
        # Move the background image vertically
        self.pos_y += scroll_speed

        # Draw the current background image at the current position
        screen.blit(self.image, (self.pos_x, self.pos_y))

        # Check if the next image is partially visible on the top side
        next_pos_y = self.pos_y - screen_height
        if next_pos_y > -screen_height:
            screen.blit(self.image, (self.pos_x, next_pos_y))

        # Check if the current image is off the screen, reset its position
        if self.pos_y >= screen_height:
            self.pos_y = 0


        self.rect.topleft = [self.pos_x, self.pos_y]



    def generate_random_background(self):
        new_image = random.choice(self.bg_images)
        new_images = pygame.transform.scale(new_image,(screen_width,screen_height))
        while new_image == self.image:
            # Keep selecting a new image until it's different
            new_image = random.choice(self.bg_images)
        self.image = new_images


# BACKGROUND CLASS
class Menu_Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bg_images = []

        for i in range(25, 28):
            img = pygame.image.load(f'graphics/Backgrounds/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (screen_width,screen_height))
            self.bg_images.append(img)

        self.image = random.choice(self.bg_images)
        self.rect = self.image.get_rect()
        self.pos_x = 0
        self.pos_y = 0
        self.rect.topleft = [self.pos_x, self.pos_y]


    def update(self):
        # Move the background image vertically
        self.pos_y += 15

        # Draw the current background image at the current position
        screen.blit(self.image, (self.pos_x, self.pos_y))

        # Check if the next image is partially visible on the top side
        next_pos_y = self.pos_y - screen_height
        if next_pos_y > -screen_height:
            screen.blit(self.image, (self.pos_x, next_pos_y))

        # Check if the current image is off the screen, reset its position
        if self.pos_y >= screen_height:
            self.pos_y = 0


        self.rect.topleft = [self.pos_x, self.pos_y]



    def generate_random_background(self):
        new_image = random.choice(self.bg_images)
        new_images = pygame.transform.scale(new_image,(screen_width,screen_height))
        while new_image == self.image:
            # Keep selecting a new image until it's different
            new_image = random.choice(self.bg_images)
        self.image = new_images

# SPACESHIP CLASS
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = default_ship
        self.image = pygame.transform.scale(self.img,(100,100))
        self.rect = self.image.get_rect()
        self.pos_x = 650
        self.pos_y = 600
        self.width = self.image.get_width()
        self.rect.center = [self.pos_x, self.pos_y]
        self.exhaust_group = pygame.sprite.Group()
        self.exhaust_activation = True
        self.shoot_cooldown = 5
    
    def update(self):
        global speed
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        keys = pygame.key.get_pressed()
        if self.pos_x <= 0:
            self.pos_x = 0 
        if self.pos_x >= screen_width:
            self.pos_x = screen_width 
        if self.pos_y >= screen_height:
            self.pos_y = screen_height
        if self.pos_y <= 250:
            self.pos_y = 250
        if game_data['spaceship'] == 3:
            mouse_pos = pygame.mouse.get_pos()
            self.pos_x, self.pos_y = mouse_pos
            if self.pos_x <= 0:
                self.pos_x = 0
            if self.pos_x >= screen_width:
                self.pos_x = screen_width
            if self.pos_y >= screen_height:
                self.pos_y = screen_height
            if self.pos_y <= 250:
                self.pos_y = 250

        if self.exhaust_activation:
            new_exhaust = self.create_exhaust()
            self.exhaust_group.add(new_exhaust)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos_y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos_y += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos_x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += speed
        
        self.rect.center = (self.pos_x, self.pos_y)
    
    def can_shoot(self):
        """Returns True if the spaceship can shoot (cooldown is over)."""
        return self.shoot_cooldown == 0

    def reset_shoot_cooldown(self):
        """Resets the cooldown timer after firing a bullet."""
        self.shoot_cooldown = 5  
    def create_bullets(self):
        bullets = [
            Bullets(self.pos_x, self.pos_y - 25),
            Bullets(self.pos_x - 15, self.pos_y - 25),
            Bullets(self.pos_x + 15, self.pos_y - 25)
        ]
        # bullets = Bullets(self.pos_x, self.pos_y - 25)
        return bullets
    def creating_laser(self):
        laser = [Laser(0,0),Laser2(screen_width,0)]
        return laser

    def projectile1(self):
        projectile = Projectile(self.pos_x,self.pos_y - 25)
        return projectile
    def skill_2(self):
        skill_2 = Xersoship_skill(self.pos_x,self.pos_y)
        return skill_2
    def reset_pos(self):
        self.pos_x = 650
        self.pos_y = 600
        self.rect.center = [self.pos_x, self.pos_y]

    def zenoship_skill(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pos_x, self.pos_y = mouse_pos
       
    def furryship_ultimate(self):
        furry_ult = Shower()
        return furry_ult
    def create_exhaust(self):
        exhaust = [Exhaust(self.pos_x,self.pos_y + 20), Exhaust(self.pos_x - 10,self.pos_y + 20), Exhaust(self.pos_x + 10,self.pos_y + 20), Exhaust(self.pos_x - 20,self.pos_y + 20), Exhaust(self.pos_x + 20,self.pos_y + 20) ]
        return exhaust





        
# XEROSHIP SKILL CLASS
class Xersoship_skill(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image =  pygame.transform.scale(pygame.image.load('graphics/Projectiles/shield.png'), (175,300)).convert_alpha() 
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.center = [pos_x,pos_y]
        self.cooldown = 0
        self.count = 0
    def update(self):
        global speed
        keys = pygame.key.get_pressed()
        if self.pos_x <= 0:
            self.pos_x = 0
        if self.pos_x >= screen_width:
            self.pos_x = screen_width
        if self.pos_y >= screen_height:
            self.pos_y = screen_height
        if self.pos_y <= 250:
            self.pos_y = 250
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos_y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos_y += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos_x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += speed

        if game_data['spaceship'] == 3:
            mouse_pos = pygame.mouse.get_pos()
            self.pos_x, self.pos_y = mouse_pos
            if self.pos_x <= 0:
                self.pos_x = 0
            if self.pos_x >= screen_width:
                self.pos_x = screen_width
            if self.pos_y >= screen_height:
                self.pos_y = screen_height
            if self.pos_y <= 250:
                self.pos_y = 250 

        if game_data['spaceship'] == 2 and keys[pygame.K_e]:
            self.count = 1



        if self.count >= 1:
            self.kill()
            self.count = 0




        
        self.rect.center = (self.pos_x, self.pos_y)
        if self.cooldown != 300:
            self.cooldown += 1
        else:
            self.cooldown = 0
            self.kill()



# XEROSHIP ULTIMATE PROJECTILE CLASS
class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.img = pygame.image.load('graphics/Projectiles/projectile1.png').convert_alpha()
        self.image = pygame.transform.scale(self.img,(50,100))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self):
        self.rect.y -= 10
        if self.rect.y <= 0:
            self.kill()

# SPACESHIP BULLET CLASS
class Bullets(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((5,40)).convert_alpha()
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = (pos_x,pos_y))

    
    def update(self):
        self.rect.y -= 10
        if self.rect.y <= 0:
            self.kill()

# DEFAULT SHIP SKILL CLASS
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((5,screen_height))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.topright = [pos_x,pos_y]

    def update(self):
        self.rect.x += 15
        if self.rect.x >= screen_width:
            self.kill()
# DEFAULT SHIP 2ND LASOR SKILL
class Laser2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((5,screen_height))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.topright = [pos_x,pos_y]

    def update(self):
        self.rect.x -= 15
        if self.rect.x <= 0:
            self.kill()





class Shower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.size = random.randint(80,160)
        self.img = pygame.image.load('graphics/celestial_body/meteors/2.png')
        self.scale = pygame.transform.scale(self.img,(self.size,self.size))
        self.image = self.scale
        self.rect = self.image.get_rect()
        self.pos_x = random.randint(200,1000)
        self.pos_y = random.randint(718,screen_height)   
        self.rect.center = [self.pos_x,self.pos_y]
        self.x_movement = random.uniform(-5.5,5.5)
        self.y_movement = random.uniform(1,20)
        self.rotate_speed = random.uniform(0.1,0.9)
    def update(self):
        self.pos_y -= self.y_movement
        self.pos_x -= self.x_movement

        if self.angle < 360:
            self.angle += self.rotate_speed
        else:
            self.angle = 0
        self.image = pygame.transform.rotate(self.scale,self.angle)
        if self.pos_x <= 0 or self.pos_x >= screen_width:
            self.kill()
        if self.pos_y <= 0:
            self.kill()


        self.rect.topright = [self.pos_x,self.pos_y]

# FLAME_ORANGE = (255, 165, 0)
# FLAME_YELLOW = (255, 255, 0)
# FLAME_RED = (255, 50, 0)
class Exhaust(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos = [pos_x + random.randint(-5, 5), pos_y]  # Add horizontal spread
        self.start_y = pos_y
        self.lifetime = 40  # frames
        self.age = 0
        
        # Flame properties
        self.size = random.randint(8, 10)
        if game_data["exhaust"]["current_exhaust"] == 0:
            self.colors = [
                (255, random.randint(150, 200), 0),  # Orange-yellow
                (255, random.randint(50, 100), 0)    # Red-orange
            ]
        else:
            self.colors = [
        (0, random.randint(100, 200), 255),  # Light blue
        (0, random.randint(50, 150), 200)    # Deep blue
    ]

        # Create initial surface
        self.image = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        
        # Movement properties
        self.speed = random.randint(3, 6)
        self.direction = random.uniform(-0.5, 0.5)  # Horizontal spread

    def update(self):
        self.age += 1
        progress = self.age / self.lifetime
        
        # Update position with upward movement
        self.pos[1] += self.speed * 0.7  # Main upward speed
        self.pos[0] += self.direction * 2  # Horizontal sway
        
        # Fade out effect
        current_alpha = int(255 * (1 - progress))
        current_size = int(self.size * (1 - progress))
        
        # Create new flame particle
        self.image = pygame.Surface((current_size*2, current_size*2), pygame.SRCALPHA)
        chosen_color = random.choice(self.colors)
        pygame.draw.circle(self.image, (*chosen_color, current_alpha), 
                          (current_size, current_size), current_size)
        
        # Update rectangle position
        self.rect.center = (int(self.pos[0]), int(self.pos[1]))
        
        # Kill particle when expired
        if self.age >= self.lifetime or self.pos[1] < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size,color):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # self.color_list = ["orange","red","yellow","green","cyan"]
        self.color = color  # Orange-ish color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        
        # Randomize particle movement
        self.velocity_x = random.uniform(-5, 5)
        self.velocity_y = random.uniform(-5, 5)
        self.gravity = 0.1  # Simulate gravity pulling particles down
        self.lifetime = random.randint(20, 40)  # How long the particle lasts
        self.alpha = 255  # Initial transparency

    def update(self):
        # Update position
        self.velocity_y += self.gravity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Fade out the particle over time
        self.alpha = max(0, self.alpha - 255 / self.lifetime)
        self.image.set_alpha(int(self.alpha))
        
        # Kill the particle if its lifetime is over
        if self.alpha <= 0:
            self.kill()

# Function to create an explosion effect
def create_explosion(group, pos_x, pos_y, size, num_particles=100):
    colors = random.choice(["red","cyan","orange","yellow"])
    for _ in range(num_particles):
        particle = Explosion(pos_x, pos_y, size,colors)
        group.add(particle)

# PIRATE CLASS
class Pirate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(f'graphics/Pirates/{pirate_num}.png').convert_alpha()
        img = pygame.transform.rotate(img, 180)
        img = pygame.transform.scale(img, (75, 75))

        self.image =img
        self.rect = self.image.get_rect()
        self.pos_x = random.randrange(30, screen_width - 30)
        self.pos_y = random.randrange(0, 100)
        self.rect.center = [self.pos_x, self.pos_y]
        self.gravity = random.randint(1, 3)
        self.movement = random.randint(-3, 3)
    
    def update(self):
        if self.pos_y <= screen_height:
            self.pos_y += self.gravity + scroll_speed/4
            self.pos_x += self.movement 
        if self.pos_y >= screen_height:
            self.kill()

        if self.pos_x < 0 or self.pos_x > screen_width:
            self.kill()


        self.rect.center = (self.pos_x, self.pos_y) 

# HEALTH REGEN CLASS
class Health(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load('graphics/hp.png').convert_alpha()
        self.image = pygame.transform.scale(self.img,(64,64))
        self.pos_x = random.randrange(30, screen_width -30  )
        self.pos_y = random.randrange(0,100)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x,self.pos_y)
        self.gravity = random.randrange(1,5)
    def update(self):
        if self.pos_y <= screen_height:
            self.pos_y += self.gravity + scroll_speed/4
        if self.pos_y >= screen_height:
            self.kill()
        if self.pos_x < 0 or self.pos_x > screen_width:
            self.kill()
        self.rect.center = (self.pos_x, self.pos_y) 

# CRYSTAL CLASS
class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randrange(64,100)
        self.img = pygame.image.load('graphics/crystal_chunk.png').convert_alpha()
        self.image = pygame.transform.scale(self.img,(self.size,self.size))
        self.rect = self.image.get_rect()
        self.pos_x = random.randrange(-self.size, screen_width)
        self.pos_y = random.randrange(-self.size, -30) 
        self.rect.topright = [self.pos_x,self.pos_y]
        self.x_movement = random.uniform(-5.5,5.5)
        self.y_movement = random.uniform(1,8)
    def update(self):
        self.pos_y += self.y_movement + scroll_speed/4
        self.pos_x += self.x_movement + scroll_speed/4
        if self.pos_x <= 0 or self.pos_x >= screen_width:
            self.kill()
        if self.pos_y >= screen_height:
            self.kill()
        self.rect.topright = [self.pos_x,self.pos_y]

# PLANET CLASS
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.number = random.randrange(1, 64)
        self.size = random.randrange(64, 128)
        self.img = pygame.image.load(f'graphics/celestial_body/planets/{self.number}.png').convert_alpha()
        self.scale = pygame.transform.scale(self.img, (self.size, self.size))
        self.image = self.scale  
        self.rect = self.image.get_rect()
        self.pos_x = random.randrange(100, screen_width - (self.size +100))
        self.pos_y = random.randrange(0, 10)
        self.rect.topright = [self.pos_x, self.pos_y]
        self.x_movement = random.uniform(-0.9, 0.9)
        self.y_movement = random.uniform(0.3, 1.5)
        self.rotate_speed = random.uniform(0.1,0.3)

    def update(self):
        self.pos_y += self.y_movement
        self.pos_x += self.x_movement
        if self.angle <= 360:
            self.angle += self.rotate_speed
        else:
            self.angle = 0


        self.image = pygame.transform.rotate(self.scale, self.angle)

        if self.pos_x <= 0 or self.pos_x >= screen_width:
            self.kill()
        if self.pos_y >= screen_height:
            self.kill()

        self.rect.topright = [self.pos_x, self.pos_y]

# BLACKHOLE CLASS
class Blackhole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initialize the Sprite base class
        self.radius = random.randint(64, 128)  # Radius of the black hole
        self.glow_radius = self.radius + 10  # Radius of the glowing outline
        self.color = (0, 0, 0)  # Black color for the black hole

        # Flame-like glow colors (orange, red, yellow gradient)
        self.glow_colors = [
            (255, 69, 0),  # Orange
            (255, 0, 0),   # Red
            (255, 215, 0), # Yellow
        ]

        # Create an image and rect for the sprite
        self.image = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # Initialize position and movement
        self.pos_x = random.randrange(0+self.radius,(screen_width-self.radius))  # Ensure it spawns within screen bounds
        self.pos_y = random.randrange(-50, -30)  # Spawn above the screen
        self.rect.center = (self.pos_x, self.pos_y)  # Set the initial position
        self.x_movement = random.uniform(-0.3, -0.9)
        self.y_movement = random.uniform(0.3, 2.5)

        # Time-based offset for the moving glow effect
        self.time_offset = 0

        # Precompute the glow surface
        self.glow_surface = self._create_glow_surface()

        # Draw the black hole and glow on the image
        self._draw_black_hole()

    def _create_glow_surface(self):
        """Create a precomputed glow surface."""
        glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        for i in range(2):  # Fewer layers for a thinner outline
            alpha = int(255 * (1 - i / 2))  # Adjust opacity
            glow_color = self.glow_colors[i % len(self.glow_colors)]  # Cycle through glow colors
            pygame.draw.circle(
                glow_surface,
                (*glow_color, alpha),
                (self.glow_radius, self.glow_radius),
                self.glow_radius - i * 10,  # Thinner outline
            )
        # Apply Gaussian blur for a smoother glow (only once during initialization)
        return pygame.transform.gaussian_blur(glow_surface, radius=3)

    def _draw_black_hole(self):
        """Draw the black hole and its glowing outline on the sprite's image."""
        self.image.fill((0, 0, 0, 0))  # Clear the image with transparency

        # Draw the precomputed glow surface with a moving effect
        offset = sin(self.time_offset) * 4  # Adjust the multiplier for stronger/weaker effect
        self.image.blit(self.glow_surface, (offset, offset))

        # Draw the black hole
        pygame.draw.circle(self.image, self.color, (self.glow_radius, self.glow_radius), self.radius)
        pygame.draw.circle(self.image, "white", (self.glow_radius, self.glow_radius), self.radius, width=2)

    def update(self):
        """Update the black hole's position and glow effect."""
        self.pos_y += self.y_movement
        self.pos_x += self.x_movement
        self.rect.center = (self.pos_x, self.pos_y)  # Update the rect's position

        # Update the time offset for the moving glow effect
        self.time_offset += 0.1  # Adjust the speed of the glow animation

        # Redraw the black hole with the updated glow
        self._draw_black_hole()

        # Kill the sprite if it goes off-screen
        if self.pos_x <= -self.glow_radius or self.pos_x >= screen_width + self.glow_radius:
            self.kill()
        if self.pos_y >= screen_height + self.glow_radius:
            self.kill()

# WORMHOLE CLASS
class Wormhole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.number = 1
        self.img = pygame.image.load(f'graphics/Portal/{self.number}.png')
        self.image = pygame.transform.scale(self.img,(400,300))
        self.rect = self.image.get_rect()
        self.pos_x = random.randrange(0 + 200, screen_width - 600)
        self.pos_y = -300 
        self.rect.topright = [self.pos_x,self.pos_y]
        self.x_movement = random.uniform(-0.9,0.9)
        self.y_movement = random.uniform(0.3,2.5)
    def update(self):
        self.pos_y += self.y_movement
        self.pos_x += self.x_movement
        if self.pos_x <= 0 or self.pos_x >= screen_width:
            self.kill()
        if self.pos_y >= screen_height:
            self.kill()
        if self.number < 64:
            self.number += 1

        else:
            self.number = 1
        self.img = pygame.image.load(f'graphics/Portal/{self.number}.png')
        self.image = pygame.transform.scale(self.img,(400,300))
        self.rect.topright = [self.pos_x,self.pos_y]

# METEOR CLASS
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.number = random.randrange(1,114)
        self.size = random.randrange(64,256)
        self.img = pygame.image.load(f'graphics/celestial_body/meteors/{self.number}.png').convert_alpha()
        self.scale = pygame.transform.scale(self.img,(self.size,self.size))
        self.image = self.scale
        self.rect = self.image.get_rect()
        self.pos_x = random.randrange(-self.size, screen_width)
        self.pos_y = random.randrange(-self.size, -30) 
        self.rect.topright = [self.pos_x,self.pos_y]
        self.x_movement = random.uniform(-5.5,5.5)
        self.y_movement = random.uniform(1,20)
        self.rotate_speed = random.uniform(0.1,0.9)
    def update(self):
        self.pos_y += self.y_movement + scroll_speed
        self.pos_x += self.x_movement + scroll_speed
        if self.angle < 360:
            self.angle += self.rotate_speed
        else:
            self.angle = 0
        self.image = pygame.transform.rotate(self.scale,self.angle)
        if self.pos_x <= 0 or self.pos_x >= screen_width:
            self.kill()
        if self.pos_y >= screen_height:
            self.kill()


        self.rect.topright = [self.pos_x,self.pos_y]




# SPACESTATION CLASS
class Spacestation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.size = random.randrange(100,150)
        self.img = pygame.image.load('graphics/Spacestation.png').convert_alpha()
        self.scale = pygame.transform.scale(self.img,(self.size,self.size))
        self.image = self.scale
        self.rect = self.image.get_rect()
        self.pos_x = random.randrange(self.size, screen_width - self.size*2)
        self.pos_y = random.randrange(-self.size, -30) 
        self.rect.topright = [self.pos_x,self.pos_y]
        self.x_movement = random.uniform(-0.9,0.9)
        self.y_movement = random.uniform(1.3,2.9)
        self.rotate_speed = random.uniform(0.1,0.4)
    def update(self):
        self.pos_y += self.y_movement
        self.pos_x += self.x_movement
        if self.angle < 360:
            self.angle += self.rotate_speed
        else:
            self.angle = 0
        self.image = pygame.transform.rotate(self.scale,self.angle)
        if self.pos_x <= 0 or self.pos_x >= screen_width:
            self.kill()
        if self.pos_y >= screen_height:
            self.kill()
        self.rect.topright = [self.pos_x,self.pos_y]

# PLANETERY CLASSES

class Planetery_bg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bg_images = []

        for i in range(1, 4):
            img = pygame.image.load(f'graphics/Planets_bg/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (screen_width,screen_height))
            self.bg_images.append(img)
        self.image = random.choice(self.bg_images)
        self.rect = self.image.get_rect()
        self.pos_x = 0
        self.pos_y = 0
        self.rect.topleft = [self.pos_x, self.pos_y]


    def update(self):
        # Move the background image vertically
        self.pos_y += scroll_speed

        # Draw the current background image at the current position
        screen.blit(self.image, (self.pos_x, self.pos_y))

        # Check if the next image is partially visible on the top side
        next_pos_y = self.pos_y - screen_height
        if next_pos_y > -screen_height:
            screen.blit(self.image, (self.pos_x, next_pos_y))

        # Check if the current image is off the screen, reset its position
        if self.pos_y >= screen_height:
            self.pos_y = 0


        self.rect.topleft = [self.pos_x, self.pos_y]



    def generate_random_background(self):
        new_image = random.choice(self.bg_images)
        new_images = pygame.transform.scale(new_image,(screen_width,screen_height))
        while new_image == self.image:
            # Keep selecting a new image until it's different
            new_image = random.choice(self.bg_images)
        self.image = new_images

class Boss_01_aa(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.number = 1
        self.img = pygame.image.load(f'graphics/Projectiles/Effects/pink/{self.number}.png').convert_alpha()  # Set a proper size for the skill surface
        self.image = pygame.transform.scale(self.img,(40,120))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
    def update(self):
        self.rect.y += 20
        if self.number !=6:
            self.number += 1
        else:
            self.number = 1
        self.img = pygame.image.load(f'graphics/Projectiles/Effects/pink/{self.number}.png').convert_alpha()  # Set a proper size for the skill surface
        self.image = pygame.transform.scale(self.img,(40,120))
        if self.rect.y > screen_height or self.rect.x > screen_width or self.rect.x < 0:
            self.kill()



class Boss_01_ultimate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load('graphics/Boss/minion.png').convert_alpha()
        self.image = pygame.transform.scale(self.img,(100,80))
        self.rect =  self.image.get_rect()
        self.pos_x = random.randrange(0,screen_width)
        self.pos_y = 0
        self.rect.topright = [self.pos_x,self.pos_y]
        self.x_movement = random.randrange(-5,5)
        self.y_movement = random.randrange(5,8)
    def update(self):
        self.pos_x += self.x_movement + scroll_speed/4
        self.pos_y += self.y_movement + + scroll_speed/4
        if self.pos_x < 0 or self.pos_x > screen_width or self.pos_y > screen_height:
            self.kill()

        self.rect.topright = [self.pos_x,self.pos_y]


boss_aa_group = pygame.sprite.Group()
boss_ultimate_group = pygame.sprite.Group()

class Boss_01(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load('graphics/Boss/Boss_01.png').convert_alpha()
        self.flip = pygame.transform.rotate(self.img, 360)
        self.image = pygame.transform.scale(self.flip, (300, 150))
        self.rect = self.image.get_rect()
        self.pos_x = (screen_width + self.image.get_width()) // 2
        self.pos_y = 50
        self.rect.topright = [self.pos_x, self.pos_y]
        self.auto = True
        self.auto_cd = 0
        self.skill = False
        self.skill_cooldown = 0
        self.skill_duration = 0
        self.ultimate = False
        self.ultimate_cd = 0
        self.left = True
        self.right = False
        self.fire = False
    def update(self):
        if self.left:
            self.pos_x -= 5
            if self.pos_x - self.image.get_width() < 0:
                self.left = False
                self.right = True
        if self.right:
            self.pos_x += 5
            if self.pos_x  >= screen_width:
                self.left = True
                self.right = False
        if self.auto:
            if self.auto_cd < 50:
                self.auto_cd += 2
                if self.skill == False:
                    self.skill_cooldown += 2
                self.ultimate_cd += 2

            else:
                self.fire = True
                boss_aa_group.add(self.create_aa())
                self.auto_cd = 0
        if self.skill_cooldown >= 1000:
            self.skill = True
        if self.skill:
            if self.skill_duration < 500:
                self.skill_duration += 2
                if self.fire:
                    new_auto = Boss_01_aa(self.pos_x - 60, self.pos_y + 80)
                    boss_aa_group.add(new_auto)
                    second_auto = Boss_01_aa(self.pos_x - 280, self.pos_y + 80)
                    boss_aa_group.add(second_auto)
                    self.fire = False
            else:
                self.skill_duration = 0
                self.skill = False
                self.skill_cooldown = 0

        if self.ultimate_cd >= 1500:
            self.ultimate = True
        if self.ultimate:
            boss_ultimate_group.add(self.create_ultimate())
            for _ in range(4):
                new_ultimate = Boss_01_ultimate()
                boss_ultimate_group.add(new_ultimate)
            self.ultimate = False
            self.ultimate_cd = 0

        # Update the rect position accordingly
        self.rect.topright = [self.pos_x, self.pos_y]

    def create_aa(self):
        aa = Boss_01_aa(self.pos_x - 170, self.pos_y + 80)
        return aa
    def create_ultimate(self):
        ultimate = Boss_01_ultimate()
        return ultimate 




class Boss_02_aa(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)  # Bigger surface for glow effect
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.create_glow()  # Draw glow effect once

    def create_glow(self):
        """ Draws a glowing red circle using multiple layers of transparency """
        self.image.fill((0, 0, 0, 0))  # Transparent background

        glow_color = (255,0,0)  # Red glow
        glow_levels = [(30, 20), (100, 15), (150, 10), (255, 7)]  
        # Format: (Alpha, Radius)

        for alpha, radius in glow_levels:
            pygame.draw.circle(self.image, (*glow_color, alpha), (30, 30), radius)  # Blend RGB with alpha
        pygame.draw.circle(self.image, (255,255,255,80), (30, 30), 10,1)


    def update(self):
        self.pos_y += 10 
        if self.pos_y >= screen_height:
            self.kill()
        self.rect.topleft = [self.pos_x, self.pos_y]

class Boss_02_skill(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,angle):
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA).convert_alpha() 
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.angle = angle
        self.create_glow() 
    def create_glow(self):
        self.image.fill((0, 0, 0, 0))  # Transparent background

        glow_color = (255,0,0)  # Red glow
        glow_levels = [(30, 20), (100, 15), (150, 10), (255, 7)]  
        # Format: (Alpha, Radius)

        for alpha, radius in glow_levels:
            pygame.draw.circle(self.image, (*glow_color, alpha), (30, 30), radius)  # Blend RGB with alpha
        pygame.draw.circle(self.image, (255,255,255,80), (30, 30), 10,1)

    def update(self):
        self.pos_x += self.angle
        self.pos_y += 20
        self.rect.topleft = [self.pos_x, self.pos_y]


class Boss_02_Ultimate(pygame.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss  # Store reference to the boss
        self.image = pygame.Surface((250, 250), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.boss = boss
        self.rect.center = self.boss.rect.center


    def update(self):
        pygame.draw.circle(self.image,"red",(125,125),125,10)
        self.rect.center = self.boss.rect.center  






class Boss_02(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.image  = pygame.transform.scale(pygame.image.load('graphics/Boss/Boss.png'),(200,200)).convert_alpha()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.pos_x = (screen.get_width()- self.width)//2
        self.pos_y = 50
        self.rect.topleft = [self.pos_x,self.pos_y]
        self.left = True
        self.right = False
        self.auto = True
        self.auto_cd = 50
        self.fire = True
        self.skill_cd = 500
        self.skill_duration = 300
        self.skill = False
        self.ultimate =  False
        self.ultimate_duration = 300
        self.ultimate_cd = 800
        self.ultimate_activated = False

    def update(self):
        if not self.ultimate_activated:
            self.ultimate_cd -= 2
        if self.left:
            self.pos_x -= 5
            if self.pos_x < 0:
                self.left = False
                self.right = True
        if self.right:
            self.pos_x += 5
            if self.pos_x + self.width  >= screen_width:
                self.left = True
                self.right = False
        if self.auto:
            self.auto_cd -= 2
            self.skill_cd -= 2
            if self.skill_cd <= 0 and self.auto_cd <=0:
                self.skill = True
                self.fire = False
                self.create_skill()
                self.auto_cd = 50
                if self.skill_duration <= 0:
                    self.fire = True
                    self.auto_cd = 50
                    self.skill_cd = 500
                    self.skill_duration = 300
                    self.skill = False
            if self.auto_cd <= 0 and self.fire:
                self.create_aa()
                self.auto_cd = 50
        if self.ultimate_cd <= 0 :
            self.ultimate = True
        if self.ultimate:
            self.create_ultimate()
            self.ultimate = False
            self.ultimate_activated = True
        if self.ultimate_activated:
            self.ultimate_duration -= 2
            if self.ultimate_duration <= 0:
                boss_ultimate_group.empty()
                self.ultimate_duration = 300
                self.ultimate_cd = 800
                self.ultimate_activated = False


        if self.skill:
            self.skill_duration -= 2
            
        self.rect.topleft = [self.pos_x,self.pos_y]

    def create_aa(self):
        center_x = self.pos_x + (200-60)//2
        center_y = self.pos_y + 160
        aa = Boss_02_aa(center_x ,center_y)
        boss_aa_group.add(aa)
        return aa
    def create_skill(self):
        center_x = self.pos_x + (200-60)//2
        center_y = self.pos_y + 160
        angles = [-15,-5,5,15]  # Left and right diagonal movement
        for angle in angles:
            skill = Boss_02_skill(center_x,center_y, angle)
            boss_aa_group.add(skill)
        return skill
    def create_ultimate(self):
        ultimate = Boss_02_Ultimate(self)
        boss_ultimate_group.add(ultimate)
        return ultimate



# def spaceship_damage():
#     global game_data,aa_damage,skill_damge,ultimate_damage
#     if game_data["spaceship"] == 0:
#         aa_damage = random.randrange(35,45)
#     if game_data["spaceship"] == 1:
#         aa_damage = random.randrange(70,80)
#         skill_damge = 0
#         ultimate_damage = random.randrange(1000,1500)
#     if game_data["spaceship"] == 2:
#         aa_damage = random.randrange(180,200)
#         skill_damge = 0
#         ultimate_damage = random.randrange(1000,2000)
#     if game_data["spaceship"] == 3:
#         aa_damage = random.randrange(280,300)
#         skill_damge = 0
#         ultimate_damage = random.randrange(400,500)

random_boss = None
boss_01_mhp = 100000
boss_01_hp = 100000
def Bossbar(mhp,hp,ratio,name):
    resize_x = mhp / ratio
    boss_font = pygame.font.Font('Font/LM.otf',15)
    boss_name = boss_font.render(name,True,'black')
    text_pos_x = (screen.get_width() - boss_name.get_width())/2
    boss_mhp = pygame.Rect(((screen.get_width() - resize_x)// 2, 10 ), (mhp / ratio, 30))
    boss_hp = pygame.Rect(((screen.get_width() - resize_x)// 2, 10 ), (hp / ratio, 30))
    pygame.draw.rect(screen,'red',boss_mhp,border_radius = 6)
    pygame.draw.rect(screen,'green',boss_hp,border_radius = 6)
    screen.blit(boss_name,(text_pos_x,14))




planetery_loadbar = 80
planetery_loadlimit = 800

def planetery_load(menu_state):
    global planetery_loadbar,planetery_loadlimit,state
    load_font = pygame.font.Font('Font/LM.otf',20)
    load_text = load_font.render('Loading',True,'white')
    load_bar_bg = pygame.Rect(((screen.get_width() - planetery_loadlimit)//2,(screen.get_height()-30)//2),(planetery_loadlimit ,50))
    load_bar_surf = pygame.Rect(((screen.get_width() - planetery_loadlimit)//2,(screen.get_height()-30)//2),(planetery_loadbar , 50))
    if planetery_loadbar < planetery_loadlimit:
        planetery_loadbar += 20
    else:
        state = menu_state
        planetery_loadbar = 80

    pygame.draw.rect(screen,'red',load_bar_bg,border_radius = 6)
    pygame.draw.rect(screen,'green',load_bar_surf,border_radius = 6)
    screen.blit(load_text,((screen.get_width()- load_text.get_width())//2,(screen.get_height()- load_text.get_height())//2 + 10))
#PLANETERY BACKGROUND GROUP
planetery_background = Planetery_bg()
planetery_bg_group = pygame.sprite.Group()
planetery_bg_group.add(planetery_background)


boss_01 = Boss_01()
boss_02 = Boss_02()
boss_group = pygame.sprite.Group()





#GROUPING EACH AND EVERY SPRITE CLASS

# Initialize the background

menu_background = Menu_Background()
menu_background_group = pygame.sprite.Group()
menu_background_group.add(menu_background)


background = Background()
background_group = pygame.sprite.Group()
background_group.add(background)

# spaceship
spaceship = Spaceship()
spaceship_group = pygame.sprite.Group()
spaceship_group.add(spaceship)

#planet group

planet = Planet()
planet_group = pygame.sprite.Group()


#blackhole group

blackhole = Blackhole()
blackhole_group = pygame.sprite.Group()


#wormhole group

wormhole = Wormhole()
wormhole_group = pygame.sprite.Group()

#meteor group

meteor = Meteor()
meteor_group = pygame.sprite.Group()

#crystal group

crystal = Crystal()
crystal_group = pygame.sprite.Group()


#spacestation group
spacestation = Spacestation()
spacestation_group = pygame.sprite.Group()


#health regen 
hp = Health()
hp_group = pygame.sprite.Group()




# pirate
pirate_group = pygame.sprite.Group()
#explosion effect
explosion_group = pygame.sprite.Group()


for _ in range(pirate_count):
    new_pirate = Pirate()
    pirate_group.add(new_pirate)

# bullets
bullet_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
skill2_group = pygame.sprite.Group()
furry_ult_group = pygame.sprite.Group()

skill_group_list = [laser_group,projectile_group,skill2_group,furry_ult_group]
boss_skill_group_list = [bullet_group,laser_group,projectile_group,skill2_group,furry_ult_group]

# SPACESHIP SKILL AND ULT COOLDOWN TIMER
xeroship_skill_timer = 0
xeroship_ult_timer = 0
furryship_ult_timer = 0
health_orbs = 0
zenoship_mana = 500
# ANIMATION TIMER
warp_time = 1
scan_time = 0
sucking_time = 0





# CUSTOM USEREVENT
PLANET_REGEN_TIMER = pygame.USEREVENT + 1 
def set_planet_timer():
    random_delay = random.randint(40000, 60000) 
    pygame.time.set_timer(PLANET_REGEN_TIMER, random_delay)
set_planet_timer()

BLACKHOLE_REGEN_TIMER = pygame.USEREVENT + 2
def set_blackhole_timer():
    random_delay = random.randint(120000, 200000) 
    pygame.time.set_timer(BLACKHOLE_REGEN_TIMER, random_delay)
set_blackhole_timer()

METEOR_REGEN_TIMER = pygame.USEREVENT + 3
def set_meteor_timer():
    random_delay = random.randint(2000,5000) 
    pygame.time.set_timer(METEOR_REGEN_TIMER, random_delay)
set_meteor_timer()

HEALTH_REGEN_TIMER = pygame.USEREVENT + 4
def set_health_timer():
    random_delay = random.randint(60000,100000) 
    pygame.time.set_timer(HEALTH_REGEN_TIMER, random_delay)
set_health_timer()

CRYSTAL_REGEN_TIMER = pygame.USEREVENT + 5
def set_crystal_timer():
    random_delay = random.randint(1000,10000) 
    pygame.time.set_timer(CRYSTAL_REGEN_TIMER, random_delay)
set_crystal_timer()

WORMHOLE_REGEN_TIMER = pygame.USEREVENT + 6
def set_wormhole_timer():
    random_delay = random.randint(300000,600000) 
    pygame.time.set_timer(WORMHOLE_REGEN_TIMER, random_delay)
set_wormhole_timer()

SPACESTATION_REGEN_TIMER = pygame.USEREVENT + 7
def set_spacestation_timer():
    random_delay = random.randint(1000000,1500000) 
    pygame.time.set_timer(SPACESTATION_REGEN_TIMER, random_delay)
set_spacestation_timer()

#CAMPAIGN MODE STUFF
spaceship_img = pygame.transform.smoothscale(pygame.image.load("graphics/Story_assets/empty_ship.png"),(screen_width,screen_height)).convert_alpha()


space_group = pygame.sprite.Group()

def draw_space(display):
    while len(space_group) < 200:  
        space = Space(display)
        space_group.add(space)

    space_group.draw(display)
    space_group.update()


run = True
enter_bar = 10
leave_bar = 10
scan_bar = 10
scan_limit = 400
sucking_bar = 10
sucking_limit = 400

def sound_bar():
    global settings_data
    header("Sound Settings")

    music_bar = settings_data['sound']['music']
    sfx_bar = settings_data['sound']['sfx']
    bar_width = settings_data['sound']['width']
    bar_height = settings_data['sound']['height']

    pos_x = (screen.get_width() - bar_width)//2
    music_y = 250
    sfx_y = 450

    pygame.draw.rect(screen,'white',[pos_x,music_y,bar_width,bar_height],0,20)
    pygame.draw.rect(screen,'cyan',[pos_x,music_y,music_bar*4,bar_height],0,20)
    pygame.draw.rect(screen,'black',[pos_x,music_y,bar_width,bar_height],2,20)

    pygame.draw.rect(screen,'white',[pos_x,sfx_y,bar_width,bar_height],0,20)
    pygame.draw.rect(screen,'cyan',[pos_x,sfx_y,sfx_bar*4,bar_height],0,20)
    pygame.draw.rect(screen,'black',[pos_x,sfx_y,bar_width,bar_height],2,20)

    main_font = pygame.font.Font('Font/gacha.ttf',40)
    music_text = main_font.render(f'Music : {int(music_bar/10)}', True, 'black')
    music_text_x = (screen.get_width() - music_text.get_width())//2
    music_text_y = 250 + (bar_height - music_text.get_height())//2 + 2
    screen.blit(music_text,(music_text_x,music_text_y))

    sfx_text = main_font.render(f'Sfx : {int(sfx_bar/10)}', True, 'black')
    sfx_text_x = (screen.get_width() - sfx_text.get_width())//2
    sfx_text_y = 450 + (bar_height - sfx_text.get_height())//2 + 2
    screen.blit(sfx_text,(sfx_text_x,sfx_text_y))

    


    

def sucking_animation (group1,group2,result1,result2):
    global sucking_bar,sucking_limit
    suck_surf_bg = pygame.Rect((440,20),(sucking_limit,20))
    suck_surf = pygame.Rect((440,20),(sucking_bar,20))
    if sucking_bar < sucking_limit:
        sucking_bar += 4
    elif sucking_bar >= sucking_limit:
        destruction = pygame.sprite.groupcollide(group1,group2,result1,result2)
        screen.blit(boom_surf2,blackhole.rect.topleft)
        sucking_bar = 10

    pygame.draw.rect(screen,'red',suck_surf_bg,border_radius = 6)
    pygame.draw.rect(screen,'green',suck_surf,border_radius = 6)
    display_letters(f'sucking {random_planet} planet',570,22,10,'black')


def loading_bar(group1,group2,result1,result2):
    global scan_bar,scan_limit,state,game_data
    scan_surf_bg = pygame.Rect((440,20),(scan_limit,20))
    scan_surf = pygame.Rect((440,20),(scan_bar,20))
    if scan_bar < scan_limit:
        scan_bar += 4
    elif scan_bar >= scan_limit:
        sfx_channel.play(planet_sound)
        random_jade = random.randrange(5,50)
        destruction = pygame.sprite.groupcollide(group1,group2,result1,result2)
        game_data["jade"] += random_jade
        quest_data['event']["planet_discovered"] += 1
        scan_bar = 10
        state = State.PLANETERY_OPTION


    pygame.draw.rect(screen,'red',scan_surf_bg,border_radius = 6)
    pygame.draw.rect(screen,'green',scan_surf,border_radius = 6)
    display_letters(f'scanning {random_planet} planet',570,22,10,'black')



def reset_game():
    global pirate_num
    background.generate_random_background()
    planetery_background.generate_random_background()
    pirate_group.empty()
    blackhole_group.empty()
    meteor_group.empty()
    crystal_group.empty()
    planet_group.empty()
    hp_group.empty()
    bullet_group.empty()
    spaceship.reset_pos()
    skill2_group.empty()
    laser_group.empty()
    projectile_group.empty()
    furry_ult_group.empty()
    spaceship.exhaust_group.empty()

    

    new_pirate_num = random.randrange(1,26)
    while new_pirate_num == pirate_num:
            # Keep selecting a new image until it's different
        new_pirate_num = random.randrange(1,26)
    pirate_num = new_pirate_num
    pirate_num = random.randrange(1,26)
    random_galaxy = random.choice(galaxy_names)
    for _ in range(pirate_count):
        new_pirate = Pirate()
        #new_pirate.pirate_regenerate()  # Call pirate_regenerate to update the appearance
        pirate_group.add(new_pirate)


# UPDATE SPACESHIP IMAGE FUNC   
def update_spaceship():
    if game_data["spaceship"] == 0:
        spaceship.image = pygame.transform.scale(default_ship,(100,100))
        spaceship_group.draw(screen)
        spaceship.update()
    if game_data["spaceship"] == 1:
        spaceship.image = pygame.transform.scale(xero_ship,(100,100))
        spaceship_group.draw(screen)
        spaceship.update()
    if game_data["spaceship"] == 2:
        spaceship.image = pygame.transform.scale(zeno_ship,(100,100))
        spaceship_group.draw(screen)
        spaceship.update()
    if game_data["spaceship"] == 3:
        spaceship.image = pygame.transform.scale(furry_ship,(100,100))
        spaceship_group.draw(screen)
        spaceship.update()

# TAB MENU
oxygen_limit = 200
oxygen_bar = 200
fuel_limit = 200
fuel_bar = 200
radiation_bar = 200
radiation_limit = 10

def tab_menu():
    global oxygen_limit,radiation_limit,fuel_limit,game_data
    tab_window = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/Window.png'),(500,500)).convert_alpha()
    data_window = pygame.transform.scale(pygame.image.load('graphics/Asset_bg/data_bg.png'),(250,500)).convert_alpha()
    pos_x = screen.get_width() * 0.17
    pos_y = (screen.get_height()- tab_window.get_height())//2
    pos_x2 = screen.get_width() * 0.83 - data_window.get_width()
    pos_y2 = (screen.get_height() - data_window.get_height()) // 2 
    spaceship_x = (pos_x + tab_window.get_width())//2
    spaceship_y = (screen.get_height() - default_ship_tab.get_height())// 2
    text_x = spaceship_x + 25
    text_y = pos_y + 15

    oxygen_x = pos_x2 + 50
    oxygen_y = pos_y2 + 20
    oxygen_rect_x = pos_x2 + 25
    oxygen_rect_y = oxygen_y + 40

    fuel_x = pos_x2 + 65
    fuel_y = oxygen_rect_y + 50
    fuel_rect_x = oxygen_rect_x
    fuel_rect_y = fuel_y + 40

    radiation_x = pos_x2 + 40
    radiation_y = fuel_rect_y + 50
    radiation_rect_x = oxygen_rect_x
    radiation_rect_y = radiation_y + 40


    tab_surf = pygame.image.load('graphics/Asset_bg/6.png').convert_alpha()
    screen.blit(tab_surf,(0,0))
    oxygen_bg = pygame.Rect((oxygen_rect_x,oxygen_rect_y),(oxygen_bar,30))
    oxygen_rect = pygame.Rect((oxygen_rect_x,oxygen_rect_y),(oxygen_limit,30))
    fuel_bg = pygame.Rect((fuel_rect_x,fuel_rect_y),(fuel_bar,30))
    fuel_rect = pygame.Rect((fuel_rect_x,fuel_rect_y),(fuel_limit,30))
    radiation_bg = pygame.Rect((radiation_rect_x,radiation_rect_y),(radiation_bar,30))
    radiation_rect = pygame.Rect((radiation_rect_x,radiation_rect_y),(radiation_limit,30))

    screen.blit(tab_window,(pos_x ,pos_y))
    screen.blit(data_window,(pos_x2 ,pos_y2))
    pygame.draw.rect(screen,'red',oxygen_bg,border_radius = 3)
    pygame.draw.rect(screen,'green',oxygen_rect,border_radius = 3)
    pygame.draw.rect(screen,'red',fuel_bg,border_radius = 3)
    pygame.draw.rect(screen,'green',fuel_rect,border_radius = 3)
    pygame.draw.rect(screen,'red',radiation_bg,border_radius = 3)
    pygame.draw.rect(screen,'green',radiation_rect,border_radius = 3)
    display_letters(f'Oxygen: {int(oxygen_limit/2)}%',oxygen_x,oxygen_y,20,'white')
    display_letters(f'Fuel: {int(fuel_limit/2)}%',fuel_x,fuel_y,20,'white')
    display_letters(f'Radiation: {int(radiation_limit/2)}%',radiation_x,radiation_y,20,'white')
    pygame.draw.rect(screen,'red',[(screen.get_width() - 300)//2,14,300,50],border_top_right_radius = 30,border_bottom_left_radius = 30)
    middle_letters('TAB MENU',0,screen.get_height() * 0.45,40,'white')

    if game_data["gold"] >= 1000:
        if o2_refill_btn.draw():
            oxygen_limit = 200
            game_data["gold"] -= 1000
        if ba_refill_btn.draw():
            radiation_limit = 10
            game_data["gold"] -= 1000
    if game_data["fuel"] >= 1:
        if fuel_refill_btn.draw():
            fuel_limit = 200
            game_data["gold"] -= 1000

        if o2_refill_btn.hover('Cost : 1000 gold','below',5):
            pass
        if fuel_refill_btn.hover('Cost : 1 fuel','below',5):
            pass
        if ba_refill_btn.hover('Cost : 1000 gold','below',5):
            pass
    
    if game_data["spaceship"] == 0:
        screen.blit(default_ship_tab,(spaceship_x - 70,spaceship_y))
        display_letters('Default ship',text_x,text_y,30,'white')
    if game_data["spaceship"] == 1:
        screen.blit(xeroship_tab,(spaceship_x - 70,spaceship_y))
        display_letters('XERO ship',text_x,text_y,30,'white')
    if game_data["spaceship"] == 2:
        screen.blit(zenoship_tab,(spaceship_x - 70,spaceship_y))
        display_letters('ZENO ship',text_x,text_y,30,'white')
    if game_data["spaceship"] == 3:
        screen.blit(furryship_tab,(spaceship_x - 70,spaceship_y))
        display_letters('FURRY ship',text_x,text_y,30,'white')

def ships_skills():
    bullet_group.draw(screen)
    bullet_group.update()
    laser_group.draw(screen)
    laser_group.update()
    projectile_group.draw(screen)
    projectile_group.update()
    skill2_group.draw(screen)
    skill2_group.update()
    furry_ult_group.draw(screen)
    furry_ult_group.update()
    spaceship.exhaust_group.draw(screen)
    spaceship.exhaust_group.update()
    update_spaceship()


def selection_func():
    global state
    screen.blit(pygame.transform.scale(pygame.image.load('graphics/Asset_bg/9.png'),(screen_width,screen_height)).convert_alpha(),(0,0))
    #Header text
    header("Select Your Duo",'orange','black','white')

    # First image positioning
    pos_x = screen.get_width()*0.15
    mid_pos_y = (screen.get_height() - 400)//2
    first_img_x = pos_x + (400 - 300)//2
    first_img_y = (screen.get_height()- 300)//2
    screen.blit(selection_template,(pos_x,mid_pos_y))

    # Second image positioning
    second_pos_x = screen.get_width() - (screen.get_width()*0.15 + 400)
    second_img_x = second_pos_x + (400 - 300)//2

    #Button
    selection_btn = Picture_Button(screen,second_pos_x,mid_pos_y,selection_template)


    if game_data['spaceship'] == 0:
        screen.blit(default_ship_sel,(first_img_x,first_img_y))
    if game_data['spaceship'] == 1:
        screen.blit(xeroship_sel,(first_img_x,first_img_y))
    if game_data['spaceship'] == 2:
        screen.blit(zenoship_sel,(first_img_x,first_img_y))
    if game_data['spaceship'] == 3:
        screen.blit(furryship_sel,(first_img_x,first_img_y))

    # BUTTON LOGIC
    if slot_two == None:
        if add_icon_btn.draw():
            state = State.SELECTION_MENU

    else:
        if selection_btn.draw():
            state = State.SELECTION_MENU

    if forward_btn.draw():
        state = State.LOADING

    if slot_two == 0:
        screen.blit(default_ship_sel,(second_img_x,first_img_y))

    if slot_two == 1:
        screen.blit(xeroship_sel,(second_img_x,first_img_y))

    if slot_two == 2:
        screen.blit(zenoship_sel,(second_img_x,first_img_y))
    if slot_two == 3:
        screen.blit(furryship_sel,(second_img_x,first_img_y))


def selection_menu():
    global state,slot_two
    screen.blit(pygame.transform.scale(pygame.image.load('graphics/Asset_bg/9.png'),(screen_width,screen_height)).convert_alpha(),(0,0))

    header('Choose Your Second Spaceship','orange','black','white')

    back_btn = Picture_Button(screen,10,10, backward_btn_img)

    selection_bg = pygame.transform.scale(pygame.image.load('graphics/Templates/selection_bg.png'),(200,200)).convert_alpha()
    gap = screen.get_width()*0.14
    #available ships
    defaultship_btn = Picture_Button(screen,gap,100,selection_bg)
    xeroship_btn = Picture_Button(screen,gap*2 + 200,100,selection_bg)
    zenoship_btn = Picture_Button(screen,gap*3 + 400,100,selection_bg)
    furryship_btn = Picture_Button(screen,gap,450,selection_bg)

    #na ships
    defaultship_na_btn = Picture_Button(screen,gap,100,selection_bg)
    xeroship_na_btn = Picture_Button(screen,gap*2 + 200,100,selection_bg)
    zenoship_na_btn = Picture_Button(screen,gap*3 + 400,100,selection_bg)
    furryship_na_btn = Picture_Button(screen,gap,450,selection_bg)

    if defaultship_btn.draw():
        slot_two = 0
        state = State.SELECTION
    if game_data['xeroship_owned'] == True:
        if xeroship_btn.draw():
            slot_two = 1
            state = State.SELECTION
    else:
        if xeroship_na_btn.draw():
            pass
        if xeroship_na_btn.below_hover("You don't own this ship",'red',22):
            pass
    if game_data['zenoship_owned'] == True:
        if zenoship_btn.draw():
            slot_two = 2
            state = State.SELECTION
    else:
        if zenoship_na_btn.draw():
            pass
        if zenoship_na_btn.below_hover("You don't own this ship",'red',22):
            pass
    if game_data['furryship_owned'] == True:
        if furryship_btn.draw():
            slot_two = 3
            state = State.SELECTION
    else:
        if furryship_na_btn.draw():
            pass
        if furryship_na_btn.below_hover("You don't own this ship",'red',22):
            pass
    if back_btn.draw():
        state = State.SELECTION

    screen.blit(default_ship_bttn,(gap+(200-150)//2,100+(200-150)//2))
    screen.blit(xeroship_bttn,(gap*2+200+(200-150)//2,100+(200-150)//2))
    screen.blit(zenoship_bttn,(gap*3+400+(200-150)//2,100+(200-150)//2))
    screen.blit(furryship_bttn,(gap+(200-150)//2,450+(200-150)//2))


def check_dailies():
    daily_quest_list = [quest_data["dailies"]["target_playtime"][1],quest_data["dailies"]["pirates_kills"][1]]
    if datetime.now().day != quest_data["dailies"]["last_reset_day"]:
        quest_data["dailies"]["daily_reset"] = True
        print("reseted")
    if all(daily_quest_list):
        quest_data["dailies"]["last_reset_day"] = datetime.now().day
    if quest_data["dailies"]["daily_reset"]:
        quest_data["dailies"]["target_playtime"][1] = False
        quest_data["dailies"]["pirates_kills"][1] = False
        quest_data["dailies"]["lavastone_needed"][1] = False
        quest_data["dailies"]["emerald_needed"][1] = False
        quest_data["dailies"]["craft_needed"][1] = False
        quest_data["dailies"]["wish_needed"][1] = False
        quest_data["dailies"]["last_reset_day"] = datetime.now().day
        quest_data["dailies"]["playtime"] = 0
        quest_data["dailies"]["pirate_killed"] = 0
        quest_data["dailies"]["lavastone_obtained"] = 0
        quest_data["dailies"]["emerald_obtained"] = 0
        quest_data["dailies"]["crafted_item"] = 0
        quest_data["dailies"]["wish_completed"] = 0
        quest_data["dailies"]["daily_reset"] = False




def time_until_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
    remaining_time = midnight - now
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    font = pygame.font.Font("font/gacha.ttf", 20)
    time_remaining = font.render(f"Resetting after - {remaining_time}",True,"lime")
    pos_x = screen_width - (time_remaining.get_width() + 20)
    pos_y = (screen_height - 50 ) + (50 - time_remaining.get_height())//2
    screen.blit(time_remaining,(pos_x,pos_y))

def progress_bar(value,data1,data2,pos_y,ratio,text,reward,data_tree="event"):
    global quest_data
    main_data = quest_data[data_tree][data2]
    sub_data = quest_data[data_tree][data1][0]
    check_data = quest_data[data_tree][data1][1] 
    if main_data >= sub_data:
        quest_data[data_tree][data2] = sub_data
    bg_size_x = None 
    main_size_x = None
    if value == 0:
        bg_size_x = sub_data / ratio
        main_size_x = quest_data[data_tree][data2] / ratio
    if value == 1:
        bg_size_x = sub_data * ratio
        main_size_x = quest_data[data_tree][data2] * ratio
    pos_x = (screen.get_width() - 1000)//2
    bg_rect = pygame.Rect((pos_x, pos_y ), (bg_size_x, 30))
    main_rect = pygame.Rect((pos_x, pos_y ), (main_size_x, 30))
    pygame.draw.rect(screen,'white',bg_rect)
    pygame.draw.rect(screen,'aqua',main_rect)
    pygame.draw.rect(screen,'black',bg_rect,2)


    mission_font = pygame.font.Font('Font/LM.otf',15)
    mission_name = mission_font.render(text,True,'black')
    text_pos_x = (screen.get_width() - mission_name.get_width())/2
    text_pos_y = pos_y + 4
    screen.blit(mission_name,(text_pos_x,text_pos_y))
    claim_button = Rect_Button(screen,100,30,pos_x + 1020,pos_y,'Claim','yellow','red','black',20)
    claimed_button = Rect_Button(screen,100,30,pos_x + 1020,pos_y,'Claimed','white','gray','black',20)
    if main_data >= sub_data and check_data == False:
        if claim_button.draw():
            game_data["jade"] += reward
            quest_data[data_tree][data1][1] = True
    
    

    if check_data == True:
        if claimed_button.draw():
            pass

def dailies_page():
    screen.blit(shop_bg,(0,0))
    header("Dailies","black","#FFC107","white")
    progress_bar(0,"target_playtime","playtime",100,0.9,f"Play 15 minutes (Minutes: {int(quest_data['dailies']['playtime']//60)})",50,"dailies")
    progress_bar(0,'pirates_kills',"pirate_killed",200,1,f"Kill 1000 pirates (Progress: {int(quest_data['dailies']['pirate_killed']//10)}%)",50,"dailies")
    progress_bar(1,"lavastone_needed","lavastone_obtained",300,500,f"Obtain 2 lavastone (Progress: {int(quest_data['dailies']['lavastone_obtained']*50)}%)",50,"dailies")
    progress_bar(1,"emerald_needed","emerald_obtained",400,500,f"Obtain 2 emerald (Progress: {int(quest_data['dailies']['emerald_obtained']*50)}%)",50,"dailies")
    progress_bar(1,"craft_needed","crafted_item",500,500,f"Craft 2 items (Progress: {int(quest_data['dailies']['crafted_item']*50)}%)",50,"dailies")
    progress_bar(1,"wish_needed","wish_completed",600,500,f"Summon 2 time (Progress: {int(quest_data['dailies']['wish_completed']*50)}%)",50,"dailies")

    

def event_page():
    screen.blit(shop_bg,(0,0))
    header("Event","black","#FFC107","white")
    progress_bar(0,'pirates_kills',"pirate_killed",100,100,f"Kill 100000 pirates (Progress: {int(quest_data['event']['pirate_killed']//1000)}%)",500)
    progress_bar(0,'planet_discover',"planet_discovered",200,1,f"Discover 1000 planets (Progress: {int(quest_data['event']['planet_discovered']//10)}%)",500)
    progress_bar(1,'boss_kills','boss_killed',300,10,f"Kill 100 planet bosses (Progress: {int(quest_data['event']['boss_killed'])}%)",500)
    progress_bar(1,'wormhole_discover',"wormhole_discovered",400,20,f"Discover 50 Wormholes (Progress: {int(quest_data['event']['wormhole_discovered']*2)}%)",500)
    progress_bar(0,'meteor_destroy',"meteor_destroyed",500,10,f"Destroy 10000 meteors (Progress: {int(quest_data['event']['meteor_destroyed']//100)}%)",500)
    progress_bar(1,'spacestation_found','spacestation_founded',600,50,f"Discover 20 Spacestation (Progress: {int(quest_data['event']['spacestation_founded']*5)}%)",500)


def clean_space_screen():
    pirate_group.empty()
    blackhole_group.empty()
    meteor_group.empty()
    crystal_group.empty()
    planet_group.empty()
    hp_group.empty()
    explosion_group.empty()
    for skills in boss_skill_group_list:
        skills.empty()

def clean_planet_screen():
    boss_group.empty()
    boss_aa_group.empty()
    boss_ultimate_group.empty()
    explosion_group.empty()
    for skills in boss_skill_group_list:
        skills.empty()

def pirates_spaceship_collisions():
    global health,state
    pirate_spaceship = pygame.sprite.groupcollide(spaceship_group, pirate_group,False, True)
    for skill in skill_group_list:
        for pirate in pirate_group:
            if pygame.sprite.groupcollide(pirate_group, skill,True, False):
                sfx_channel.play(explosion_sound)
                create_explosion(explosion_group, pirate.rect.topleft[0],pirate.rect.topleft[1], size=6)
    pirate_bullet = pygame.sprite.groupcollide(pirate_group, bullet_group, True, True)
    if pirate_spaceship:
        health -= 1
        explosion_group.draw(screen)
        explosion_group.update()
        sfx_channel.play(explosion_sound)
    if pirate_bullet:
        sfx_channel.play(explosion_sound)

    for pirate in pirate_bullet:
        create_explosion(explosion_group, pirate.rect.topleft[0],pirate.rect.topleft[1], size=6)
# def spaceship_object_collisions:
#     global health
#     spaceship_health = pygame.sprite.groupcollide(hp_group,spaceship_group,True,False)
#     spaceship_meteor = 

GAME_STATE = [State.ALIVE,State.PLANETERY_ENTER,State.CAMPAIGN,state.RESEARCH]

current_state = None
def pause_menu(resume_state):
    global state 
    menu_background.generate_random_background()
    pause_font = pygame.font.Font('font/LM.otf',40)
    pause_text = pause_font.render('Pause Menu', True, 'lime')
    screen.blit(pause_bg,(0,0))
    pygame.draw.rect(screen,'orange',[(screen.get_width() - pause_text.get_width())//2 - 40,10,pause_text.get_width()+ 40*2,pause_text.get_height()],border_radius = 40,width = 2)
    screen.blit(pause_text,((screen.get_width() - pause_text.get_width())//2 ,10))
    music_disk.update(pygame.event.get())
    music_disk.draw(screen)
    if resume_button.draw():
        state = resume_state
    if menu_button.draw():
        state = State.MENU

while run:
    volume_adjustment()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = State.QUIT
        elif event.type == PLANET_REGEN_TIMER and state == State.ALIVE:
            new_planet = Planet()
            planet_group.add(new_planet)
            set_planet_timer()
        elif event.type == BLACKHOLE_REGEN_TIMER and state == State.ALIVE:
            new_blackhole = Blackhole()
            blackhole_group.add(new_blackhole)
            set_blackhole_timer()
        elif event.type == METEOR_REGEN_TIMER and state == State.ALIVE:
            new_meteor = Meteor()
            meteor_group.add(new_meteor)
            set_meteor_timer()
        elif event.type == HEALTH_REGEN_TIMER and state == State.ALIVE:
            new_health = Health()
            hp_group.add(new_health)
            set_health_timer()
        elif event.type == CRYSTAL_REGEN_TIMER and state == State.ALIVE:
            new_crystal = Crystal()
            crystal_group.add(new_crystal)
            set_crystal_timer()
        elif event.type == WORMHOLE_REGEN_TIMER and state == State.ALIVE:
            new_wormhole = Wormhole()
            wormhole_group.add(new_wormhole)
            set_wormhole_timer()
        elif event.type == SPACESTATION_REGEN_TIMER and state == State.ALIVE:
            new_spacestation = Spacestation()
            spacestation_group.add(new_spacestation)
            set_spacestation_timer()



    # INFINITY MODE BULLET CREATION
        if event.type == pygame.MOUSEBUTTONDOWN and state in GAME_STATE:
            if event.button == 3:
                bullet = spaceship.create_bullets()
                bullet_group.add(bullet)
                laser_channel.play(laser_sound)



        if event.type == pygame.KEYDOWN:
            if event.key == K_f:
                screen = pygame.display.set_mode((screen_width, screen_height),FULLSCREEN) 
            if event.key == K_x:
                screen = pygame.display.set_mode((screen_width, screen_height)) 


            if event.key == K_1 and state in GAME_STATE:
                game_data['spaceship'] = slot_one
                update_all_damage()
                speed_amount()


            if slot_two!=None:
                if event.key == K_2 and state in GAME_STATE:
                    game_data['spaceship'] = slot_two
                    update_all_damage()
                    speed_amount()



            


    # INFINITY MODE XEROSHIP SKILL
            if event.key == K_e and state in GAME_STATE and game_data["spaceship"] == 1 and xeroship_skill_timer == 1000:
                xero_skill = spaceship.skill_2()
                skill2_group.add(xero_skill)
                xeroship_skill_timer = 0



    # INFINITY MODE XEROSHIP ULTIMATE
            if event.key == K_r and state in GAME_STATE and game_data["spaceship"] == 1 and xeroship_ult_timer == 2000:
                projectile1 = spaceship.projectile1()
                projectile_group.add(projectile1)
                xeroship_ult_timer = 0



    # INFINITY MODE ZENOSHIP SKILL
            if event.key == K_e and state in GAME_STATE and game_data["spaceship"] == 2  and zenoship_mana>=50:
                sfx_channel.play(teleport_sound)
                spaceship.zenoship_skill()
                zenoship_mana -= 50




    # INFINITY MODE ZENOSHIP ULT
            if event.key == K_r and state in GAME_STATE and game_data["spaceship"] == 2 and zenoship_mana >= 500:
                lasers = spaceship.creating_laser()
                laser_group.add(lasers)
                zenoship_mana -= 500

    # INFINITY MODE FURRYSHIP SKILL
            if event.key == K_e and state in GAME_STATE and game_data["spaceship"] == 3 and health_orbs >= 100:
                health += 1
                health_orbs = 0



     # INFINITY MODE FURRYSHIP ULTIMATE            
            if event.key == K_r and state in GAME_STATE and game_data["spaceship"] == 3 and furryship_ult_timer == 1500:
                meteor_shower = spaceship.furryship_ultimate()
                furry_ult_group.add(meteor_shower)
                furryship_ult_timer = 0
                for _ in range(4):
                    new_meteor = Shower()
                    furry_ult_group.add(new_meteor)



            if event.key == K_TAB and state == State.ALIVE:
                state = State.TAB_MENU


            if event.key == K_ESCAPE and state in GAME_STATE and state != State.CAMPAIGN:     
                current_state = state           
                state = State.PAUSE
    # LASER BEAM LOGIC
    if state in GAME_STATE:
        if game_data["spaceship"] == 0 and game_data["defaultship_equipment"]["laser_beam"] and spaceship.can_shoot():
            bullets = spaceship.create_bullets()
            bullet_group.add(bullets)
            laser_channel.play(laser_sound)
            spaceship.reset_shoot_cooldown() 
        elif game_data["spaceship"] == 1 and game_data["xeroship_equipment"]["laser_beam"] and spaceship.can_shoot():
            bullets = spaceship.create_bullets()
            bullet_group.add(bullets)
            laser_channel.play(laser_sound)
            spaceship.reset_shoot_cooldown() 

        elif game_data["spaceship"] == 2 and game_data["zenoship_equipment"]["laser_beam"] and spaceship.can_shoot():
            bullets = spaceship.create_bullets()
            bullet_group.add(bullets)
            laser_channel.play(laser_sound)
            spaceship.reset_shoot_cooldown() 

        elif game_data["spaceship"] == 3 and game_data["furryship_equipment"]["laser_beam"] and spaceship.can_shoot():
            bullet = spaceship.create_bullets()
            bullet_group.add(bullet)
            laser_channel.play(laser_sound)
            spaceship.reset_shoot_cooldown() 


    if state == State.START_BGM:
        music_channel.play(menu_music,loops=-1)
        update_all_damage()
        state = State.MENU
    if state == State.MODES:
        game_modes()
        infinity_button.draw()
        campaign_button.draw()
        research_button.draw()
        if menu_back_button.draw():
            state = State.MENU
    if state == State.EVENT:
        event_page()
        shop_bottombar(jade_icon,game_data["jade"])
        if menu_back_button.draw():
            state = State.MENU
        if dailies_button.draw():
            state = State.JOURNEY
        if event_button.draw():
            state = State.EVENT
            
    if state == State.JOURNEY:
        dailies_page()
        shop_bottombar(jade_icon,game_data["jade"])
        time_until_midnight()
        if menu_back_button.draw():
            state = State.MENU
        if event_button.draw():
            state = State.EVENT
        if dailies_button.draw():
            state = State.JOURNEY

        # middle_letters('Comming Soon',0,0,40,'red')
    if state == State.PLANETERY_OPTION:
        confirm_font = pygame.font.Font('Font/LM.otf',30)
        confirm_text = confirm_font.render('Are You Sure For The Boss Fight?',True,'white')
        screen.fill('black')
        screen.blit(confirm_text,((screen.get_width() - confirm_text.get_width())//2,(screen.get_height()- confirm_text.get_height())//2 - 80))
        yes_button.draw()
        no_button.draw()
    if state == State.PLANETERY_LOADING:
        screen.fill('black')
        random_boss = random.choice([1,2])
        clean_planet_screen()
        planetery_load(State.PLANETERY_ENTER)

    if state == State.PAUSE:
       pause_menu(current_state)
    if state == State.TAB_MENU:
        tab_menu()
        if backward_btn.draw():
            state = State.LOADING

    if state == State.MENU:
        menu_background_group.draw(screen)
        menu_background_group.update()
        draw_menu()
        reset_game()
        check_dailies()
        score = 0
        xeroship_skill_timer = 0
        xeroship_ult_timer = 0
        loading_time = 0
        zenoship_mana = 500
        furryship_ult_timer = 0
        oxygen_limit = 200
        fuel_limit = 200
        radiation_limit = 10
        pirate_count = 8
        health_amount()
        speed_amount()
        slot_two = None
        game_data["spaceship"]  = saved_ship
        slot_one = game_data["spaceship"]


    if state == State.SELECTION:
        selection_func()
        if modes_back_button.draw():
            state = State.MODES

    if state == State.SELECTION_MENU:
        selection_menu()

    if state == State.LOADING:
        if loading_time < 100:
            loading_time += 1
            loading_animation(f'loading {loading_time}%')
            if loading_time >= 100:
                loading_time = 0 
                state = State.ALIVE  #you can put any condition you want
    if state == State.SHOP:
        shop_menu()


    if state == State.GACHA:
        # limited_banner, permanent_banner = gacha_menu(limited_banner,permanent_banner)
        gacha.menu()
    if state == State.GACHA_ROLL:
        gacha.roll()
        # state = State.GACHA_RESULT
    if state == State.GACHA_RESULT:
        gacha.result()
        if gacha_back_button.draw():
            state = State.GACHA
    if state == State.SHIPS_INV:
        ships_inv()
    if state == State.UPGRADE_INV:
        upgrade_menu(game_data["spaceship"])
    if state == State.THRUSTER:
        select_thruster()
    if state == State.CANNON:
        select_cannon()
    if state == State.ITEMS_INV:
        items_inv()
    if state == State.ITEMS_INV2:
        items_inv2()
    if state == State.CRAFTING:
        crafting_inv()
        if game_data["coal"] >= 100:
            if fuel_craft_btn.draw():
                game_data["coal"] -= 100
                game_data["fuel"] += 1
                quest_data["dailies"]["crafted_item"] += 1
            fuel_craft_btn.hover(f"Spend 100 coal to get 1 fuel","below",20)
        else:
            if fuel_craft_btn.draw():
                pass 
            fuel_craft_btn.hover(f"Need 100 coal(Coal - {game_data['coal']})",'below',20)
        if game_data["gold_ore"] >= 100:
            if gold_craft_btn.draw():
                game_data["gold_ore"] -= 100 
                game_data["gold"] += 5000
                quest_data["dailies"]["crafted_item"] += 1
            gold_craft_btn.hover(f"Spend 100 gold ores to craft 5000 gold","below",20)
        else:
            if gold_craft_btn.draw(): 
                pass 
            gold_craft_btn.hover(f"Need 100 gold ores(Gold ore - {game_data['gold_ore']})",'below',20)

    if state == State.EXHAUST:
        exhaust_inv()

    if state == State.SETTINGS:
        screen.blit(settings_bg,(0,0))
        sound_bar()
        if sound_button.draw():
            state = State.SETTINGS
        if display_button.draw():
            state = State.DISPLAY

        if menu_back_button.draw():
            state = State.MENU
        if settings_data["sound"]["music"] < 100:
            if music_increase_btn.draw(20):
                settings_data["sound"]["music"] += 10
        if settings_data["sound"]["music"] > 0:
            if music_decrease_btn.draw(20):
                settings_data["sound"]["music"] -= 10
        if settings_data["sound"]["sfx"] < 100:
            if sfx_increase_btn.draw(20):
                settings_data["sound"]["sfx"] += 10
        if settings_data["sound"]["sfx"] > 0:
            if sfx_decrease_btn.draw(20):
                settings_data["sound"]["sfx"] -= 10




    if state == State.DISPLAY:
        screen.blit(settings_bg,(0,0))
        if sound_button.draw():
            state = State.SETTINGS
        if display_button.draw():
            state = State.DISPLAY
        header('Display Settings')
        if seven_twenty_button.draw():
            settings_data["screen_width"] = 1280
            settings_data["screen_height"] = 720
            state = State.QUIT
        seven_twenty_button.hover("Restart to apply  changes",'below',20)
        if seven_sixty_eight_button.draw():
            settings_data["screen_width"] = 1366
            settings_data["screen_height"] = 768
            state = State.QUIT
        seven_sixty_eight_button.hover("Restart to apply  changes",'below',20)
        if menu_back_button.draw():
            state = State.MENU

   


    if state == State.SPACESTATION_ENTER:
        screen.fill('black')
        if enter_bar < 880:
            enter_bar += 10
        if enter_bar >= 880:
            state = State.SPACESTATION
            enter_bar = 10
        display_letters(f'Entering {random_galaxy} spacestation',220,270,40,'white')
        spacestation_loading_bg = pygame.Rect((200,340),(880,40))
        spacestation_loading = pygame.Rect((200,340),(enter_bar,40))
        pygame.draw.rect(screen,'red',spacestation_loading_bg,border_radius = 6)
        pygame.draw.rect(screen,'green',spacestation_loading,border_radius = 6)   
    if state == State.SPACESTATION_EXIT:
        screen.fill('black')
        if leave_bar < 880:
            leave_bar += 10
        if leave_bar >= 880:
            state = State.ALIVE
            leave_bar = 10
        display_letters(f'leaving {random_galaxy} spacestation',220,270,40,'white')
        spacestation_loading_bg = pygame.Rect((200,340),(880,40))
        spacestation_leaving = pygame.Rect((200,340),(leave_bar,40))
        pygame.draw.rect(screen,'red',spacestation_loading_bg,border_radius = 6)
        pygame.draw.rect(screen,'green',spacestation_leaving,border_radius = 6)


    if state == State.SPACESTATION:
        spacestation_menu()


    if state == State.ALIVE:
        boss_01_hp = 100000
        # ENSURE ALWAYS 8 PIRATES STAY IN THE SCREEN
        if (len(pirate_group)) < pirate_count:
            new_pirate = Pirate()
            pirate_group.add(new_pirate)

        # RANDOM BG MUSIC
        

        # SPACESHIP WARNINGS 
        oxygen_limit -= 0.005
        fuel_limit -= 0.001
        radiation_limit += 0.003
        if fuel_limit <= 40 and not fuel_warning_triggered:
            warning_channel.play(fuel_warning)
            fuel_warning_triggered = True
        if oxygen_limit <= 40 and not oxygen_warning_triggered:
            warning_channel.play(oxygen_warning)
            oxygen_warning_triggered = True
        if radiation_limit>=160 and not radiation_warning_triggered:
            warning_channel.play(radiation_warning)
            radiation_warning_triggered = True

   # XEROSPACESHIP SKILL COOLDOWN AND TIMER LOGIC
        xeroship_skill_timer += 1
        if xeroship_skill_timer >= 1000:
            xeroship_skill_timer =1000
        xeroship_ult_timer +=1
        if xeroship_ult_timer >=2000:
            xeroship_ult_timer = 2000
    # ZENOSHIP SKILL AND COOLDOWN LOGIC
        zenoship_mana += 0.2
        if zenoship_mana >= 600:
            zenoship_mana = 600
    # FURRYSPACESHIP SKILL COOLDOWN AND TIMER LOGIC
        furryship_ult_timer +=2
        if furryship_ult_timer >= 1500:
            furryship_ult_timer = 1500



        if health == 0 or oxygen_limit <= 0 or fuel_limit <= 0 or radiation_limit >= 200:
            state = State.DEAD

        #meteor collisions
        meteor_collide = pygame.sprite.groupcollide(meteor_group,spaceship_group,True,False)
        for _ in range(len(meteor_collide)):
            health -=1


        #health regen collisions
        hp_regenarate = pygame.sprite.groupcollide(spaceship_group,hp_group,False,True)
        if hp_regenarate:
            health +=1


        # Detect collisions between lasor and bullets
        laser_collisions = pygame.sprite.groupcollide(pirate_group,laser_group,True,False)
        # Create new pirates to replace destroyed ones
        for pirate in laser_collisions:
            sfx_channel.play(explosion_sound)
            score += 10
            quest_data['event']['pirate_killed'] += 1
            quest_data['dailies']['pirate_killed'] += 1
            


        # Detect collisions between pirates and bullets
        collisions = pygame.sprite.groupcollide(pirate_group, bullet_group, True, True)
        collisions2 = pygame.sprite.groupcollide(skill2_group, pirate_group, False, True)
        collisions3 = pygame.sprite.groupcollide(furry_ult_group, pirate_group, False, True)

        if collisions3:
            if game_data["spaceship"] == 3:
                health_orbs +=1
        # Create new pirates to replace destroyed ones
        for pirate in collisions or collisions2 or collisions3:
            sfx_channel.play(explosion_sound)
            score += 10
            quest_data['event']['pirate_killed'] += 1
            quest_data['dailies']['pirate_killed'] += 1



        spacestation_entry = pygame.sprite.groupcollide(spacestation_group, spaceship_group, True, False)
        if spacestation_entry:
            state = State.SPACESTATION_ENTER
            quest_data['event']['spacestation_founded'] +=1
           
        meteor_destroy = pygame.sprite.groupcollide(meteor_group, projectile_group, True, True)
        meteor_destroy2 = pygame.sprite.groupcollide(skill2_group, meteor_group, False, True)
        meteor_destroy3 = pygame.sprite.groupcollide(furry_ult_group, meteor_group, False, True)
        meteor_destroy4 = pygame.sprite.groupcollide(laser_group, meteor_group, False, True)

        if meteor_destroy or meteor_destroy2 or meteor_destroy3 or meteor_destroy4:
            quest_data['event']['meteor_destroyed'] += 1
            if game_data["spaceship"] == 3:
                health_orbs +=1

            random_mat = random.randint(1,101)
            if random_mat > 0 and random_mat <= 35:
                random_silver = random.randint(5,50)
                game_data["silver"] += random_silver
            if random_mat > 35 and random_mat <= 39:
                random_gold_ore = random.randint(2,7)
                game_data["gold_ore"] += random_gold_ore
            if random_mat > 40 and random_mat <= 49:
                random_iron = random.randint(3,10)
                game_data["iron"] += random_iron
            if random_mat > 50 and random_mat <= 69:
                random_coal = random.randint(1,100)
                game_data["coal"] += random_coal
            if random_mat > 70 and random_mat <=79:
                random_platinum = random.randint(1,5)
                game_data["platinum"] += random_platinum
            if random_mat > 80 and random_mat <=99:
                random_copper = random.randint(20,100)
                game_data["copper"] += random_copper
            if random_mat == 40:
                game_data["purple gemstone"] += 1
            if random_mat == 50:
                game_data["emerald"] += 1
                quest_data["dailies"]["emerald_obtained"] += 1
            if random_mat == 70:
                game_data["frost crystal"] += 1
            if random_mat == 80:
                game_data["iridium"] += 1
            if random_mat == 100:
                game_data["lavastone"] += 1
                quest_data["dailies"]["lavastone_obtained"] +=1


        death = pygame.sprite.groupcollide(spaceship_group,pirate_group,False,True)
        if death:
            sfx_channel.play(explosion_sound)
        for _ in range(len(death)):
            health -= 1
            


        fake_planet_blackhole_collision = pygame.sprite.groupcollide(planet_group,blackhole_group,False,False)
        fake_planet_ship_collision = pygame.sprite.groupcollide(planet_group,spaceship_group,False,False)
        ship_blackhole_collision = pygame.sprite.groupcollide(spaceship_group,blackhole_group,False,False)
        if ship_blackhole_collision:
            health = 0

        if pygame.sprite.groupcollide(spaceship_group, wormhole_group, False, True):
            pirate_count += 1
            quest_data['event']['wormhole_discovered'] +=1
            new_pirate_num = random.randrange(1,26)
            while new_pirate_num == pirate_num:
                # Keep selecting a new image until it's different
                new_pirate_num = random.randrange(1,26)
            pirate_num = new_pirate_num
            pirate_num = random.randrange(1,26)
            random_galaxy = random.choice(galaxy_names)
            state = State.WARPING
            


        
        #CRYSTAL REWARDS  LOGIC
        crystal_laser_collsions = pygame.sprite.groupcollide(crystal_group,laser_group,True,False)
        for  _ in range(len(crystal_laser_collsions)):
            random_crystal = random.randrange(1,5)
            game_data["jade"] += random_crystal

        crystal_bullet_collsions = pygame.sprite.groupcollide(crystal_group,bullet_group,True,False)
        for  _ in range(len(crystal_bullet_collsions)):
            random_gold = random.randrange(1,500)
            game_data["gold"] += random_gold
        crystal_shield_collisions = pygame.sprite.groupcollide(crystal_group,skill2_group,True,False)
        for  _ in range(len(crystal_shield_collisions)):
            random_crystal = random.randrange(1,5)
            game_data["jade"] += random_crystal



        background_group.draw(screen)
        background_group.update()

        planet_group.draw(screen)
        planet_group.update()
        blackhole_group.draw(screen)
        blackhole_group.update()
        meteor_group.draw(screen)
        meteor_group.update()  
        hp_group.draw(screen)
        hp_group.update()
        crystal_group.draw(screen)
        crystal_group.update()
        wormhole_group.draw(screen)
        wormhole_group.update()
        spacestation_group.draw(screen)
        spacestation_group.update()

        ships_skills()
        pirate_group.draw(screen)
        pirate_group.update()
        explosion_group.draw(screen)
        explosion_group.update()
        display_score(score)
        volume_adjustment()


        if fake_planet_ship_collision:
            loading_bar(spaceship_group,planet_group,False,True)
        else:
            scan_bar = 10
        if fake_planet_blackhole_collision:
            sucking_animation(blackhole_group,planet_group,False,True)
        else:
            sucking_bar = 10

        if meteor_collide:
            screen.blit(boom_surf2,spaceship.rect.topleft )
        if meteor_destroy or meteor_destroy2 or meteor_destroy3 or meteor_destroy4:
            screen.blit(boom_surf2,meteor.rect.topleft )

        for pirate in collisions or laser_collisions or collisions2 or collisions3 or death:
            create_explosion(explosion_group, pirate.rect.topleft[0],pirate.rect.topleft[1], size=6)

    if state == State.DEAD:
        screen.fill('black')
        middle_letters(f'GAME OVER',0,0,100,'red')
        game_data['spaceship'] = saved_ship
        if menu_btn.draw():
            state = State.START_BGM

    if state == State.WARPING:
        warp_time += 1
        screen.fill('black')
        display_fstring(f'Warping : {warp_time}% to {random_galaxy}','white',550,320)
        if warp_time >= 100:
            warp_time = 0
            state = State.ALIVE
            background.generate_random_background()
            clean_space_screen()

            for _ in range(8):
                new_pirate = Pirate()
                #new_pirate.pirate_regenerate()  # Call pirate_regenerate to update the appearance
                pirate_group.add(new_pirate)
    if state == State.ALIVE:
         # Calculate FPS
        fps = int(clock.get_fps())


        # Render the FPS count as text
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 50))
        display_fstring(f'Health: {health}','white',10,10)
        display_fstring(f'Galaxy: {random_galaxy}','cyan',10,30)
        if game_data["spaceship"] == 1:
            display_fstring(f'Skill: {int(xeroship_skill_timer/10)}%','green',10,70)
            display_fstring(f'Ultimate: {int(xeroship_ult_timer/20)}%','yellow',10,90)
        if game_data["spaceship"] == 2:
            display_fstring(f'Mana: {int(zenoship_mana)}','green',10,70)
        if game_data["spaceship"] == 3:
            if health_orbs <100:
                display_fstring(f'Orbs: {health_orbs}','green',10,70)
            else:
                display_fstring(f'Skill: Heal + 1','green',10,70)
            display_fstring(f'Ultimate: {int(furryship_ult_timer/15)}%','yellow',10,90)



    if state == State.PLANETERY_EXIT:
        blackhole_group.empty()
        state = State.LOADING
# PLANETERY ENTER ZONE
    if state == State.PLANETERY_ENTER:
        # XEROSPACESHIP SKILL COOLDOWN AND TIMER LOGIC
        if game_data["spaceship"] == 1:
            xeroship_skill_timer += 1
            if xeroship_skill_timer >= 1000:
                xeroship_skill_timer =1000
            xeroship_ult_timer +=1
            if xeroship_ult_timer >=2000:
                xeroship_ult_timer = 2000
    # ZENOSHIP SKILL AND COOLDOWN LOGIC
        if game_data["spaceship"] == 2:
            zenoship_mana += 0.2
            if zenoship_mana >= 600:
                zenoship_mana = 600
    # FURRYSPACESHIP SKILL COOLDOWN AND TIMER LOGIC
        if game_data["spaceship"] == 3:
            furryship_ult_timer +=2
            if furryship_ult_timer >= 1500:
                furryship_ult_timer = 1500



        # SHIELD LOGIC
        for skills in boss_skill_group_list:
            pygame.sprite.groupcollide(boss_ultimate_group,skills,False,True)
    # COLLISION LOGIC AND RESULT
        boss01_bullet_collision = pygame.sprite.groupcollide(boss_group,bullet_group,False,True)
        if boss01_bullet_collision:
            sfx_channel.play(explosion_sound)
            boss_01_hp -= aa_damage

        # XEROSHIP COLLISIONS
        boss01_xeroskill = pygame.sprite.groupcollide(boss_aa_group,skill2_group,True,False)

        boss01_xeroult_collision = pygame.sprite.groupcollide(boss_group,projectile_group,False,True)
        if boss01_xeroult_collision:
            sfx_channel.play(explosion_sound)
            boss_01_hp -= ultimate_damage

        # ZENOSHIP COLLISSIONS
        boss01_zenoult = pygame.sprite.groupcollide(boss_group,laser_group,False,True)
        if boss01_zenoult:
            sfx_channel.play(explosion_sound)
            boss_01_hp -= ultimate_damage

        # FURRYSHIP COLLISIONS
        boss01_furryult =  pygame.sprite.groupcollide(boss_group,furry_ult_group,False,True)
        if boss01_furryult:
            health_orbs += 5
            sfx_channel.play(explosion_sound)
            boss_01_hp -= ultimate_damage



        # Check for collisions with boss_aa_group
        boss01_collisions_aa = pygame.sprite.groupcollide(spaceship_group, boss_aa_group, False, True)

        # Check for collisions with boss_01_ultimate_group
        boss01_collisions_ultimate = pygame.sprite.groupcollide(spaceship_group, boss_ultimate_group, False, True)

        # Combine the results
        spaceship_death = boss01_collisions_aa or boss01_collisions_ultimate

        if spaceship_death:
            sfx_channel.play(explosion_sound)
            health -= 1
            if health == 0:
                state = State.DEAD



        if boss_01_hp <= 0:
            clean_space_screen()
            set_planet_timer()
            boss_01_hp = 0
            quest_data['event']['boss_killed'] +=1
            state = State.PLANETERY_EXIT

            

    # DRAWING SPRITES AND ELEMENTS ON THE SCREEN
        planetery_bg_group.draw(screen)
        planetery_bg_group.update()
        
        if random_boss == 1:
            boss_group.add(boss_01)
        if random_boss == 2:
            boss_group.add(boss_02)
        boss_group.draw(screen)
        boss_group.update()
        boss_aa_group.draw(screen)
        boss_aa_group.update()
        boss_ultimate_group.draw(screen)
        boss_ultimate_group.update()
        ships_skills()
        volume_adjustment()
        if random_boss == 1:
            Bossbar(boss_01_mhp,boss_01_hp,125,f'Mechanical Cyborg : {boss_01_hp}')
        if random_boss == 2:
            Bossbar(boss_01_mhp,boss_01_hp,125,f'Dark Harbinger : {boss_01_hp}')
        if menu_back_button.draw():
            state = State.START_BGM
        display_score(score)
        fps = int(clock.get_fps())
        if spaceship_death:
            screen.blit(boom_surf2,(spaceship.rect.x - 35,spaceship.rect.y - 95))
        if boss01_bullet_collision or boss01_xeroskill or boss01_xeroult_collision or boss01_zenoult or boss01_furryult:
            if random_boss == 1:
                screen.blit(boom_surf2,(boss_01.rect.x + 65,boss_01.rect.y + 10))
            if random_boss == 2:
                screen.blit(boom_surf2,(boss_02.rect.x,boss_02.rect.y))


        # Render the FPS count as text
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 50))
        display_fstring(f'Health: {health}','white',10,10)
        display_fstring(f'Planet: {random_planet}','cyan',10,30)
        if game_data["spaceship"] == 1:
            display_fstring(f'Skill: {int(xeroship_skill_timer/10)}%','green',10,70)
            display_fstring(f'Ultimate: {int(xeroship_ult_timer/20)}%','yellow',10,90)
        if game_data["spaceship"] == 2:
            display_fstring(f'Mana: {int(zenoship_mana)}','green',10,70)
        if game_data["spaceship"] == 3:
            if health_orbs <100:
                display_fstring(f'Orbs: {health_orbs}','green',10,70)
            else:
                display_fstring(f'Skill: Heal + 1','green',10,70)
            display_fstring(f'Ultimate: {int(furryship_ult_timer/15)}%','yellow',10,90)

    if state == State.QUIT:
        end_time = time()
        previous_play_time = quest_data["dailies"]["playtime"]
        playtime_duration = previous_play_time + (end_time - start_time)
        quest_data["dailies"]["playtime"] = round(playtime_duration)
        run = False
        save_all_data()


    if state == State.CAMPAIGN:
        # boss_group.add(boss_01)
        # planetery_bg_group.draw(screen)
        # planetery_bg_group.update()
        # boss_group.draw(screen)
        # boss_group.update()
        # boss_aa_group.draw(screen)
        # boss_aa_group.update()
        # boss_ultimate_group.draw(screen)
        # boss_ultimate_group.update()
        # spaceship_group.draw(screen)
        # spaceship_group.update()
        # ships_skills()
        # if menu_back_button.draw():
        #     state = State.MENU
        # screen.fill("black")
        # draw_space(screen)
        # screen.blit(spaceship_img,(0,0))
        screen.fill("black")
        middle_letters(f"Comming Soon",0,0,100,"red")
        if backward_btn.draw():
            state = State.MODES
    if state == State.RESEARCH:
        if (len(pirate_group)) < pirate_count:
            new_pirate = Pirate()
            pirate_group.add(new_pirate)
        background_group.draw(screen)
        background_group.update()
        spaceship_group.draw(screen)
        spaceship_group.update()
        pirate_group.draw(screen)
        pirate_group.update()
        explosion_group.draw(screen)
        explosion_group.update()
        ships_skills()
        pirates_spaceship_collisions()

        xeroship_skill_timer += 1
        if xeroship_skill_timer >= 1000:
            xeroship_skill_timer =1000
        xeroship_ult_timer +=1
        if xeroship_ult_timer >=2000:
            xeroship_ult_timer = 2000
    # ZENOSHIP SKILL AND COOLDOWN LOGIC
        zenoship_mana += 0.2
        if zenoship_mana >= 600:
            zenoship_mana = 600
    # FURRYSPACESHIP SKILL COOLDOWN AND TIMER LOGIC
        furryship_ult_timer +=2
        if furryship_ult_timer >= 1500:
            furryship_ult_timer = 1500

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 50))
        display_fstring(f'Health: {health}','white',10,10)
        display_fstring(f'Planet: {random_planet}','cyan',10,30)
        if game_data["spaceship"] == 1:
            display_fstring(f'Skill: {int(xeroship_skill_timer/10)}%','green',10,70)
            display_fstring(f'Ultimate: {int(xeroship_ult_timer/20)}%','yellow',10,90)
        if game_data["spaceship"] == 2:
            display_fstring(f'Mana: {int(zenoship_mana)}','green',10,70)
        if game_data["spaceship"] == 3:
            if health_orbs <100:
                display_fstring(f'Orbs: {health_orbs}','green',10,70)
            else:
                display_fstring(f'Skill: Heal + 1','green',10,70)
            display_fstring(f'Ultimate: {int(furryship_ult_timer/15)}%','yellow',10,90)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
