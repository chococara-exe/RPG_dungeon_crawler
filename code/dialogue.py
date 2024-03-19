import pygame, json, sys
from settings import *
from button import Button

'''the dialogue is created using a tree data structure, where each dialogue node will lead 
to child nodes according to their ids'''

class DialogueChoice:

    '''this class is used for the choices inside a dialogue node'''

    def __init__(self, text, next_id):
        self.text = text
        self.next_id = next_id

class DialogueNode:

    '''this class is used to define the attributes of a node inside a dialogue'''

    def __init__(self, node_id, text, choices):
        self.node_id = node_id
        self.text = text
        self.choices = choices


class DialogueGraph:

    '''this class will get all the node ids and also show the current node being displayed. the current node will update
    to the next node id once the player makes a choice'''

    def __init__(self, root_node_id, nodes):
        self.nodes_by_id = {}
        self.active_node_id = root_node_id
        for node in nodes:
            node_id = node.node_id
            self.nodes_by_id[node_id] = node

    def make_choice(self, choice_index):
        #when the player makes a choice, the active node will be changed to the next node down the tree
        node = self.nodes_by_id[self.active_node_id]
        self.active_node_id = node.choices[choice_index].next_id

    def current_node(self):
        return self.nodes_by_id[self.active_node_id]

    def __repr__(self):
        return str(self.__dict__)

class DialogueUI:

    '''this class is used to display the dialogue box along with aligning the text inside the dialogue box. it also
    draws a button for each choice. the dialogue box will be updated when the current node changes to the next node'''

    def __init__(self, dialogue_node):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, 20)
        self.sheet = pygame.image.load("../graphics/game_GUI.png").convert_alpha()
        self.dialogue_node = dialogue_node

        self.box = pygame.Surface((16 * 18, 16 * 4))
        self.box.blit(self.sheet, (0, 0), (0, 32, 16 * 18, 16 * 4))
        self.box = pygame.transform.scale(self.box, (64 * 18, 64 * 4))
        self.box_rect = self.box.get_rect(center=(640, 600))
        self.box.set_colorkey("black")

        self.next_dialogue(dialogue_node)

    def next_dialogue(self, dialogue_node):
        self.text = self.font.render(dialogue_node.text, True, "black")
        self.text_rect = self.text.get_rect(topleft=(150, 550))

        #create instances of the choice buttons in the dialogue box
        self.choice_buttons = [Button(None, 640, 660 - 30 * number, choice.text, self.font, BUTTON_HOVER_COLOR, "black", "black")
                               for number, choice in enumerate(dialogue_node.choices)]

    def redraw(self, mouse):
        #redraws the dialogue box when the nodes change
        self.display.blit(self.box, self.box_rect)
        self.display.blit(self.text, self.text_rect)

        for choice in self.choice_buttons:
            choice.change_color(mouse)
            choice.update(self.display)


class Dialogue:

    '''this class combines all the different dialogue classes into one so that they can all work together. it is used to
    run the game loop for the dialogue screen and check for player inputs'''

    def __init__(self, dialogue_graph):
        self.dialogue_graph = dialogue_graph
        self.current_dialogue_node = self.dialogue_graph.current_node()
        self.ui = DialogueUI(self.current_dialogue_node)
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            mouse = pygame.mouse.get_pos()
            self.ui.redraw(mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, choice in enumerate(self.ui.choice_buttons):
                        if choice.check_input(mouse):
                            #check which choice button the player is pressing and update the screen accordingly
                            self.dialogue_graph.make_choice(index)
                            self.current_dialogue_node = self.dialogue_graph.current_node()
                            self.ui.next_dialogue(self.current_dialogue_node)
                            #ends the dialogue if the flag id "STOP" is called
                            if self.current_dialogue_node.node_id == "STOP":
                                self.running = False
            pygame.display.update()


def open_file(file):
    #opens the json file containing the dialogue
    with open(file) as file:
        dialogue = json.load(file)
    return dialogue

def parse_graph_json(graph_json):
    '''this function breaks the json file down into the nodes and their choices. it will return a dialogue graph that
    can be used to get and change the current node'''

    def parse_choice(array):
        #breaks down the choices into its attributes: text and next id
        return DialogueChoice(array[0], array[1])

    def parse_node(node):
        #breaks down the node into its attributes: node id, text and choices
        return DialogueNode(
            node_id=node["id"],
            text=node["text"],
            choices=[parse_choice(choice) for choice in node["choices"]]
        )

    return DialogueGraph(graph_json["root"], [parse_node(node) for node in graph_json["nodes"]])