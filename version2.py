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

class Game2:  
    def __init__(self, master):
        self.master = master
        

    def main(self):
        def check_collisions(canvas, player):
            x1, y1 = canvas.coords(player[0])
            x2 = x1 + SIZE
            y2 = y1 + SIZE

            if x1 < 0 or x2 > CANVAS_WIDTH or y1 < 0 or y2 > CANVAS_HEIGHT:
                return True
                
            for part in player[2:]:
                part_x1, part_y1 = canvas.coords(part)
                part_x2 = part_x1 + SIZE
                part_y2 = part_y1 + SIZE
                if (part_x1 <= x1 < part_x2) and (part_y1 <= y1 < part_y2):
                    return True

            return False


        def generate_random_goal_position():
            x = random.randint(0, CANVAS_WIDTH - SIZE)
            y = random.randint(0, CANVAS_HEIGHT - SIZE)
            x -= x % SIZE
            y -= y % SIZE
            return x, y
    

        canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "MY BABY SNAKE GAME")
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
        canvas.create_text(20,195,text = 'score 25 points and if you touch ',font = 'Arial Rounded MT Bold',font_size = 23,color ='blue')
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

        player = [canvas.create_image_with_size(0,0,50,50,"snake1.png",0)]
        
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


            for i in range(len(player) - 1, 0, -1):
                coords = canvas.coords(player[i-1])
                if coords:  # Check if coords is not empty
                    x1, y1 = coords
                    canvas.coords(player[i], x1, y1)
                else:
                    print(f"Player {i-1} doesn't exist on the canvas")


            canvas.update()
            time.sleep(DELAY)
            #time.sleep(DELAY) 

            
        

            
            player_x1, player_y1 = canvas.coords(player[0])
            player_x2 = player_x1 + SIZE
            player_y2 = player_y1 + SIZE
        

            goal_x1, goal_y1 = canvas.coords(goal)
            goal_x2 = goal_x1 + SIZE
            goal_y2 = goal_y1 + SIZE

            canvas.update()

            if player_x1 == goal_x1 and player_y1 == goal_y1:
                last_x1, last_y1 = canvas.coords(player[-1])
                last_x2 = last_x1 + SIZE
                last_y2 = last_y1 + SIZE 
                new_rectangle = canvas.create_image_with_size(int(last_x1),int(last_y1),SIZE,SIZE,"snake2.png",0)
                player.append(new_rectangle)
                canvas.delete(goal)
                canvas.delete(sc)
                new_x, new_y = generate_random_goal_position()
                goal = canvas.create_image_with_size(new_x, new_y, SIZE, SIZE, "apple.jpg",0)
                DELAY -= 0.001
                score += 1
                sc = canvas.create_text(20,10,text = 'Score:- ' + str(score),font = 'Arial Rounded MT Bold',font_size = 25,color ='black')
                sd = eat_sound.play()
                canvas.update()
                

            
            if direction == 'left' or direction == 'right':
                canvas.move(player[0], -SIZE if direction == 'left' else SIZE, 0)
                canvas.rotate_images(player[1:], 0,SIZE,SIZE)
                #pil_image = pil_image.rotate(90)
            elif direction == 'up' or direction == 'down':
                canvas.move(player[0], 0, -SIZE if direction == 'up' else SIZE)
                canvas.rotate_images(player[1:], 90,SIZE,SIZE)  # Add this line
                #pil_image = pil_image.rotate(90)  # Remove this line if not needed
                
                # Sleep

            if score == 25:
                print("You win")
                canvas.clear()
                background_sound_play_obj.stop()
                sd.stop()
                canvas.update()
                new_HS = score
                if new_HS > HS:
                    HS = new_HS
                    canvas.create_text(25,(CANVAS_WIDTH/2)-70,text = 'High Score:- ' + str(new_HS),font = 'Arial Rounded MT Bold',font_size = 45,color ='brown')
                else:
                    canvas.create_text(25,(CANVAS_WIDTH/2)-70,text = 'High Score:- ' + str(new_HS),font = 'Arial Rounded MT Bold',font_size = 45,color ='brown')
                canvas.update()
                time.sleep(1)
                image = canvas.create_image_with_size(0,0,CANVAS_HEIGHT,CANVAS_WIDTH,"win.png",0)
                canvas.update()
                youWin.play()
                time.sleep(2) 
                break


    


            

            if check_collisions(canvas, player):
                print("game over")
                canvas.clear()
                background_sound_play_obj.stop()
                sd.stop()
                canvas.update()
                new_HS = score
                if new_HS > HS:
                    HS = new_HS
                    canvas.create_text(25,(CANVAS_WIDTH/2)-70,text = 'High Score:- ' + str(new_HS),font = 'Arial Rounded MT Bold',font_size = 45,color ='brown')
                else:
                    canvas.create_text(25,(CANVAS_WIDTH/2)-70,text = 'High Score:- ' + str(new_HS),font = 'Arial Rounded MT Bold',font_size = 45,color ='brown')
                canvas.update()
                time.sleep(1)
                image = canvas.create_image_with_size(0,0,CANVAS_HEIGHT,CANVAS_WIDTH,"game over.png",0)
                canvas.update()
                game_over_sound.play()
                time.sleep(2)
                break  

            canvas.update()
            time.sleep(DELAY)
        




    

        
            

if __name__ == '__main__':
    
    game = Game2(Canvas)
    game.main()