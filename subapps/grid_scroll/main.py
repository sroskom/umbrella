from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import random
from kivy.graphics import Color,Rectangle
from kivy.uix.image import Image
from kivy.clock import Clock

class Globals():
    debugMode = False
    
class Menu(Widget):
    def gennewback(self):
        return self.lstbacks[random.randint(0,len(self.lstbacks)-1)]

    def setnewback(self,*args):
        self.rect.texture = Image(source=self.gennewback()).texture

    def fadeoutBackground(self,*args):
        amt = .02
        if not self.paused:
            
            if not self.togglefade:
                self.color2.a += amt
            else:
                self.color2.a -= amt
            if self.color2.a >= 1:
                self.rect.texture = Image(source=self.gennewback()).texture
                self.togglefade = True
            if self.color2.a <= 0:
                self.togglefade = False
                self.paused = True
        else:
            self.fadecounter +=1
            if self.fadecounter >= self.fadepauseAmt:
                self.fadecounter = 0
                self.paused = False

    def moveGameArea(self,*args):
        sped = 2
        self.gameWidBack1.pos = self.gameWidBack1.pos[0]+sped,0
        if self.gameWidBack1.pos[0]>=self.width:
            self.gameWidBack1.pos = self.width*(-1),0
            for i in self.back_1pattern:
                i.pos = i.pos[0]+(self.width*(-2)),i.pos[1]
        for i in self.back_1pattern:
            i.pos = sped+i.pos[0],i.pos[1]
        self.gameWidBack2.pos = self.gameWidBack2.pos[0]+sped,0
        if self.gameWidBack2.pos[0]>=self.width:
            self.gameWidBack2.pos = self.width*(-1),0
            for i in self.back_2pattern:
                i.pos = i.pos[0]+(self.width*(-2)),i.pos[1]
        for i in self.back_2pattern:
            i.pos = sped+i.pos[0],i.pos[1]
        
    def fadeToBlack(self,*args):
        self.endingFadeCol.a += .02
        if self.endingFadeCol.a >= 1:
            gameWid = Widget(size=self.size)
            self.gameWidBack1 = Widget(size=self.size)
            self.gameWidBack2 = Widget(size=self.size)
            #self.gameWidBack1.canvas.bind(pos=self.gameWidBack1.pos)
            self.gameWidBack2.pos = [self.gameWidBack2.width*(-1),0]
            backs = [self.gameWidBack1,self.gameWidBack2]
            for i in backs:
                with i.canvas:
                    Color(*[.9,.9,.8,.2])
                    if i == backs[0]:
                        self.back_1pattern = self.pattern3()
                    else:
                        self.back_2pattern = self.pattern3()
                gameWid.add_widget(i)

            for i in self.back_1pattern:
                i.pos = self.gameWidBack1.pos[0]+i.pos[0],i.pos[1]
            for i in self.back_2pattern:
                i.pos = self.gameWidBack2.pos[0]+i.pos[0],i.pos[1]
            Clock.schedule_interval(self.moveGameArea,3.0/60.0)
            self.parent.add_widget(gameWid)
            self.parent.remove_widget(self)
            #self.pattern4Buttons()
            return False
        
    def fadeintoNewback(self,*args):
        Clock.schedule_interval(self.fadeoutBackground,3.0/60.0)

    def toggledebugMode(self,*args):
        if not Globals.debugMode:
            self.parent.enterdebugMode()
        else:
            Globals.debugMode = False

    def pattern1(self,*args):
        pattern = []
        for b in range(0,(self.height/32)+1):
            for i in range(0,(self.width/32)+1):
                pattern.append(Rectangle(size=[16,16],pos=[(i*16)+(i*16),(b*16)+(b*16)]))
        return pattern
    
    def pattern2(self,*args):
        toggle = False
        sqrsize = self.width/100
        for b in range(0,(self.height/sqrsize)+1):
            for i in range(0,(self.width/sqrsize/2)+1):
                adj = 0
                if not toggle:
                    adj = sqrsize
                Rectangle(size=[sqrsize,sqrsize],
                          pos=[(i*sqrsize)+(i*sqrsize)+adj,(b*sqrsize)])
            if toggle:
                toggle = False
            else:
                toggle = True
                
    def pattern3(self,*args):
        linethick = 3
        sqrsize = self.width/20
        pattern = []
        for b in range(0,(self.height/sqrsize)+1):
            for i in range(0,(self.width/sqrsize)+1):
                pattern.append(Rectangle(size=[linethick,sqrsize],
                          pos=[(i*sqrsize),(b*sqrsize)]))
                pattern.append(Rectangle(size=[sqrsize,linethick],
                          pos=[(i*sqrsize),(b*sqrsize)]))
        return pattern

    def pattern4Buttons(self,*args):
        #pattern = []
        for b in range(0,(self.height/32)+1):
            for i in range(0,(self.width/32)+1):
                #rect = Rectangle(size=[16,16],pos=[(i*16)+(i*16),(b*16)+(b*16)])
                #pattern.append(rect)
                self.gameWidBack1.add_widget(Button(size=[16,16],pos=[(i*16)+(i*16),(b*16)+(b*16)]))
        #return pattern
      
                
    def startPlay(self,*args):
        with self.canvas:
            self.endingFadeCol = Color(0,0,0,0)
            self.endingFadeRect = Rectangle(size=self.size)
        Clock.schedule_interval(self.fadeToBlack,3.0/60.0)    
        
        
    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)
        self.lstbacks = ['images/grid_scroll/Badlands.png','images/grid_scroll/FireTemple.png',
                         'images/grid_scroll/IcePalace.png']
        with self.canvas:
            self.color1 = Color(1,1,1,1)
            self.rect = Rectangle(texture=
                                  Image(source=
                                        self.gennewback()).texture,
                                  size=self.size)
            self.color2 = Color(0,0,0,0)
            self.rect2 = Rectangle(size=self.size)
            
            
        butsize = self.width/3,self.height/5
        font_name = 'images/grid_scroll/04B_19.ttf'
        font_color = [.9,.9,.8,1]
        #font_color = [1,0,0,1]
        button_color = [.9,.9,.8,.2]
        self.option_1 = Button(text='play',size=butsize,
                          font_name=font_name,
                               color=font_color)
        self.option_2 = Button(text='settings',size=butsize,
                          font_name=font_name,
                               color=font_color)
        
            
        self.add_widget(self.option_1)
        self.add_widget(self.option_2)
        self.option_1.center=self.center
        self.option_2.center=self.center[0],self.height/4

        with self.option_1.canvas.before:
            Color(*button_color)
            Rectangle(size=self.option_1.size,
                      pos=self.option_1.pos)
            
        with self.option_2.canvas.before:
            Color(*button_color)
            Rectangle(size=self.option_2.size,
                      pos=self.option_2.pos)
        

        with self.canvas:
            Color(*button_color)
            self.pattern2()

        self.option_1.bind(on_press=self.startPlay)
        self.option_2.bind(on_press=self.toggledebugMode)
        
        self.paused = False
        self.fadepauseAmt = 120
        self.fadecounter = 0
        self.togglefade = False
        self.fadeintoNewback()
        
class Top(Widget):
    def updatefpslabel(self, *args):
        if Globals.debugMode:
            self.fpslabel.opacity = 1
            self.fpslabel.text = 'rfps:'+ str(Clock.get_rfps())
        else:
            self.fpslabel.opacity = 0
            return False

    def enterdebugMode(self, *args):
        Globals.debugMode = True
        Clock.schedule_interval(self.updatefpslabel,1.0/60.0)
        
    def __init__(self,**kwargs):
        super(Top,self).__init__(**kwargs)
        self.size = Window.size
        with self.canvas:
            Color(0,0,0,1)
            Rectangle(size=self.size)
        self.fpslabel = Label(text='rfps:'+str(Clock.get_rfps()),
                              size=[100,50],opacity=0)
        self.fpslabel.pos = 0,0
        menu = Menu(size=self.size)
        self.add_widget(menu)
        self.add_widget(self.fpslabel)
        
        
        
class GameApp(App):
    def on_pause(self,*args):
        return True
    def genlst(self,lstsize):
        lst = []
        for i in range(lstsize):
            lst.append(random.randint(0,3))
        return str(lst)
    
    def clickButton(self,*args):
        self.randLabel.text = self.genlst(int(self.txtinp.text))
    
    def build(self,*args):
        
        self.randLabel = Label(text=self.genlst(4),
                          center=Window.center)

        self.txtinp = TextInput()
        button = Button(text='regen')
        button.bind(on_press=self.clickButton)
        bxlay = BoxLayout(orientation='vertical')
        bxlay.add_widget(self.txtinp)
        bxlay.add_widget(button)
        bxlay.add_widget(self.randLabel)
       
        return Top()

if __name__=='__main__':
    Window.size = 475,300
    game = GameApp()
    game.run()
