from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color,Rectangle
from kivy.clock import Clock

class Background(Widget):
    def __init__(self,**kwargs):
        super(Background,self).__init__(**kwargs)
        self.size = Window.size
        with self.canvas:
            Color(1,1,1,.8)
            self.rect = Rectangle(source='images/scrolling_sky/sky1.png',
                                  size=self.size)
        print('init background')
    def update(self,*args):
        self.rect.pos = [self.rect.pos[0]+1,
                         self.rect.pos[1]]
        if self.rect.pos[0] >= Window.width:
            self.rect.pos = [Window.width*(-1),0]
        
class Top(Widget):
    def update(self,*args):
        self.background_1.update()
        self.background_2.update()
        fadespeed = .019
        if self.fade_toggle:
            self.color.a -= fadespeed
        else:
            self.color.a += fadespeed
        if self.color.a <= 0:
            self.fade_toggle = False
        if self.color.a >= 1:
            self.fade_toggle = True
        
        
    def __init__(self,**kwargs):
        super(Top,self).__init__(**kwargs)
        self.size = Window.size
        self.fade_toggle = True
        with self.canvas:
            self.color = Color(1,.9,.7,1)
            Rectangle(size=self.size)            
        print(str(Window.size))
        self.background_1 = Background()
        self.background_2 = Background()
        self.background_2.rect.pos = [Window.width*(-1),
                                      0]
        
        self.add_widget(self.background_1)
        self.add_widget(self.background_2)
        Clock.schedule_interval(self.update,3.0/60.0)

class GameApp(App):
    def build(self,*args):
        return Top()

if __name__=='__main__':
    Window.size = 300,450
    game = GameApp()
    game.run()
