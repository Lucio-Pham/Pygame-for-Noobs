#memory puzzle
#From IYOCGWP

import pygame, sys
import random 
from pygame.locals import*

#thiet lap cac constant variable - cac bien co dinh 
FPS= 30 #khung hinh xuat hien tren 1 giay 
WINDOWWIDTH= 640 #chieu rong man hinh 
WINDOWHEIGHT= 480 #chieu cao man hinh 
REVEALSPEED= 8 #toc do dich chuyen cua box, dong va mo
BOXSIZE= 40 #kich co cua moi box, box hinh vuong. 
GAPSIZE= 10 #kich co khoang trong giua cac box
BOARDWIDTH= 10 #so luong cot co trong bang
BOARDHEIGHT= 7 #so luong dong co trong bang 

assert (BOARDHEIGHT*BOARDWIDTH) %2 ==0, 'Board needs to have an even number of boxes for pairs of matches.'
#dung de thong bao cho lap trinh vien biet neu moi board dat khong dung kich thuoc

#cong thuc tinh toan vi tri dat cac box. luon tra ve so chan. vi cac box di theo cap. 
XMARGIN = int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2) 
YMARGIN = int((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)

# set up mau R     G     B 
GRAY     = (100,  100,  100)
NAVYBLUE = ( 60,   60,  100)
WHITE    = (255,  255,  255) 
RED      = (255,    0,    0) 
GREEN    = (  0,  255,    0) 
BLUE     = (  0,    0,  255) 
YELLOW   = (255,  255,    0) 
ORANGE   = (255,  128,    0) 
PURPLE   = (255,    0,  255) 
CYAN     = (  0,  255,  255) 

BGCOLOR  = NAVYBLUE
LIGHTBGCOLOR = GRAY 
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

#su dung constant variable thay vi dung string de tranh nham lan cu phap. 
DONUT   = 'donut'
SQUARE  = 'square' 
DIAMOND = 'diamond'
LINES   = 'lines'
OVAL    = 'oval' 

#Luu giu mau sac va hinh dang vao 2 tuple. se duoc dung de tron voi nhau. 
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN) 
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL) 
#kiem tra xem mau va hinh dang box co phu hop voi kich co cua board khong
assert len(ALLCOLORS)*len(ALLSHAPES) *2 >= BOARDHEIGHT*BOARDWIDTH, 'Board is too big for the number of shapes/colors defined'

def main(): 
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 #bien dung de luu tru gia tri toa do x cua con tro chuot 
    mousey = 0 #bien dung de luu tru gia tri toa do y cua con tro chuot 
    pygame.display.set_caption('Memory Puzzle') 

    mainBoard = getRandomizedBoard() #tra ve cau truc du lieu the hien cac icon trong board. randomize
    revealedBoxes = generateRevealedBoxesData(False) #tra ve gia tri False: box cover. tra ve True: box unveil
    #ham nay tra ve cau truc du lieu the hien box nao duoc cover

    firstSelection = None #bien so luu tru gia tri toa do (x, y) cua box dau tien click vao

    DISPLAYSURF.fill(BGCOLOR) 
    startGameAnimation(mainBoard) #ham khoi dau choi game 

    while True: #vong lap game chinh 
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) #ve mau nen cho man hinh 
        drawBoard(mainBoard, revealedBoxes) 

        for event in pygame.event.get(): 
            if event.type==QUIT or (event.type == KEYUP and event.key ==K_ESCAPE): 
                pygame.quit()
                sys.exit()
            #vong lap else if ghi nhan hoat dong cua tro chuot 
            elif event.type ==MOUSEMOTION: 
                mousex, mousey = event.pos 
            elif event.type ==MOUSEBUTTONUP: 
                mousex, mousey = event.pos 
                mouseClicked =True 

        boxx, boxy = getBoxAtPixel (mousex, mousey) #kiem tra xem tro chuot co click vao box hay khong
        if boxx != None and boxy != None: 
            #neu dung thi tra ve gia tri boxx, boxy la vi tri cua box 
            if not revealedBoxes[boxx][boxy]: #kiem tra xem box co duoc cover hay khong 
                drawHighlightBox(boxx, boxy) #ve duong vien highlight quanh box khi co tro chuot luot qua
            if not revealedBoxes[boxx][boxy] and mouseClicked: 
                revealedBoxesAnimation (mainBoard, [(boxx, boxy)]) 
                revealedBoxes[boxx, boxy] = True #box da duoc mo. neu ko co dong nay thi khi tro chuot click vao, box se duoc mo ra sau do dong lai ngay lap tuc

                if firstSelection == None: #True neu box hien tai la box thu nhat duoc mo trong 1 cap box
                    firstSelection = (boxx, boxy) 
                else: #neu dieu kien tren ko dung, box hien tai click vao la box thu hai. 
                    #code nay se kiem tra xem box hien tai co match voi box dau tien hay ko
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1]) 
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy) 

                    if icon1shape != icon2shape or icon1color != icon2color: 
                        #kiem tra xem 2 icon box co giong nhau hay khong
                        pygame.time.wait(1000) #wait for 1s when uncover box
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False #update game sau khi player chon sai, box se duoc lat up lai nhu cu
                    elif hasWon(revealedBoxes): #kiem tra neu tat ca cac cap deu duoc tim thay
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000) 

                        #reset lai game board
                        mainBoard = get getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False) 

                        #lat tat ca cac box dong thoi trong vong 1s de nguoi choi co duoc goi y
                        drawBoard(mainBoard, revealedBoxes) 
                        pygame.display.update()
                        pygame.time.wait(1000) 

                        #Man khoi dong game animation 
                        startGameAnimation(mainBoard) 
                    firstSelection = None #reset lai first selection 
                    
         pygame.display.update() #se tro den doi tuong DISPLAYSURF de ve lai man hinh
         FPSCLOCK.tick(FPS) #so khung hinh chay 1s 

def generateRevealedBoxesData(val): #Ham nay tao ra 1 list cac gia tri boolean True hoac False
    revealedBoxes = []
    for i in range (BOARDWIDTH): 
        revealedBoxes.append([val]*BOARDHEIGHT) #tao ra cau truc du lieu theo hang doc(chieu cao hop) dang [x][y]
    return revealedBoxes

#creating board data structure
#Buoc 1: lay tat ca cac to hop co the co
def getRandomizedBoard(): 
    #cac gia tri mau sac va hinh dang duoc tron lan va lay het
    icons=[]
    for color in ALLCOLORS: 
        for shape in ALLSHAPES: 
            icons.append((shape, color)) #tao ra 1 list cac tuple la cac to hop hinh khoi, mau sac khac nhau
    #Buoc 2: tron lan cac to hop tren bang ham shuffle
    random.shuffle(icons) 
    numIconsUsed = int(BOARDWIDTH*BOARDHEIGHT/2) #tinh toan ra bao nhieu icon la can thiet
    #vi se co nhieu su ket hop hon kich thuoc man hinh 
    icons = icons[:numIconsUsed]*2 #tao ra 2 list icons giong nhau
    random.shuffle(icons) #tiep tuc tron lan cac icons tu list icon moi tao

    #Buoc 3: xep cac icons vao board
    #Tao ra mot board roi dat cac icon random vao 
    board = []
    for x in range (BOARDWIDTH): 
        column = []
        #them icon vao tung column, xong do xoa icon moi them o trong list icons. vong lap tiep tuc cho toi khi day bang. 
        #viec del icon moi them vao se tranh icon bi trung lap khi them cac icon vao bang
        for y in range(BOARDHEIGHT): 
            column.append(icons[0]) 
            del icons[0] 
        board.append(column) #them cac icon o tron column vao bang (board) 
    return board 

    #phan chia 1 list ra cac list cua list 
def splitIntoGroupsOf(groupSize, theList): 
    #chia list thanh cac list cua list 
    result = []
    for i in range(0, len(theList, groupSize)):
        result.append(theList[i:i+groupSize]) 
    return result 

def leftTopCoordsOfBox (boxx, boxy): 
    #ham tra ve gia tri toa do 
    # convert cac board coordinate thanh cac gia tri pixel
    left = boxx*(BOXSIZE+ GAPSIZE) + XMARGIN
    top = boxy*(BOXSIZE + GAPSIZE) +YMARGIN
    return (left, top) 

#Ham chuyen doi tu pixel coordinate sang box coordinate. 
#Tro chuot di chuyen tren man hinh qua vi tri cac box, ham nay se xac dinh vi tri tro chuot va doi chieu vi tri cac box
def getBoxAtPixel(x,y): 
    for boxx in range (BOARDWIDTH): 
        for boxy in range (BOARDHEIGHT): 
            left, top = leftTopCoordsOfBox(boxx, boxy) 
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE) 
            if boxRect.collidepoint(x,y): #kiem tra vi tri (x,y) co khop hay ko
                return (boxx, boxy)       #Tra ve True neu (x,y) nam trung voi box Rect 
                                          #neu ko co don vi nao trung thi tra ve (None, None) 

#Ham ve icon voi hinh dang, mau sac. vi tri cu the
def drawIcon (shape, color, boxx, boxy): 
    quarter = int(BOXSIZE*0.25) #syntactic sugar
    half    = int(BOXSIZE*0.5) #syntactic sugar 

    left, top = leftTopCoordsOfBox(boxx, boxy) #lay gia tri pixel tu board coord

    #Ham ve hinh tung icon 
    if shape == DONUT: 
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top +half), - 5) #vong tron thu nhat cua hinh donut 
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left +half, top + half), quarter- 5) #vong tron thu hai cua hinh donut

    elif shape == SQUARE: 
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND: 
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE -1 ),(left, top + half)))
    elif shape == LINES: 
        for i in range (0, BOXSIZE, 4): 
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left +i, top)) 
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i)) 
    elif shape == OVAL: 
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

def getShapeAndColor(board, boxx, boxy): 
    #gia tri hinh dang la cac so x, y duoc luu duoi dang board[x][y][0]
    #gia tri mau sac duoc luu trong cac toa do board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage): #ve duong vien hop 
    #Ve cac box duoc che lai/mo ra. "boxes" la mot list 2 items, voi x va y danh dau box
    for box in boxes: 
        left, top = leftTopCoordsOfBox(box[0], box[1]) 
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1]) 
        drawIcon(shape, color, box[0], box[1]) #goi ham ve icon 
        if coverage > 0: #chi ve cover neu co vien 
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS) 

#Xu ly cac hanh dong lat mo va dong box
def revealedBoxesAnimation(board, boxesToReveal): 
    #Hanh dong lat mo o
    for coverage in range (BOXSIZE, (-REVEALSPEED)-1, -REVEALSPEED): 
        drawBoxCovers(board, boxesToReveal, coverage) #lat mo cac o tu vi tri cuoi 
def coverBoxesAnimation(board, boardToCover): 
    #Hanh dong dong o 
    for coverage in range (0, BOXSIZE + REVEALSPEED, REVEALSPEED): #hanh dong dong o tu vi tri dau
        drawBoxCovers(board, boxesToCover, coverage)
def drawBoard(board, revealed): 
    #Ve tat ca cac box dang duoc cover hoac cac box da lat mo
    for boxx in range (BOARDWIDTH): 
        for boxy in range (BOARDHEIGHT): 
            left, top = leftTopCoordsOfBox(boxx, boxy) 
            if not revealed[boxx][boxy]: 
                #Ve duong vien box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else: 
                #Ve nhung icon da duoc lat mo 
                shape, color = getShapeAndColor(board, boxx, boxy) 
                drawIcon(shape, color, boxx, boxy) 
#Ve duong vien highlight cho moi box, mau blue
def drawHighlightBox(boxx, boxy): 
    left, top = leftTopCoordsOfBox(boxx, boxy) 
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top -5, BOXSIZE + 10, BOXSIZE + 10), 4) 

def startGameAnimation(board): 
    #Hanh dong lat mo tung box trong game. 8 box 1 lan lat mo
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range (BOARDWIDTH): 
        for y in range (BOARDHEIGHT): 
            boxes.append((x,y))
    random.shuffle(boxes) 
    boxGroups = splitIntoGroupsOf(8, boxes) 

    drawBoard(board, coveredBoxes) 
    for boxGroup in boxGroups: 
        revealedBoxesAnimation(board, boxGroup) 
        coverBoxesAnimation(board, boxGroup) 

def gameWonAnimation(board): 
    #Hanh dong xac dinh nguoi chien thang
    coveredBoxes = generateRevealedBoxesData(True) 
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range (13): 
        color1, color2 = color2, color1 #swap color
        DISPLAYSURF.fill(color1) 
        drawBoard(board, coveredBoxes) 
        pygame.display.update()
        pygame.time.wait(300) 

def hasWon(revealedBoxes): 
    #Hanh dong thong bao cho nguoi choi biet ho da thang. 
    #Tra ve True neu tat ca box deu duoc lat mo. neu khong la False
    for i in revealedBoxes: 
        if False in i: #kiem tra cac cap box mo ra co trung nhau khong. neu co du chi 1 cap khong giong nhau, tra ve false
            return False
        return True
if __name__ == '__main__': 
    main()






