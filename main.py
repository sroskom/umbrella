from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color,Rectangle
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from subapps.grid_scroll import Grid_Scroll
from subapps.scrolling_sky import Scrolling_Sky
from subapps.flappybird_tutorial import Flappybird_Tutorial
from subapps.spritesheet_viewer import Spritesheet_Viewer
from subapps.side_scroller_viewer_landscape import Side_Scroller_Viewer_Landscape


class Global():
    debugMode = False

class GameSelector(Widget):
    def playGrid_Scroll(self,*args):
        self.parent.add_widget(Grid_Scroll())
        self.parent.remove_widget(self)
        
    def playScrolling_Sky(self,*args):
        self.parent.add_widget(Scrolling_Sky())
        self.parent.remove_widget(self)
        
    def playFlappybird_Tutorial(self,*args):
        self.parent.add_widget(Flappybird_Tutorial())
        self.parent.remove_widget(self)
        
    def playSpritesheet_Viewer(self,*args):
        self.parent.add_widget(Spritesheet_Viewer(size=self.size))
        self.parent.remove_widget(self)
        
    def playSide_Scroller_Viewer_Landscape(self,*args):
        self.parent.add_widget(Side_Scroller_Viewer_Landscape(size=self.size))
        self.parent.remove_widget(self)

              
    def __init__(self,**kwargs):
        super(GameSelector,self).__init__(**kwargs)
        gridlay = GridLayout(size=self.size,
                             cols=2)

        gridlay.add_widget(Button(text='playGrid_Scroll',
                                  on_press=self.playGrid_Scroll))
        gridlay.add_widget(Button(text='playScrolling_Sky',
                                  on_press=self.playScrolling_Sky))
        gridlay.add_widget(Button(text='playFlappybird_Tutorial',
                                  on_press=self.playFlappybird_Tutorial))
        gridlay.add_widget(Button(text='playSpritesheet_Viewer',
                                  on_press=self.playSpritesheet_Viewer))
        gridlay.add_widget(Button(text='playSide_Scroller_Viewer_Landscape',
                                  on_press=self.playSide_Scroller_Viewer_Landscape))
        self.add_widget(gridlay)
        
class Top(Widget):
    def __init__(self,*args):
        super(Top,self).__init__(*args)
        self.size = Window.size
        self.add_widget(MainMenu(size=self.size))

class GameArea(Widget):
    def __init__(self,size,*args):
        super(GameArea,self).__init__(size=size,*args)
        self.add_widget(GameSelector(size=self.size))

class SettingsScreen(Widget):
    def __init__(self,size,*args):
        super(SettingsScreen,self).__init__(size=size,*args)
        button_height = self.height*.10
        button_size = [button_height*6,button_height]
        self.option_1 = Label(text=('debug:on' if Global.debugMode
                                    else 'debug:off'),
                              size=button_size,
                              font_size=button_size[1],
                              pos=[0,self.height*.60])
        self.option_2 = Label(text='back',
                              size=button_size,
                              font_size=button_size[1],
                              pos=[0,self.height*.30])
        self.option_1.center_x = self.center_x
        self.option_2.center_x = self.center_x
        self.add_widget(self.option_1)
        self.add_widget(self.option_2)
        
    def on_touch_down(self,touch,*args):
        super(SettingsScreen,self).on_touch_down(touch,*args)
        if self.option_1.collide_point(*touch.pos):
            if not Global.debugMode:
                self.option_1.text = 'debug:on'
                Global.debugMode = True
            else:
                self.option_1.text = 'debug:off'
                Global.debugMode = False
        elif self.option_2.collide_point(*touch.pos):
            self.parent.add_widget(MainMenu(size=self.size))
            self.parent.remove_widget(self)
        
class MainMenu(Widget):
    def __init__(self,size,*args):
        super(MainMenu,self).__init__(size=size,*args)
        
        button_height = self.height*.10
        button_size = [button_height*5,button_height]
        self.option_1 = Label(text='play game',
                              size=button_size,
                              font_size=button_size[1],
                              pos=[0,self.height*.60])
        self.option_2 = Label(text='settings',
                              size=button_size,
                              font_size=button_size[1],
                              pos=[0,self.height*.30])
        self.option_1.center_x = self.center_x
        self.option_2.center_x = self.center_x
        self.add_widget(self.option_1)
        self.add_widget(self.option_2)
        
    def on_touch_down(self,touch,*args):
        super(MainMenu,self).on_touch_down(touch,*args)
        if self.option_1.collide_point(*touch.pos):
            self.parent.add_widget(GameArea(size=self.size))
            self.parent.remove_widget(self)
        elif self.option_2.collide_point(*touch.pos):
            self.parent.add_widget(SettingsScreen(size=self.size))
            self.parent.remove_widget(self)
        
        
class GameApp(App):
    def on_pause(self,*args):
        return True
    
    def build(self,*args):
        try:
            return Top()
        except Exception as exp:
            return Label(text=str(exp))

if __name__=='__main__':
    #Window.size = 300,450
    GameApp().run()
