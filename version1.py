from graphics import Canvas
import time
import random
import threading

import simpleaudio as sa

    
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
SIZE = 50

eat_sound = sa.WaveObject.from_wave_file('sounds/gulp.wav')
game_over_sound = sa.WaveObject.from_wave_file('sounds/game-over.wav')
youWin = sa.WaveObject.from_wave_file('sounds/you-win.wav')
Backgroundsound = sa.WaveObject.from_wave_file('sounds/nature.wav')

class Game1:
    def __init__(self, master=None):
        self.master = master
        self.won = False
        self.high_score = 0

    def main(self):
        def check_collisions(canvas, player):
            x1, y1 = canvas.coords(player)
            x2 = x1 + SIZE
            y2 = y1 + SIZE

            if x1 < 0 or x2 > CANVAS_WIDTH or y1 < 0 or y2 > CANVAS_HEIGHT:
                return True
            return False



        def generate_random_goal_position():
            x = random.randint(0, CANVAS_WIDTH - SIZE)
            y = random.randint(0, CANVAS_HEIGHT - SIZE)
            x -= x % SIZE
            y -= y % SIZE
            return x, y


        canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT,"MY BABY SNAKE GAME")
        canvas.master.iconbitmap('Game Logo.ico') 
        canvas.update()
        sd = eat_sound.play()
        sd.stop()
        
        canvas.create_image_with_size(0,0,CANVAS_WIDTH,CANVAS_HEIGHT,"Game Logo.png",0)
        canvas.update()

        background_sound_play_obj = Backgroundsound.play()

        
        time.sleep(3)


        image = canvas.create_image_with_size(0,0,CANVAS_WIDTH,CANVAS_HEIGHT,"bg.png",0)
        
        

        time.sleep(1)

        canvas.create_text(30,100,text = 'Welcome to Baby Snake Game ',font = 'Arial Rounded MT Bold',font_size = 23,color ='red')
        
        canvas.create_text(20,160,text = 'To win this game you need to ',font = 'Arial Rounded MT Bold',font_size = 23,color ='blue')
        canvas.create_text(20,195,text = 'score 50 points and if you touch ',font = 'Arial Rounded MT Bold',font_size = 23,color ='blue')
        canvas.create_text(20,230,text = 'the walls you will lose the game ',font = 'Arial Rounded MT Bold',font_size = 23,color ='blue')
        canvas.create_text(25,265,text = 'and use Arrow key to move.',font = 'Arial Rounded MT Bold',font_size = 23,color ='blue')
        canvas.update()

        time.sleep(5)

        canvas.clear()
        
        canvas.update()


        for i in range(30):
            canvas.create_line(50 *i, 0,50 *i, CANVAS_HEIGHT,"green")
            canvas.create_line(0, 50*i,CANVAS_WIDTH,50*i,"green")

        score = 0

        HS = 0

        sc = canvas.create_text(20,10,text = 'Score:- ' + str(score),font = 'Arial Rounded MT Bold',font_size = 25,color ='black')

        player = canvas.create_image_with_size(0,0,50,50,"snake.png",0) 
        goal = canvas.create_image_with_size(350,350,50,50,"apple.jpg",0) 
    

        DELAY = 0.1

        

        
        
        direction = 'right'
        direction_lock = threading.Lock()
        canvas.update()

        while True:
            canvas.update()


            keys = canvas.get_new_key_presses()
            canvas.update()

            for key in keys:
                if key.keysym in ['Left', 'Right', 'Up', 'Down']:
                    if (key.keysym == 'Left' and direction!= 'right') or \
                    (key.keysym == 'Right' and direction!= 'left') or \
                    (key.keysym == 'Up' and direction!= 'down') or \
                    (key.keysym == 'Down' and direction!= 'up'):
                        if key.keysym == 'Left':
                            direction = 'left'
                        elif key.keysym == 'Right':
                            direction = 'right'
                        elif key.keysym == 'Up':
                            direction = 'up'
                        elif key.keysym == 'Down':
                            direction = 'down'

                    canvas.update()
                    time.sleep(DELAY)

        #...
            if direction == 'left':
                canvas.move(player, -SIZE, 0)
            elif direction == 'right':
                canvas.move(player, SIZE, 0)
            elif direction == 'up':
                canvas.move(player, 0, -SIZE)
            elif direction == 'down':
                canvas.move(player, 0, SIZE)

            canvas.update()
            time.sleep(DELAY)
            #time.sleep(DELAY) 

            
        

            player_x1, player_y1 = canvas.coords(player)
            player_x2 = player_x1 + SIZE
            player_y2 = player_y1 + SIZE

            goal_x1, goal_y1 = canvas.coords(goal)
            goal_x2 = goal_x1 + SIZE
            goal_y2 = goal_y1 + SIZE

            canvas.update()

            if player_x1 == goal_x1 and player_y1 == goal_y1:
                canvas.delete(goal)
                canvas.delete(sc)
                new_x, new_y = generate_random_goal_position()
                goal = canvas.create_image_with_size(new_x, new_y, SIZE, SIZE, "apple.jpg",0)
                DELAY -= 0.001
                score += 1
                sc = canvas.create_text(20,10,text = 'Score:- ' + str(score),font = 'Arial Rounded MT Bold',font_size = 25,color ='black')
                canvas.update()
                sd = eat_sound.play()
                
                # Sleep

            if score == 50:
                print("You win")
                canvas.clear()
                background_sound_play_obj.stop()
                sd.stop()
                canvas.update()
                HS += score
                canvas.create_text(25,(CANVAS_WIDTH/2)-70,text = 'High Score:- ' + str(HS),font = 'Arial Rounded MT Bold',font_size = 45,color ='brown')
                canvas.update()
                time.sleep(1)
                image = canvas.create_image_with_size(0,0,CANVAS_HEIGHT,CANVAS_WIDTH,"win.png",0)
                canvas.update()
                youWin.play()
                time.sleep(1)
                self.won = True
                canvas.destroy()
                break


            

            if check_collisions(canvas, player):
                print("game over")
                canvas.clear()
                background_sound_play_obj.stop()
                sd.stop()
                canvas.update()
                HS += score
                canvas.create_text(25,(CANVAS_WIDTH/2)-70,text = 'High Score:- ' + str(HS),font = 'Arial Rounded MT Bold',font_size = 45,color ='brown')
                canvas.update()
                time.sleep(1)
                image = canvas.create_image_with_size(0,0,CANVAS_HEIGHT,CANVAS_WIDTH,"game over.png",0)
                canvas.update()
                game_over_sound.play()
                time.sleep(1.5)
                canvas.destroy()
                break  

            canvas.update()
            time.sleep(DELAY)


        
        
        

    

    if __name__ == '__main__':
        main(Canvas)
        