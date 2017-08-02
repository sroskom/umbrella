from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color,Rectangle,Rotate
from kivy.clock import Clock
import os
from kivy.core.window import Window

class Sprite(Image):
    def __init__(self,*args, **kwargs):
        super(Sprite,self,*args).__init__(*args,**kwargs)
        ratio = self.texture.size[1]/float(Window.height)
        self.size = self.texture.size[0]/ratio,Window.height  

class Background(Sprite):
    def __init__(self, *args, **kwargs):
        super(Background, self).__init__(*args,**kwargs)
        self.image = Sprite(source=kwargs.get('source'))
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=kwargs.get('source'), x=self.width)
        self.add_widget(self.image_dupe)
        
    def update(self, *args):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width
            
class Game(ScreenManager):
    def nextScreen(self, *args):
        self.current = self.next()
        
    def update(self, background):
        background.update()   
    
    def __init__(self, *args,**kwargs):
        super(Game, self).__init__(*args,**kwargs)
        user_data_dir = App.get_running_app().user_data_dir
        imgdir = os.path.join(user_data_dir,'images')
        
        if os.path.isdir(imgdir) and len(os.listdir(imgdir))>0:
            imglist = os.listdir(imgdir)
            
            for img in imglist:
                background = Background(source=os.path.join(imgdir,img))
                
                widget = Widget()
                
                button = Button(text='+')
                button.pos = [20,20]
                button.bind(on_press=self.nextScreen)
                
                widget.add_widget(background)
                widget.add_widget(button)
                
                
                screen = Screen()
                screen.name = img
                screen.add_widget(widget)
                self.add_widget(screen)

                Clock.schedule_interval(background.update, 1.0/60.0)
        else:
            if not os.path.isdir(imgdir):
                os.makedirs(imgdir)
                
            screen = Screen()
            screen.add_widget(Label(text='no images at: '+imgdir))
            self.add_widget(screen)
        

class SideScrollerApp(App):
    def on_pause(self, *args):
        return True
    
    def build(self, *args):
        try:
            return Game()
        except Exception as exp:
            return Label(text=str(exp))
            

if __name__ == '__main__':
    SideScrollerApp().run()
