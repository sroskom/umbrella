from kivy.app import App
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
import os
from SpriteViewer import SpriteAnimator


class DirButton(Button):
    def __init__(self,fdir,*args):
        super(DirButton,self).__init__(*args)
        self.text = fdir
    
    def on_press(self,*args):
        screen = Screen()
        screen.name = self.text
        screen.add_widget(SpriteAnimator(self.text))
        manager = App.get_running_app().root
        manager.add_widget(screen)
        manager.current = screen.name
    
class Top(Widget):
    def __init__(self,**kwargs):
        super(Top,self).__init__(**kwargs)
        dirlst = os.listdir('./images/spritesheet_viewer/')
        manager = ScreenManager()
        screen1 = Screen()
        screen1.name = 'main'
        
        bxlayout = BoxLayout(orientation='vertical')
        for f in dirlst:
            if f.find('.png') > -1 or f.find('.jpg') > -1:
                bxlayout.add_widget(DirButton(fdir=f))
        if not len(bxlayout.children):
            bxlayout.add_widget(Label(text='no .png or .jpg files found'))
        screen1.add_widget(bxlayout)
        manager.add_widget(screen1)
        self.add_widget(manager)
        
class GameApp(App):
    def build(self,*args):
        return Top()
    

if __name__=='__main__':
    GameApp().run()

