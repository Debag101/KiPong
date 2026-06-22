from kivy.uix.screenmanager import Screen
from kivy.properties import Clock
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.animation import Animation

from kivy.properties import ListProperty, StringProperty, NumericProperty

from kivy.metrics import dp
from kivy.core.window import Window

from kivy.core.audio import SoundLoader

class GameWindow(Screen):

    paddle_size = ListProperty([0,0])
    ball_size = ListProperty([dp(20), dp(20)])

    left_paddle_pos = ListProperty([0, 0])
    right_paddle_pos = ListProperty([0, 0])
    ball_pos = ListProperty([0,0])

    left_player_score = StringProperty('0')
    right_player_score = StringProperty('0')

    left_panel_color = ListProperty([0, 0, 0, 0])
    right_panel_color = ListProperty([0, 0, 0, 0])

    left_msg = StringProperty('')
    right_msg = StringProperty('')

    bounce_sound = SoundLoader.load('../resources/audio/bounce.mp3')
    victory_sound = SoundLoader.load('../resources/audio/victory.mp3')

    opa = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_playing = False

        self.frames = 60
        self.ball_velocity_x = 900
        self.ball_velocity_y = 0
        self.ball_velocity_y_cap = 1000
        self.paddle_velocity = 15
        self.y_vel_multiplier = 50
        self.action_keys = set()

        self.left_score = 0
        self.right_score = 0

        self.score_threshold = 5

        Window.bind(on_key_down = self.on_keyboard_down)
        Window.bind(on_key_up = self.on_keyboard_up)


    
    def on_enter(self, *args):
        self.game_event = Clock.schedule_interval(self.gameloop, 1/self.frames)
        self.on_size()
        self.is_playing = True

    def on_leave(self, *args):
        self.on_size()

        self.win_msg = ""
        self.left_score = 0
        self.right_score = 0
        self.left_player_score = '0'
        self.right_player_score = '0'

        self.left_msg = ''
        self.right_msg = ''

        self.left_panel_color = [0,0,0,0]
        self.right_panel_color = [0,0,0,0]

        self.opa = 0

        self.game_event.cancel()


    def on_size(self, *args):

        self.paddle_size = [dp(30), dp(120)]
        self.left_paddle_pos = [0, (self.height - self.paddle_size[1]) / 2]
        self.right_paddle_pos = [self.width - self.paddle_size[0], (self.height - self.paddle_size[1]) / 2]

        self.ball_pos = [
                        (self.width - self.ball_size[0])/2,
                        (self.height - self.ball_size[0])/2
                        ]
        
    
    def gameloop(self, dt):

        if not self.is_playing:
            return
        
        rp_curr_vel = 0
        lp_curr_vel = 0 
        
        if 'w' in self.action_keys:
            self.left_paddle_pos[1] += self.paddle_velocity
            lp_curr_vel = self.paddle_velocity

        if 's' in self.action_keys:
            self.left_paddle_pos[1] -= self.paddle_velocity
            lp_curr_vel = self.paddle_velocity * -1
            
        if 'i' in self.action_keys:
            self.right_paddle_pos[1] += self.paddle_velocity
            rp_curr_vel = self.paddle_velocity

        if 'j' in self.action_keys:
            self.right_paddle_pos[1] -= self.paddle_velocity
            rp_curr_vel = self.paddle_velocity * -1

        # The ball is inscribed inside a square of side = diam of the circle, and bot left corner is the ball_pos coords

        # corner_x and corner_y then actually denote the corner points after simulating a displacement
        corner_x = self.ball_pos[0] + self.ball_velocity_x * dt
        corner_y = self.ball_pos[1] + self.ball_velocity_y * dt

        r_ball_pt_x = corner_x + self.ball_size[0]
        l_ball_pt_x = corner_x
        
        #both points have same y coord
        ball_pt_y = corner_y + self.ball_size[0]/2

        #top and bottom edges, only need the y

        top_ball_pt = corner_y + self.ball_size[0]
        bottom_ball_pt = corner_y


        # checking collision with paddles

        if (self.width >= r_ball_pt_x >= self.right_paddle_pos[0] and self.right_paddle_pos[1] <= ball_pt_y <= self.right_paddle_pos[1] + self.paddle_size[1]):            
            self.ball_velocity_x *= -1
            self.ball_velocity_y += rp_curr_vel * self.y_vel_multiplier
            self.bounce_sound.play()

            if self.ball_velocity_y > self.ball_velocity_y_cap:
                self.ball_velocity_y  = self.ball_velocity_y_cap


        elif (0<=l_ball_pt_x <= self.paddle_size[0] and self.left_paddle_pos[1] <= ball_pt_y <= self.left_paddle_pos[1] + self.paddle_size[1]):
            self.ball_velocity_x *= -1
            self.ball_velocity_y += lp_curr_vel * self.y_vel_multiplier
            self.bounce_sound.play()

            if self.ball_velocity_y < self.ball_velocity_y_cap * -1:
                self.ball_velocity_y  = self.ball_velocity_y_cap * -1
            

        # Ball going out of boundary
        elif(r_ball_pt_x >= self.width or l_ball_pt_x <= 0):
            self.ball_velocity_y = 0
            
            if self.ball_velocity_x <= 0:
                self.right_score += 1
                self.right_player_score = str(self.right_score)
            else:
                self.left_score += 1
                self.left_player_score = str(self.left_score)


            if self.right_score == self.score_threshold:
                self.game_over('RIGHT')
            
            if self.left_score == self.score_threshold:
                self.game_over('LEFT')

            self.on_size()
            return 

        elif top_ball_pt >= self.height or bottom_ball_pt <= 0:
            self.ball_velocity_y *= -1
        

        corner_x = self.ball_pos[0] + self.ball_velocity_x * dt
        corner_y = self.ball_pos[1] + self.ball_velocity_y * dt
 
        self.ball_pos = [corner_x, corner_y]
        

    def on_keyboard_down(self, *args):
        self.action_keys.add(args[3])
        return True
    
    def on_keyboard_up(self, *args):
        key_up = chr(args[2] + 93)
        if key_up in self.action_keys:
            self.action_keys.remove(key_up)
        return True
    

    def game_over(self, winner):
        
        self.is_playing = False
        self.on_size()

        if winner == 'LEFT':
            self.left_panel_color = [0,1,0,0]
            self.right_panel_color = [1,0,0,0]

            self.left_msg = 'WON'
            self.right_msg = 'LOST'

        else:
            self.left_panel_color = [1,0,0,0]
            self.right_panel_color = [0,1,0,0]

            self.left_msg = 'LOST'
            self.right_msg = 'WIN'

        self.victory_sound.play()

        anim_left = Animation(left_panel_color=[self.left_panel_color[0], self.left_panel_color[1], self.left_panel_color[2], 0.4], duration=2.5)
        anim_right = Animation(right_panel_color=[self.right_panel_color[0], self.right_panel_color[1], self.right_panel_color[2], 0.4], duration=2.5)
        
        anim_left.start(self)
        anim_right.start(self)

        Clock.schedule_once(self.show_buttons, 3)

    def show_buttons(self, dt):
        self.opa = 100

    def game_refresh(self):

        self.win_msg = ""
        self.left_score = 0
        self.right_score = 0
        self.left_player_score = '0'
        self.right_player_score = '0'

        self.left_msg = ''
        self.right_msg = ''

        self.left_panel_color = [0,0,0,0]
        self.right_panel_color = [0,0,0,0]

        self.opa = 0

        self.is_playing = True

    
