<<<<<<< HEAD:upset_recovery.py
def pfd():
    import pygame
    pygame.init()
    import os
    import time as timer
    recordtime = str(timer.ctime()).replace(':', '_')
    dirname = str(username + recordtime)
    try:
        os.mkdir(dirname)
    except Exception:
        pass
    finally:
        os.chdir(str(os.getcwd())+'/'+dirname)

    pygame.display.init()
    pygame.joystick.init()
    import matplotlib.pyplot as plt
    import math
    import table_creator
    import random
    import numpy as np

    # SETTINGS
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    W = 1200
    H = 800
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption('Vyvod Iz SPP')
    # pygame.display.set_icon(pygame.image.load())
    clock = pygame.time.Clock()
    FPS = 60
    a = True
    rounds = 5
    blindpitch = 0.05
    blindroll = 0.05
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (50, 50, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BROWN = (200, 155, 40)
    xstart = W // 2
    ystart = H // 2
    xstart1 = 150  # center of a brown surfase
    ystart1 = 180  # center of a brown surfase
    storona = 1200
    interval = 25
    shirina = 22
    speedroll = 0.3
    speedpitch = 10
    roll = random.random() * random.randint(-2, 2)
    pitch = random.randint(-200, +200)
    time = 10
    shag = int(FPS * rounds)
    surf = pygame.Surface((300, 360))
    surf.fill(BROWN)
    sc.blit(surf, (xstart - 150, ystart - 180))
    pygame.display.update()
    rolllist=[]
    pitchlist=[]
    yrolllist = []
    ypitchlist = []
    expnum = 0

    while a == True:

        for i in range(pygame.joystick.get_count()):

            if pygame.joystick.Joystick(i).get_axis(0) > -blindroll and pygame.joystick.Joystick(i).get_axis(0) < blindroll:
                speedroll = 0
            else:
                speedroll = pygame.joystick.Joystick(i).get_axis(0)

            speedroll1 = speedroll * 0.75
            roll += speedroll1 / 17
            speedpitch = pygame.joystick.Joystick(i).get_axis(1)


            if pitch > -23 and pitch<23:
                speedpitch1=speedpitch*1
            if pitch > -11 and pitch<11:
                speedpitch1=speedpitch*1.2
            elif pitch > -35 and pitch<35:
                speedpitch1 = 0.88 * pygame.joystick.Joystick(i).get_axis(1)
            else:
                speedpitch1=speedpitch*0.75

            if pygame.joystick.Joystick(i).get_axis(1) > -blindpitch and pygame.joystick.Joystick(i).get_axis(
                    1) < blindpitch:
                speedpitch = 0
            pitch += speedpitch1 * 4
            yrolllist.append(speedroll)
            ypitchlist.append(speedpitch)
            rolllist.append(roll*55)
            pitchlist.append(pitch/5)

        if len(ypitchlist) == shag:
            expnum += 1
            table_creator.tables_to_exc(ypitchlist, f'Pitch_table{expnum}')
            table_creator.tables_to_exc(yrolllist, f'Roll_table{expnum}')

            def Inputplot(expnum):

                xplot = np.linspace(0.0, FPS * rounds, shag)

                ypitchplot = ypitchlist
                yrollplot = yrolllist
                plt.figure(figsize=(8, 8))  # GRAFIKI START
                plt.subplot(211)
                plt.axis([0, FPS * rounds, -1.2, 1.2])
                plt.title('Pitch movement                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Amplitude', color='gray')
                plt.plot(xplot, ypitchplot)
                plt.grid()
                plt.subplot(212)
                plt.axis([0, FPS * rounds, -1.2, 1.2])
                plt.title('Roll movement                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Amplitude', color='gray')
                plt.plot(xplot, yrollplot)
                plt.grid()
               # plt.show()
                plt.savefig(str(recordtime)+'Input_plot'+str(expnum)+'.pdf',format='pdf')
                plt.close()
                pygame.time.delay(100)
                roll = random.random() * random.randint(-1, 1)
                pitch = random.randint(-50, +50)
                # if roll in np.arange(-0.2,0.2) ==True or pitch in np.arange(-1.0,1.0)==True:
                if (roll < 0.2 == True and roll > -0.2 == True) or (pitch < 30 == True and roll > -30 == True):
                    roll = random.random() * random.randint(-1, 1)
                    pitch = random.randint(-50, +50)
            Inputplot(expnum)
            def Attitudeplot(expnum):
              #  expnum += 1
                xplot = np.linspace(0.0, FPS * rounds, shag)

                rollplot=rolllist
                pitchplot=pitchlist
                plt.figure(figsize=(8, 8))  # GRAFIKI START
                plt.subplot(211)
                plt.axis([0, FPS * rounds, -90, 90])
                plt.title('Pitch attitude                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Degrees', color='gray')
                plt.plot(xplot, pitchplot)
                plt.grid()
                plt.subplot(212)
                plt.axis([0, FPS * rounds, -130, 130])
                plt.title('Roll attitude                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Degrees', color='gray')
                plt.plot(xplot, rollplot)
                plt.grid()
                plt.savefig(str(recordtime)+'Attitude_plot' + str(expnum) + '.pdf', format='pdf')
                plt.close()
                #plt.show()


            Attitudeplot(expnum)



        if len(ypitchlist) > FPS * rounds:
            print(ypitchlist)
            pitchlist = []
            rolllist = []
            ypitchlist = []
            yrolllist = []


            plusminus=random.randint(-1,1)
            if plusminus<=0:
                pitch = random.randint(-150, -60)
            else:
                pitch = random.randint(+60, +150)
            minusplus= random.randint(-1,1)
            if minusplus<=0:
                roll=random.random()*-1.7
            else:
                roll=random.random()*1.7

        for event in pygame.event.get():



            if event.type == pygame.KEYDOWN:
                # Other buttons

                if pygame.key.get_pressed()[pygame.K_RALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.display.set_mode((W, H), pygame.FULLSCREEN)
                    if pygame.key.get_pressed()[pygame.K_RALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                        pygame.display.set_mode((W, H))
                if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.display.set_mode((W, H), pygame.FULLSCREEN)
                    if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                        pygame.display.set_mode((W, H))
                #Упарвление РУС с клавы(данные в таблицу не записыаются)
                pygame.key.set_repeat(100, 50)
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    roll -= speedroll
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    roll += speedroll
                if pygame.key.get_pressed()[pygame.K_UP]:
                    pitch -= speedpitch * 10
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    pitch += speedpitch * 10
                if pygame.key.get_pressed()[pygame.K_r]:
                    pygame.time.delay(500)
                    roll = random.random() * random.randint(-2, 2)
                    pitch = random.randint(-200, +200)

                    if (math.sin(roll) < 0.9  and math.sin(roll) > -0.9) or (pitch < 50 == True and roll > -50 == True):
                        while (math.cos(roll) < 0.9 and math.cos(roll) > -0.9) or (
                                pitch < 50 and roll > -50):
                            roll = random.random() * random.randint(-2, 2)
                            pitch = random.randint(-200, +200)





        # Отрисовка

        sc.fill(BLACK)
        sc.blit(surf, (xstart - 150, ystart - 180))

        surf.fill(BROWN)
        pygame.draw.polygon(surf, BLUE, (
            (xstart1, ystart1 + pitch * math.cos(roll)),
            (xstart1 + storona * math.cos(roll), pitch * math.cos(roll) + ystart1 - storona * math.sin(roll)),
            (xstart1 + ((2 * (storona ** 2)) ** (1 / 2)) * math.cos(roll + 0.785398),
             pitch * math.cos(roll) + ystart1 - ((2 * (storona ** 2)) ** (1 / 2)) * math.sin(roll + 0.785398)),
            (xstart1 - storona * math.sin(roll), pitch * math.cos(roll) + ystart1 - storona * math.cos(roll)))
                            , 0)
        pygame.draw.polygon(surf, BLUE, (
            (xstart1, ystart1 + pitch * math.cos(roll)),
            (xstart1 - storona * math.cos(roll), pitch * math.cos(roll) + ystart1 + storona * math.sin(roll)),
            (xstart1 - ((2 * (storona ** 2)) ** (1 / 2)) * math.sin(roll + 0.785398),
             pitch * math.cos(roll) + ystart1 - ((2 * (storona ** 2)) ** (1 / 2)) * math.cos(roll + 0.785398)),
            (xstart1 - storona * math.sin(roll), pitch * math.cos(roll) + ystart1 - storona * math.cos(roll)))
                            , 0)
        # RISKI NIZJE

        i = -8
        while i <= 8:
            y = i * interval
            if i % 2 == 0:
                x1 = 2 * shirina
            else:
                x1 = shirina
            pygame.draw.line(surf, WHITE,
                             (xstart1 - y * math.sin(roll), ystart1 + pitch * math.cos(roll) - y * math.cos(roll)),
                             (xstart1 + ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.cos(math.atan(y / x1) + roll),
                              pitch * math.cos(roll) + ystart1 - ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.sin(
                                  roll + math.atan(y / x1))),
                             3)
            pygame.draw.line(surf, WHITE,
                             (xstart1 - y * math.sin(roll), ystart1 + pitch * math.cos(roll) - y * math.cos(roll)),
                             (xstart1 - ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.cos(math.atan(y / x1) - roll),
                              pitch * math.cos(roll) + ystart1 - ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.sin(
                                  -roll + math.atan(y / x1))),
                             3)
            i = i + 1
        # SNIZU PTICHKA
        pygame.draw.line(sc, WHITE, (xstart - 100, ystart), (xstart - 40, ystart), 5)
        pygame.draw.line(sc, WHITE, (xstart - 40, ystart), (xstart - 40, ystart + 15), 5)
        pygame.draw.line(sc, WHITE, (xstart + 100, ystart), (xstart + 40, ystart), 5)
        pygame.draw.line(sc, WHITE, (xstart + 40, ystart), (xstart + 40, ystart + 15), 5)
        pygame.draw.line(sc, WHITE, (xstart + 3, ystart), (xstart - 3, ystart), 5)

        pygame.draw.rect(sc, BLUE, ((xstart - 150, ystart - 155), (300, -30)), 0, 1, 7, 7, 1, 1)
        pygame.draw.rect(sc, BROWN, ((xstart - 150, ystart + 155), (300, +30)), 0, 1, 1, 1, 7, 7)


        pygame.display.update()

        clock.tick(FPS)

        if event.type == pygame.KEYDOWN:
            # Other buttons
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                a = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            a = False




def main():
    import tkinter
    mainwindow = tkinter.Tk()
    mainwindow.geometry("600x300+300+300")
    mainwindow.title('Complex attitude recovery')

    tkinter.Label(mainwindow,text='На данный момент в программе доступен только тренировочный режим,\n'
                          ' в нем у вас будет 5 секунд на то чтобы вывести "самолёт" из сложного пространственного положения,\n'
                          ' после чего программа вновь ввёдет СПП.\n'
                          'Данные о каждой проведенной попытке сохраняются в папке с программой ').pack()

    tkinter.Label(mainwindow,text='Введите Имя').pack()
    inputfield1 = tkinter.Entry(mainwindow)
    inputfield1.pack()

    tkinter.Label(mainwindow, text='Введите Фамилию').pack()
    inputfield2 = tkinter.Entry(mainwindow, )
    inputfield2.pack()

    tkinter.Label(mainwindow, text='Введите Отчество').pack()
    inputfield3 = tkinter.Entry(mainwindow, )
    inputfield3.pack()


    Startbutton = tkinter.Button(mainwindow, text='Start training!',command=pfd)

    def getinputvalues(*args):
        input1stname = inputfield1.get()
        inputlastname = inputfield2.get()
        inputmdlname = inputfield3.get()
        global username
        username = str('{}_{}_{}').format(inputmdlname , inputlastname , input1stname)
        #for i in args:


        if  input1stname == '' or inputlastname == '' or inputmdlname == '':
            Startbutton['state'] = 'disabled'
        else:
            Startbutton['state'] = 'normal'
        mainwindow.after(100, getinputvalues)

    getinputvalues()

    Startbutton.pack()

    mainwindow.mainloop()


main()
=======
def pfd():
    import pygame
    pygame.init()
    import os
    import time as timer
    recordtime = str(timer.ctime()).replace(':', '_')
    dirname = str(username + recordtime)
    try:
        os.mkdir(dirname)
    except Exception:
        pass
    finally:
        os.chdir(str(os.getcwd())+'/'+dirname)

    pygame.display.init()
    pygame.joystick.init()
    import matplotlib.pyplot as plt
    import math
    import table_creator
    import random
    import numpy as np

    # SETTINGS
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    W = 1200
    H = 800
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption('Vyvod Iz SPP')
    # pygame.display.set_icon(pygame.image.load())
    clock = pygame.time.Clock()
    FPS = 60
    a = True
    rounds = 5
    blindpitch = 0.05
    blindroll = 0.05
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (50, 50, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BROWN = (200, 155, 40)
    xstart = W // 2
    ystart = H // 2
    xstart1 = 150  # center of a brown surfase
    ystart1 = 180  # center of a brown surfase
    storona = 1200
    interval = 25
    shirina = 22
    speedroll = 0.3
    speedpitch = 10
    roll = random.random() * random.randint(-2, 2)
    pitch = random.randint(-200, +200)
    time = 10
    shag = int(FPS * rounds)
    surf = pygame.Surface((300, 360))
    surf.fill(BROWN)
    sc.blit(surf, (xstart - 150, ystart - 180))
    pygame.display.update()
    rolllist=[]
    pitchlist=[]
    yrolllist = []
    ypitchlist = []
    expnum = 0

    while a == True:

        for i in range(pygame.joystick.get_count()):

            if pygame.joystick.Joystick(i).get_axis(0) > -blindroll and pygame.joystick.Joystick(i).get_axis(0) < blindroll:
                speedroll = 0
            else:
                speedroll = pygame.joystick.Joystick(i).get_axis(0)

            speedroll1 = speedroll * 0.75
            roll += speedroll1 / 17
            speedpitch = pygame.joystick.Joystick(i).get_axis(1)


            if pitch > -23 and pitch<23:
                speedpitch1=speedpitch*1
            if pitch > -11 and pitch<11:
                speedpitch1=speedpitch*1.2
            elif pitch > -35 and pitch<35:
                speedpitch1 = 0.88 * pygame.joystick.Joystick(i).get_axis(1)
            else:
                speedpitch1=speedpitch*0.75

            if pygame.joystick.Joystick(i).get_axis(1) > -blindpitch and pygame.joystick.Joystick(i).get_axis(
                    1) < blindpitch:
                speedpitch = 0
            pitch += speedpitch1 * 4
            yrolllist.append(speedroll)
            ypitchlist.append(speedpitch)
            rolllist.append(roll*55)
            pitchlist.append(pitch/5)

        if len(ypitchlist) == shag:
            expnum += 1
            table_creator.tables_to_exc(ypitchlist, f'Pitch_table{expnum}')
            table_creator.tables_to_exc(yrolllist, f'Roll_table{expnum}')

            def Inputplot(expnum):

                xplot = np.linspace(0.0, FPS * rounds, shag)

                ypitchplot = ypitchlist
                yrollplot = yrolllist
                plt.figure(figsize=(8, 8))  # GRAFIKI START
                plt.subplot(211)
                plt.axis([0, FPS * rounds, -1.2, 1.2])
                plt.title('Pitch movement                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Amplitude', color='gray')
                plt.plot(xplot, ypitchplot)
                plt.grid()
                plt.subplot(212)
                plt.axis([0, FPS * rounds, -1.2, 1.2])
                plt.title('Roll movement                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Amplitude', color='gray')
                plt.plot(xplot, yrollplot)
                plt.grid()
               # plt.show()
                plt.savefig(str(recordtime)+'Input_plot'+str(expnum)+'.pdf',format='pdf')
                plt.close()
                pygame.time.delay(100)
                roll = random.random() * random.randint(-1, 1)
                pitch = random.randint(-50, +50)
                # if roll in np.arange(-0.2,0.2) ==True or pitch in np.arange(-1.0,1.0)==True:
                if (roll < 0.2 == True and roll > -0.2 == True) or (pitch < 30 == True and roll > -30 == True):
                    roll = random.random() * random.randint(-1, 1)
                    pitch = random.randint(-50, +50)
            Inputplot(expnum)
            def Attitudeplot(expnum):
              #  expnum += 1
                xplot = np.linspace(0.0, FPS * rounds, shag)

                rollplot=rolllist
                pitchplot=pitchlist
                plt.figure(figsize=(8, 8))  # GRAFIKI START
                plt.subplot(211)
                plt.axis([0, FPS * rounds, -90, 90])
                plt.title('Pitch attitude                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Degrees', color='gray')
                plt.plot(xplot, pitchplot)
                plt.grid()
                plt.subplot(212)
                plt.axis([0, FPS * rounds, -130, 130])
                plt.title('Roll attitude                              ', fontsize=12, fontname='Times New Roman')
                plt.xlabel('                    Time', color='gray')
                plt.ylabel('Degrees', color='gray')
                plt.plot(xplot, rollplot)
                plt.grid()
                plt.savefig(str(recordtime)+'Attitude_plot' + str(expnum) + '.pdf', format='pdf')
                plt.close()
                #plt.show()


            Attitudeplot(expnum)



        if len(ypitchlist) > FPS * rounds:
            print(ypitchlist)
            pitchlist = []
            rolllist = []
            ypitchlist = []
            yrolllist = []


            plusminus=random.randint(-1,1)
            if plusminus<=0:
                pitch = random.randint(-150, -60)
            else:
                pitch = random.randint(+60, +150)
            minusplus= random.randint(-1,1)
            if minusplus<=0:
                roll=random.random()*-1.7
            else:
                roll=random.random()*1.7

        for event in pygame.event.get():



            if event.type == pygame.KEYDOWN:
                # Other buttons

                if pygame.key.get_pressed()[pygame.K_RALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.display.set_mode((W, H), pygame.FULLSCREEN)
                    if pygame.key.get_pressed()[pygame.K_RALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                        pygame.display.set_mode((W, H))
                if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.display.set_mode((W, H), pygame.FULLSCREEN)
                    if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_RETURN]:
                        pygame.display.set_mode((W, H))
                #Упарвление РУС с клавы(данные в таблицу не записыаются)
                pygame.key.set_repeat(100, 50)
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    roll -= speedroll
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    roll += speedroll
                if pygame.key.get_pressed()[pygame.K_UP]:
                    pitch -= speedpitch * 10
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    pitch += speedpitch * 10
                if pygame.key.get_pressed()[pygame.K_r]:
                    pygame.time.delay(500)
                    roll = random.random() * random.randint(-2, 2)
                    pitch = random.randint(-200, +200)

                    if (math.sin(roll) < 0.9  and math.sin(roll) > -0.9) or (pitch < 50 == True and roll > -50 == True):
                        while (math.cos(roll) < 0.9 and math.cos(roll) > -0.9) or (
                                pitch < 50 and roll > -50):
                            roll = random.random() * random.randint(-2, 2)
                            pitch = random.randint(-200, +200)





        # Отрисовка

        sc.fill(BLACK)
        sc.blit(surf, (xstart - 150, ystart - 180))

        surf.fill(BROWN)
        pygame.draw.polygon(surf, BLUE, (
            (xstart1, ystart1 + pitch * math.cos(roll)),
            (xstart1 + storona * math.cos(roll), pitch * math.cos(roll) + ystart1 - storona * math.sin(roll)),
            (xstart1 + ((2 * (storona ** 2)) ** (1 / 2)) * math.cos(roll + 0.785398),
             pitch * math.cos(roll) + ystart1 - ((2 * (storona ** 2)) ** (1 / 2)) * math.sin(roll + 0.785398)),
            (xstart1 - storona * math.sin(roll), pitch * math.cos(roll) + ystart1 - storona * math.cos(roll)))
                            , 0)
        pygame.draw.polygon(surf, BLUE, (
            (xstart1, ystart1 + pitch * math.cos(roll)),
            (xstart1 - storona * math.cos(roll), pitch * math.cos(roll) + ystart1 + storona * math.sin(roll)),
            (xstart1 - ((2 * (storona ** 2)) ** (1 / 2)) * math.sin(roll + 0.785398),
             pitch * math.cos(roll) + ystart1 - ((2 * (storona ** 2)) ** (1 / 2)) * math.cos(roll + 0.785398)),
            (xstart1 - storona * math.sin(roll), pitch * math.cos(roll) + ystart1 - storona * math.cos(roll)))
                            , 0)
        # RISKI NIZJE

        i = -8
        while i <= 8:
            y = i * interval
            if i % 2 == 0:
                x1 = 2 * shirina
            else:
                x1 = shirina
            pygame.draw.line(surf, WHITE,
                             (xstart1 - y * math.sin(roll), ystart1 + pitch * math.cos(roll) - y * math.cos(roll)),
                             (xstart1 + ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.cos(math.atan(y / x1) + roll),
                              pitch * math.cos(roll) + ystart1 - ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.sin(
                                  roll + math.atan(y / x1))),
                             3)
            pygame.draw.line(surf, WHITE,
                             (xstart1 - y * math.sin(roll), ystart1 + pitch * math.cos(roll) - y * math.cos(roll)),
                             (xstart1 - ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.cos(math.atan(y / x1) - roll),
                              pitch * math.cos(roll) + ystart1 - ((y ** 2 + x1 ** 2) ** (1 / 2)) * math.sin(
                                  -roll + math.atan(y / x1))),
                             3)
            i = i + 1
        # SNIZU PTICHKA
        pygame.draw.line(sc, WHITE, (xstart - 100, ystart), (xstart - 40, ystart), 5)
        pygame.draw.line(sc, WHITE, (xstart - 40, ystart), (xstart - 40, ystart + 15), 5)
        pygame.draw.line(sc, WHITE, (xstart + 100, ystart), (xstart + 40, ystart), 5)
        pygame.draw.line(sc, WHITE, (xstart + 40, ystart), (xstart + 40, ystart + 15), 5)
        pygame.draw.line(sc, WHITE, (xstart + 3, ystart), (xstart - 3, ystart), 5)

        pygame.draw.rect(sc, BLUE, ((xstart - 150, ystart - 155), (300, -30)), 0, 1, 7, 7, 1, 1)
        pygame.draw.rect(sc, BROWN, ((xstart - 150, ystart + 155), (300, +30)), 0, 1, 1, 1, 7, 7)


        pygame.display.update()

        clock.tick(FPS)

        if event.type == pygame.KEYDOWN:
            # Other buttons
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                a = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            a = False




def main():
    import tkinter
    mainwindow = tkinter.Tk()
    mainwindow.geometry("600x300+300+300")
    mainwindow.title('Complex attitude recovery')

    tkinter.Label(mainwindow,text='На данный момент в программе доступен только тренировочный режим,\n'
                          ' в нем у вас будет 5 секунд на то чтобы вывести "самолёт" из сложного пространственного положения,\n'
                          ' после чего программа вновь ввёдет СПП.\n'
                          'Данные о каждой проведенной попытке сохраняются в папке с программой ').pack()

    tkinter.Label(mainwindow,text='Введите Имя').pack()
    inputfield1 = tkinter.Entry(mainwindow)
    inputfield1.pack()

    tkinter.Label(mainwindow, text='Введите Фамилию').pack()
    inputfield2 = tkinter.Entry(mainwindow, )
    inputfield2.pack()

    tkinter.Label(mainwindow, text='Введите Отчество').pack()
    inputfield3 = tkinter.Entry(mainwindow, )
    inputfield3.pack()


    Startbutton = tkinter.Button(mainwindow, text='Start training!',command=pfd)

    def getinputvalues(*args):
        input1stname = inputfield1.get()
        inputlastname = inputfield2.get()
        inputmdlname = inputfield3.get()
        global username
        username = str('{}_{}_{}').format(inputmdlname , inputlastname , input1stname)
        #for i in args:


        if  input1stname == '' or inputlastname == '' or inputmdlname == '':
            Startbutton['state'] = 'disabled'
        else:
            Startbutton['state'] = 'normal'
        mainwindow.after(100, getinputvalues)

    getinputvalues()

    Startbutton.pack()

    mainwindow.mainloop()


main()
>>>>>>> fc83f5b314f5662d46bc927333b5923bd66c0c3c:Вывод из СПП.py
