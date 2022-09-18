"""
This game is based on an existing framework that I found. It turns out making a game in pygame is quite difficult.
I had only just started learning about OOP, functions, classes, and different modules, but I was determined
to make a game using pygame. With the time I had I realised I couldn't make my own from scratch but I knew I could
learn a lot by making my own improvements and researching how to implement them.
I noted down the things about the game I thought needed improving, and I improved them (well, most of them).
The game looked rather dull so, I made some cosmetic changes such as changing the background, layout and fonts.
I made the game more immersive by adding sound effects for whether you win or lose.
I created different functions for winning and losing. I played around with different modules to see what
directions I could take a simple game like hangman. The most obvious improvement I made using a module was generating
a truly random word so I would be able to play the game too. The other improvement was displaying the word and its
definition after the game had finished whether you won  or lost. Displaying a paragraph in pygame proved to be quite
a challenge, Instead of a simple '\n' it ended up being an extra file with 46 lines of code and also the game only runs
properly if you run it through that file (fatboy.py). Other than that, the only other thing I wanted to do was make
a 'play again' button but I wasn't able to implement that unfortunately.
"""

import pygame
import math
import randomword
from PyDictionary import PyDictionary
import os


# setup display and sounds
pygame.init()
WIDTH, HEIGHT = 1100, 600 #constants in capitals
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Not a childrens game")
pygame.mixer.init()


# sounds
poof = pygame.mixer.Sound(os.path.join('s/' + 'fart' + '.wav'))
woo = pygame.mixer.Sound(os.path.join('s/' + 'applause' + '.wav'))

# fonts
LETTER_FONT = pygame.font.SysFont('arial', 25)
WORD_FONT = pygame.font.SysFont('arial', 45)
TITLE_FONT = pygame.font.SysFont('constantia', 55)

# load images
background = pygame.image.load('img/' + 'town' + '.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
images = []
for i in range(7):
    image = pygame.image.load('img/' + 'hangman' + str(i) + '.png')  # import images
    images.append(image)

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 450
A = 65 # A is represented by 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])


# game variables
dictionary = PyDictionary()
hangman_status = 0
wordz = randomword.get_random_word()
worp = wordz.upper()
meaning = (dictionary.meaning(worp))
meanings = str(meaning)
guessed = [" "]

# colours - mix the colours with red + green + blue (0-255)
WHITE = (255, 255, 255)
LILAC = (120, 110, 130)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# frames per second
FPS = 60
clock = pygame.time.Clock()
run = True



def draw():
    win.blit(background, (0, 0))
    # draw title
    text = TITLE_FONT.render("THE GALLOWS POLE", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in worp:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400,250))
    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x- text.get_width()/2, y -text.get_height()/2))

    win.blit(images[hangman_status], (125, 150))
    pygame.display.update()

# If the player loses
def not_yet():
    pygame.mixer.Sound.play(poof)
    pygame.time.delay(2000)
    win.fill(WHITE)
    text = LETTER_FONT.render("You almost had it!... ", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2)) # (400, 300))
    pygame.display.update()
    pygame.time.delay(4000)

# If the player wins
def you_won():
    pygame.mixer.Sound.play(woo)
    pygame.time.delay(4000)
    win.fill(WHITE)
    text = LETTER_FONT.render("You saved me!", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2)) # (400, 300))
    pygame.display.update()
    pygame.time.delay(4000)


# setup main game loop
while run:
    clock.tick(FPS)

    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x,m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x)**2 + (y -m_y)**2)
                    if dis < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in worp:
                            hangman_status += 1

    draw()

    won = True
    for letter in worp:
        if letter not in guessed:
            won = False
            break

    if won:
        you_won()
        break

    if hangman_status == 6:
        not_yet()
        break

pygame.quit()