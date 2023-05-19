import pygame
import random

# constants
FPS = 144
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# define fonts
font = pygame.font.SysFont("arialblack",50)
text_font = pygame.font.SysFont("arialblack",25)

# print text to screen
def draw_text(text,font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# set cpus based on desired number of cpus
def set_cpu(cpu_num):
    player_num = 4 - cpu_num
    for player in Player.players:
        if player_num > 0:
            player.cpu = False
        else:
            player.cpu = True
        player_num -= 1

# player class
class Player:
    players = []
    def __init__(self,CPU,color,name):
        self.cpu = CPU
        self.color = color
        self.name = name
        self.cards = []
        self.total = 0
        Player.players.append(self)

    def add_card(self,value):
        self.cards.append(value)

    def select(self,deck,pos):
        self.add_card(deck.get_num(pos))
        deck.remove_card(pos)

    def get_total(self):
        for num in self.cards:
            self.total += num


# select arrow class
class Selector:
    def __init__(self,color,y_value,x_center,width,height,running,value):
        self.value = value
        self.color = color
        self.posY = y_value
        self.x_center = x_center
        self.radius = width / 2
        self.height = height
        # takes the x center - or + half the width to get x points and heigth to get y points
        self.points = [(x_center - self.radius,self.posY),(x_center + self.radius,self.posY),(x_center,self.posY+self.height)]
        self.running = running

    # sets the points and displays the polygon
    def display(self):
        self.points = [(self.x_center - self.radius,self.posY),(self.x_center + self.radius,self.posY),(self.x_center,self.posY+self.height)]
        pygame.draw.polygon(screen,self.color,self.points)

    # gets input and changes the x value by 90, and increments the value
    def input(self,deck,player):
        keys = pygame.key.get_pressed()
        # delay between inputs
        pygame.time.delay(90)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # if at max card wont allow movment right
            if self.value != len(deck.cards)-1:
                self.x_center += 90
                self.value += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # if at position 1, wont allow left movement
            if self.value != 0:
                self.x_center -= 90
                self.value -= 1
        if keys[pygame.K_RETURN]:
            self.select_card(deck,self.value,player)
            self.running = False

    # select a random card for the player
    def cpu_select(self,deck,player):
        selection = random.randint(0,len(deck.cards)-1)
        self.x_center += selection * 90
        self.select_card(deck,selection,player)
        self.running = False

    def select_card(self,deck,value,player):
        deck.display_card(value,300)
        player.select(deck,value)

# deck of cards
class Cards:
    def __init__(self):
        self.cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.length = len(self.cards)

    # input a numerical value and retrun the position of the value in the list
    def return_pos(self,num):
        return self.cards.index(num)

    # input a position and get the numerical value
    def get_num(self,pos):
        return self.cards[pos-1]

    # shuffles the deck
    def shuffle_deck(self):
        random.shuffle(self.cards)
        
    # displays all the blank cards
    def display_blank_deck(self,card_y):
        x_val = 50
        for card in self.cards:
            pygame.draw.rect(screen,"pink",(x_val,card_y,65,100))
            pygame.draw.circle(screen,"yellow",(x_val+32.5,card_y+50),25)
            x_val += 90

    # display singular card
    def display_card(self,list_pos,card_y):
        if self.get_num(list_pos) < 10:
            pad = 14
        else:
            pad = 0
        x_val = (90* int(list_pos)) + 50
        pygame.draw.rect(screen,"pink",(x_val,card_y,65,100))
        draw_text(str(self.get_num(list_pos)),font,"green",x_val+pad,card_y+10)

    def remove_card(self,pos):
        self.cards.remove(self.get_num(pos))

    @staticmethod
    def print_card(value,x,y):
        if value < 10:
            pad = 14
        else:
            pad = 0
        pygame.draw.rect(screen,"pink",(x,y,65,100))
        draw_text(str(value),font,"green",x+pad,y+10)

deck = Cards()
p1 = Player(False,"red","Player 1")
p2 = Player(False,"blue","Player 2")
p3 = Player(False,"green","Player 3")
p4 = Player(False,"yellow","Player 4")

# get the number of cpus with arrow keys
def get_cpu_num():
    running = True
    cpu_num = 0
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # RENDER YOUR GAME HERE
        draw_text("CPUS: "+str(cpu_num),font,"black",550,310)

        keys = pygame.key.get_pressed()
        # delay between inputs
        pygame.time.delay(90)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if cpu_num != 4:
                cpu_num += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if cpu_num != 0:
                cpu_num -= 1
        if keys[pygame.K_RETURN]:
            set_cpu(cpu_num)
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

# 1 player's turn of the game
def card_game(player,deck):
    pointer = Selector(player.color,220,82.5,40,50,True,0)
    deck.shuffle_deck()

    while pointer.running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pointer.running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # RENDER YOUR GAME HERE
        deck.display_blank_deck(300)
        draw_text(player.name + "'s Turn",font, player.color,440,100)
        if player.cpu == False:
            pointer.input(deck,player)
        else:
            pointer.cpu_select(deck,player)
            pygame.time.delay(1000)

        pointer.display()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60
    pygame.time.delay(1500)

# winner / final screen
def show_cards():
    running = True
    for player in Player.players:
        player.get_total()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # RENDER YOUR GAME HERE
        
        y_pos = 100
        winner_total = 0
        winner = p1

        for player in Player.players:
            x_pos = 200
            draw_text(str(player.name)+": ",text_font,player.color,x_pos,y_pos)
            x_pos += 150
            for i in player.cards:
                Cards.print_card(i,x_pos,y_pos)
                x_pos += 90
            draw_text("Total: "+str(player.total),text_font,player.color,x_pos,y_pos)
            y_pos += 150

            if player.total > winner_total:
                winner_total = player.total
                winner = player

        draw_text("Winner: "+winner.name,text_font,winner.color,850,360)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

def main():
    get_cpu_num()
    for x in range(3):
        for player in Player.players:
            card_game(player,deck)
    show_cards()

main()
pygame.quit()