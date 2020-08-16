
# Для начала игры поставьте модуль keyboard (pip install keyboard)

import os, time, random, threading, keyboard

duble_cactus_flag = False
game_loop_flag = True
game_not_started = True
end_game_mode = 0

dino_sit = False
dino_jump = False

dino_jump_flag = False

dino_numb_jump = 0
dino_numb_sit = 0

gameOverText = '''
  ___                                                
 / __|  __ _   _ __    ___     ___  __ __  ___   _ _     
| (_ | / _` | | '  \  / -_)   / _ \ \ V / / -_) | '_|     \033[47m\033[30m R Ctrl \033[49m\033[39m - Играть ещё!
 \___| \__,_| |_|_|_| \___|   \___/  \_/  \___| |_|       \033[47m\033[30m Esc \033[49m\033[39m - Выйти из игры
'''


def listen_pressed_keys(e):

    global game_loop_flag, dino_numb_jump, dino_numb_sit, dino_jump_flag, dino_sit, dino_jump, game_not_started, end_game_mode

    if e.event_type == 'down' and e.name == 'down': 
        dino_sit = True
        dino_numb_jump = 0
        dino_numb_sit = 8

    if e.event_type == 'down' and e.name == 'up' and dino_numb_jump == 0 and dino_jump_flag == False: 
        dino_jump = True
        dino_jump_flag = True
        dino_numb_jump = 4
        dino_numb_sit = 0

    if e.event_type == 'down' and e.name == 'esc' and game_loop_flag: game_loop_flag = False
    if e.event_type == 'down' and e.name == 'right ctrl' and game_loop_flag: game_not_started = False

    if e.event_type == 'down' and e.name == 'right ctrl' and not game_loop_flag: end_game_mode = 1
    if e.event_type == 'down' and e.name == 'esc' and not game_loop_flag: end_game_mode = 2

def draw():
    keyboard.hook(listen_pressed_keys)
    keyboard.wait()

def game():

    os.system('cls||clear')

    global dino_sit, dino_jump, dino_jump_flag, dino_numb_jump, dino_numb_sit, duble_cactus_flag, game_loop_flag, gameOverText, game_not_started, end_game_mode

    duble_cactus_flag = False
    game_loop_flag = True
    dino_sit = False
    dino_jump = False
    dino_numb_jump = 0
    dino_numb_sit = 0
    end_game_mode = 0

    t = threading.Thread(target=draw, args=())
    t.start()

    hi = 0
    hi_true = 0

    speed = 0.2
    score_start = '                                                                                              HI '

    f = open('record.txt', 'r')

    best_score = f.read()
    best_score_int = int(best_score)

    f.close()

    r = [4, 3, 2, 1, 0]
    image_save = [' ', ' ', ' ', ' ', ' ']

    width = 0
    start_width = 0
    bird_flag = True

    menu = '''
                 ___                           _              _   _                    \033[47m\033[30m Up \033[49m\033[39m - Прыжок
                / __|  ___   _ _    ___  ___  | |  ___     __| | (_)  _ _    ___       \033[47m\033[30m Down \033[49m\033[39m - Присесть
               | (__  / _ \ | ' \  (_-< / _ \ | | / -_)   / _` | | | | ' \  / _ \      \033[47m\033[30m R Ctrl \033[49m\033[39m - Играть
                \___| \___/ |_||_| /__/ \___/ |_| \___|   \__,_| |_| |_||_| \___/      \033[47m\033[30m Esc \033[49m\033[39m - Выйти из игры
    '''

    screenlines = ["                 ___                           _              _   _                                         ",
                   "                / __|  ___   _ _    ___  ___  | |  ___     __| | (_)  _ _    ___                            ",
                   "               | (__  / _ \ | ' \  (_-< / _ \ | | / -_)   / _` | | | | ' \  / _ \                           ",
                   "                \___| \___/ |_||_| /__/ \___/ |_| \___|   \__,_| |_| |_||_| \___/                           ",
                   "____________________________________________________________________________________________________________"]

    road = ".       ..       .  .            .  .          .  .              ....            .   .            .   .    ."

    print(menu)
    while game_not_started and game_loop_flag:
        time.sleep(0.5)

    os.system('cls||clear')

    if not game_loop_flag:
        print("Выход из игры ...\n")
        os._exit(0)

    while game_loop_flag:

        # Randon

        height = random.randint(1, 2)

        if width == 0: # Если пришло время спавна препядствия
            width = random.randint(10, 30)
            start_width = width
            bird_flag = True

            duble_cactus_flag = True
            for x in r:
                screenlines[x] = screenlines[x][1:]
                if height > 0:
                    screenlines[x] += '#'
                    height -= 1
                else:
                    if x != 4: screenlines[x] += ' '
                    else: screenlines[x] += '_'
        else:
            width -= 1

            height = random.randint(1, 2)
            chance = random.randint(0, 1)

            bird_chance = random.randint(0, 10)
            bird_height = random.randint(2, 4)

            for x in r:
                screenlines[x] = screenlines[x][1:]
                if chance == 0 and height > 0 and duble_cactus_flag:
                    screenlines[x] += '#'
                    height -= 1
                else:
                    if hi_true > 400 and bird_flag and start_width - width > 4 and width > 4 and bird_chance == 0 and bird_height == x:
                        screenlines[x] += '<'
                        bird_flag = False
                    else:
                        if x != 4: screenlines[x] += ' '
                        else: screenlines[x] += '_' 
            
            duble_cactus_flag = False

        # Спавн камешков :)

        road = road[1:]
        road_stone = random.randint(1, 10)

        if road_stone == 1: 
            road += '.'
        else: 
            road += ' '
                
                
        hi += 1
        hi_true = hi - 99
        

        # Dino

        # Проверка на врезание в кактусы
        if dino_sit and screenlines[4][9] == '#': game_loop_flag = False
        if dino_jump and screenlines[0][9] == '#': game_loop_flag = False
        if dino_jump and screenlines[0][9] == '#': game_loop_flag = False
        if not dino_jump and not dino_sit and screenlines[4][9] == '#': game_loop_flag = False
        if not dino_jump and not dino_sit and screenlines[3][9] == '#': game_loop_flag = False

        # Запоминание обьектов за дино
        for x in r:     
            screenlines[x] = screenlines[x][:8] + image_save[x] + screenlines[x][9:]

        for x in r:
            image_save[x] = screenlines[x][9]

        if not dino_jump:
            dino_jump_flag = False

        # Отрисовка динозаврика
        if dino_sit:
            screenlines[4] = screenlines[4][:9] + 'P' + screenlines[4][10:]
        elif dino_jump:
            screenlines[1] = screenlines[1][:9] + '˄' + screenlines[1][10:]
            screenlines[0] = screenlines[0][:9] + 'P' + screenlines[0][10:]
        else:
            if hi%2 == 0: screenlines[4] = screenlines[4][:9] + 'л' + screenlines[4][10:]
            else: screenlines[4] = screenlines[4][:9] + 'l' + screenlines[4][10:]
            screenlines[3] = screenlines[3][:9] + 'P' + screenlines[3][10:]

        # Отрисовка очков

        # Drow screen
        if hi_true < 0: hi_str = '0'
        else: hi_str = str(hi_true)

        text = '0' * (5 - len(best_score))
        text += best_score
        score = text + ' '
        text = ''

        text = '0' * (5 - len(hi_str))
        text += hi_str
        score += text
        text = ''

        print(score_start + score)

        for line in screenlines:
            print(line)

        print(road)

        # Update screen

        if dino_numb_sit > 0:
            dino_numb_sit -= 1
        else:
            dino_sit = False

        if dino_numb_jump > 0:
            dino_numb_jump -= 1
        else:
            dino_jump = False

        if (hi_true) % 100 == 0 and speed != 0.02:
            speed -= 0.02

        # time.sleep(speed) На очистку экрана тратится и так слишком много времени
        os.system('cls||clear')

        if not game_loop_flag:
            print(gameOverText)
            print("Ваш счет: ", hi_true)

            if hi_true > best_score_int:
                f = open('record.txt', 'w')
                f.write(hi_str)
                f.close()

            while end_game_mode == 0:
                time.sleep(0.5)

            if end_game_mode == 1: game()
            else: 
                print("Выход из игры ...\n")
                os._exit(0)


# Стартуем!
game()