import sys
import pygame
from pygame.locals import *
import random
from datetime import date
from gameSettings import *
import shelve # shelve is One of the standardLibrary to communicate with directory file.

# Initialization of pygame
pygame.init()

# Setting of clock for game
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((SCREENWIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# Intialize of Fonts variable
BigFont = pygame.font.SysFont("dejavusans", 100)
MedFont = pygame.font.SysFont("dejavusans", 50)
SmallFont = pygame.font.SysFont("dejavusans", 25)

# BackGround images   
BackGround = pygame.image.load("assets/sprites/BackGround.png")
BackGround = pygame.transform.scale(BackGround, (SCREENWIDTH, SCREEN_HEIGHT))

# Players images
BIRDIMAGE = pygame.image.load('assets/sprites/Bird.png')
PLANEIMAGE = pygame.image.load('assets/sprites/Plane01.png')
FISHIMAGE = pygame.image.load('assets/sprites/Fish01.png')

# To save and load User data
UserData = shelve.open("UserData")

#  Variables used in game
Is_Score = True
Ground = pygame.image.load('assets/sprites/base.png').convert_alpha()
Ground = pygame.transform.scale(Ground, (int(SCREENWIDTH), int(168)))
GroundX_Pos = 0

# Player Variables and settings
UserBird = pygame.transform.scale2x(pygame.image.load('assets/sprites/Bird1.png').convert_alpha())
BirdFrames = [UserBird, UserBird, UserBird]
BirdSprites = BirdFrames[PLAYER_INDEX]
BirdRect = BirdSprites.get_rect(center = (100,325))

# Obstecle VAriables and settings
GreenPipe = pygame.image.load('assets/sprites/GreenPipe.png')
GreenPipe = pygame.transform.scale2x(GreenPipe)
#GreenPipe = pygame.transform.scale(GreenPipe, (int(168), int(568)))
GreenPipeList = []
PipeHeight = [400,450,500]

# Events
BirdEvent = pygame.USEREVENT + 1
pygame.time.set_timer(BirdEvent,225)
PipeEvent = pygame.USEREVENT
pygame.time.set_timer(PipeEvent,2500)
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

# audio
WingSound = pygame.mixer.Sound('assets/audio/wing.wav')
HitSound= pygame.mixer.Sound('assets/audio/hit.wav')
PointSound = pygame.mixer.Sound('assets/audio/point.wav')

# Welcome page on the screen 
def WelcomePage():
    TitleText = SmallFont.render("Flappy Animal", True, NAVYBLUE)
    today = date.today()
    todayText =  today.strftime("%A , %B  %D") 
    todayText = SmallFont.render(todayText, True, NAVYBLUE)
    HIGH_SCORE = SmallFont.render("HighestScore",True, NAVYBLUE)
   

    while True:
        screen.fill((105,213,238))
        screen.blit(BackGround, [0, 0])
        screen.blit(todayText, (5, 10))
        screen.blit(TitleText, ((SCREENWIDTH - TitleText.get_width()) / 2, 10))
        screen.blit(HIGH_SCORE, (SCREENWIDTH -  125, 10)) 

        BackGround_rect = BackGround.get_rect()
        screen.blit(BackGround, (BackGround_rect.width, 0))

        TxtLine1 = SmallFont.render("Space key to start as Guest User", True, NAVYBLUE)
        TxtLine2 = SmallFont.render("Enter or Return key to choose settings ", True, NAVYBLUE)
        TxtLine3 = SmallFont.render("Use Space key to move", True, NAVYBLUE)
        tl1_rct = TxtLine1.get_rect(midbottom = (SCREENWIDTH / 2, SCREENHEIGHT / 2))
        tl2_rct = TxtLine2.get_rect(midbottom = (SCREENWIDTH / 2, SCREENHEIGHT * 2.5 / 4))
        tl3_rct = TxtLine3.get_rect(midbottom = (SCREENWIDTH / 2, SCREENHEIGHT * 3 / 4))
        screen.blit(TxtLine1,  tl1_rct)
        screen.blit(TxtLine2, tl2_rct)
        screen.blit(TxtLine3,  tl3_rct)

        pygame.display.flip()
        KeyWait()
def GameMenu():
    TitleText = SmallFont.render("The Flappy Animal Game", True, MEDUIMBLUE)
    
    global NEWUSER

    # Active - deactive upon selection
    UNameActive = False
    BirdActive = False
    PlaneActive = False
    FishActive = False
    AstrntActive = False
    
  
    UserChoicePrompt = SmallFont.render("Select your choices", True, MEDUIMBLUE)
   
    StartGame = SmallFont.render("Start Game", True, WHITE)

    while True:
        screen.fill((105,213,238))
        screen.blit(TitleText, ((SCREENWIDTH - TitleText.get_width()) / 2, 0))

        # UserName  TextBox
        UserNameText = SmallFont.render(NEWUSER, True, WHITE)
        UNTextBorder = pygame.Rect(((SCREENWIDTH - UserNameText.get_width()) / 2) - 10, SCREENHEIGHT * .20, UserNameText.get_width() + 10, 50)
        screen.blit(UserNameText, ((SCREENWIDTH - UserNameText.get_width()) / 2, SCREENHEIGHT * .20))

        # Border for User Iamges
        BirdBorder = pygame.Rect((SCREENWIDTH * .250) - 4, (SCREENHEIGHT * .45) - 4, BIRDIMAGE.get_width() + 8, BIRDIMAGE.get_height() + 8)
        PlaneBorder = pygame.Rect(((SCREENWIDTH - PLANEIMAGE.get_width()) * .462) - 4, (SCREENHEIGHT * .45) - 4, PLANEIMAGE.get_width() + 8, PLANEIMAGE.get_height() + 8)
        FishBorder = pygame.Rect(((SCREENWIDTH - FISHIMAGE.get_width()) * .650) - 4, (SCREENHEIGHT * .45) - 4, FISHIMAGE.get_width() + 8, FISHIMAGE.get_height() + 8)
        AstrntBorder = pygame.Rect(((SCREENWIDTH - ASTRNTIMAGE.get_width()) * .840) - 4, (SCREENHEIGHT * .45) - 4, ASTRNTIMAGE.get_width() + 8, ASTRNTIMAGE.get_height() + 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # KeyBoard - Mouse Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if UNTextBorder.collidepoint(event.pos):
                    UNameActive = True
                elif BirdBorder.collidepoint(event.pos):
                    BirdActive = True
                elif PlaneBorder.collidepoint(event.pos):
                    PlaneActive = True
                elif FishBorder.collidepoint(event.pos):
                    FishActive = True
                elif AstrntBorder.collidepoint(event.pos):
                    AstrntActive = True
                else:
                    UNameActive = False
                    BirdActive = False
                    PlaneActive = False
                    FishActive = False
                    AstrntActive = False

            if event.type == pygame.KEYDOWN:
                if UNameActive:
                    if event.key == pygame.K_BACKSPACE:
                        NEWUSER = NEWUSER[:-1]
                    else:
                        NEWUSER += event.unicode

        # UserName TextBox Click Event
        if UNameActive:
            pygame.draw.rect(screen, WHITE, UNTextBorder, 2)
            USERNAMEPrompt = SmallFont.render("Enter UserName here", True, WHITE)
        else:
            pygame.draw.rect(screen, MEDUIMBLUE, UNTextBorder, 2)
            USERNAMEPrompt = SmallFont.render("Enter User-Name here", True, MEDUIMBLUE)

        if BirdActive:
            PlaneActive = False
            FishActive = False
            AstrntActive = False
            pygame.draw.rect(screen, WHITE, BirdBorder, 2)
            UserChoice = "Bird"
        else:
            pygame.draw.rect(screen, NAVYBLUE, BirdBorder, 2)

        if PlaneActive:
            BirdActive = False
            FishActive = False
            AstrntActive = False
            pygame.draw.rect(screen, WHITE, PlaneBorder, 2)
            UserChoice = "Plane"
        else:
            pygame.draw.rect(screen, NAVYBLUE, PlaneBorder, 2)

        if FishActive:
            BirdActive = False
            PlaneActive = False
            AstrntActive = False
            pygame.draw.rect(screen, WHITE, FishBorder, 2)
            UserChoice = "Fish"
        else:
            pygame.draw.rect(screen, NAVYBLUE, FishBorder, 2) 
        
        if AstrntActive:
            BirdActive = False
            PlaneActive = False
            FishActive
            pygame.draw.rect(screen, WHITE, AstrntBorder, 2)
            UserChoice = "Astronaut"
        else:
            pygame.draw.rect(screen, NAVYBLUE, AstrntBorder, 2) 


        screen.blit(USERNAMEPrompt, ((SCREENWIDTH - USERNAMEPrompt.get_width()) / 2, (SCREENHEIGHT * .05) + UserNameText.get_height()))
        screen.blit(UserChoicePrompt, ((SCREENWIDTH - UserChoicePrompt.get_width()) / 2, SCREENHEIGHT * .35))

        # User Selection
        UserText = MedFont.render("Users:", True, WHITE)
        screen.blit(UserText, (SCREENWIDTH * .075, SCREENHEIGHT * .45))
        screen.blit(BIRDIMAGE, (SCREENWIDTH * .250, SCREENHEIGHT * .45))
        screen.blit(PLANEIMAGE, (SCREENWIDTH * .425, SCREENHEIGHT * .45))
        screen.blit(FISHIMAGE, (SCREENWIDTH * .600, SCREENHEIGHT * .45))
        screen.blit(ASTRNTIMAGE, (SCREENWIDTH * .775, SCREENHEIGHT * .45))
        submitButtton = Button((SCREENWIDTH / 2) - (StartGame.get_width() / 2) - 5, SCREENHEIGHT * .9,StartGame.get_width() + 10, StartGame.get_height(), MEDUIMBLUE, NAVYBLUE)

        screen.blit(StartGame, ((SCREENWIDTH / 2) - (StartGame.get_width() / 2), int(SCREENHEIGHT * .9)))

        global USERNAME
        if submitButtton:
            if NEWUSER != "":
                USERNAME = NEWUSER
                UserData['USERNAME'] = USERNAME
            else:
                USERNAME = 'GuestUser'
                UserData['USERNAME'] = USERNAME

            UserData['HIGH_SCORE'] = UserChoice
            UserData.close()
            SuccessScreen(USERNAME, UserChoice)

        pygame.display.update()
        clock.tick(FPS / 4)

       
# This is loop for Main Game
while True:
    WelcomePage()
