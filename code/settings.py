import pygame, pathlib, sys, json
from button import Button

'''this file contains all the constants and datas, and functions used to access the save files'''

#constants
DIS_W = 1280
DIS_H = 720
FPS = 60
TILESIZE = 64
FONT = "../graphics/Cubic_11_110.ttf"
TITLE = "Disaster Survival"
BUTTON_HOVER_COLOR = "white"
BUTTON_BASE_TEXT = "white"
MAIN_COLOR = "#aa7959"
SUPPORT_COLOR = "#c49a6c"
SCALE = 4
SAVES_DIR = pathlib.Path().absolute() / "saves"
SAVES_DIR.mkdir(exist_ok=True)

class Save:
    '''this class creates a save file and allows the program to access and change the file'''
    def __init__(self, save_number, saves_dir):
        self.save_number = save_number
        self.path = saves_dir

    def save_data(self, data):
        cur_save_dir = self.path / ("save" + str(self.save_number) + ".json")
        with open(cur_save_dir, "w") as file:
            json.dump(data, file)

    def load_save(self):
        cur_save_dir = self.path / ("save" + str(self.save_number) + ".json")
        with open(cur_save_dir, "r") as file:
            data = json.load(file)
        return data

class SaveMenu:
    '''creates the save menu and allow the player to choose a save file to load'''
    def __init__(self, saves_dir):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, 35)
        self.running = True
        self.path = saves_dir
        self.buttons = []

        self.back_button = Button(None, 150, 100, "Back", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)
        for index, save in enumerate(self.path.iterdir()):
            if save.is_file():
                self.buttons.append(Button(None, DIS_W // 2, 200 + 70*index, "Save " + str(index+1), self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR))

    def run(self):
        while self.running:
            self.display.fill(MAIN_COLOR)
            mouse = pygame.mouse.get_pos()

            self.back_button.change_color(mouse)
            self.back_button.update(self.display)

            for button in self.buttons:
                button.change_color(mouse)
                button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.check_input(mouse):
                        self.running = False
                    for number, button in enumerate(self.buttons):
                        if button.check_input(mouse):
                            self.running = False
                            return number + 1

            pygame.display.update()

#save information
saves = [save for save in SAVES_DIR.iterdir() if save.is_file()]
save_file = [Save(len(saves)+1, SAVES_DIR)]
cutscenes = [(1, "dialogue1"), (5, "dialogue2"), (15, "first_aid"), (20, "end")]
items = ["rocks", "sand", "charcoal", "bottle"]
game_data = [{"save number": len(saves) + 1, "level": 1, "inventory": {}, "health": 3,
              "activated cutscenes": []}]

def get_data():
    #gets data from the save selected
    save = SaveMenu(SAVES_DIR).run()
    if save != None:
        global save_file
        global game_data
        save_file[0] = Save(save, SAVES_DIR)
        game_data[0] = save_file[0].load_save()
        return True
    return False

#object data

monster_data = {
    "skeleton": {
        "health": 10,
        "speed": 3,
        "damage": 1,
        "resistance": 2,
        "attack_radius": 50,
        "notice_radius": 300,
        "attack_type": "weapon"
    }
}

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 1,'graphic':'../graphics/weapons/sword/full.png'},
}

herb_data = {
    "daisy": 1,
    "mugwort": 1,
    "sheperd's purse": 1,
    "scurvy grass": 2,
    "fool's watercress": 1,
    "fool's parsley": -1,
    "deadly nightshade": -2,
    "foxglove": -1
}