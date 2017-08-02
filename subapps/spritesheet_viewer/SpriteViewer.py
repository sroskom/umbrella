from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock


class Sprite(Widget):
    def __init__(self,texture,*args,**kwargs):
        super(Sprite,self).__init__(*args,**kwargs)
        self.texture = texture
        self.texture.mag_filter = 'nearest'
        spriteHeight = Window.height/2
        aspectRatio = spriteHeight/float(self.texture.size[1])
        spriteWidth = self.texture.size[0]*aspectRatio
        
        self.size = spriteWidth,spriteHeight
        with self.canvas:
            self.rect = Rectangle(texture=self.texture, size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        
        
class SpriteAtlas:
    @staticmethod
    def getSpriteListFromAtlas(source,sqs):
        #sqs = 'square size'
        atlas = Image(source='images\spritesheet_viewer\\'+source).texture
        atlas.mag_filter = 'nearest'
        regions_x = atlas.width/sqs
        regions_y = atlas.height/sqs
        spriteList = []
        for i in range(0,regions_y):
            for b in range(0,regions_x):
                coords = b*sqs,i*sqs,sqs,sqs
                region = atlas.get_region(coords[0],coords[1],coords[2],coords[3])
                spriteList.append(Sprite(region))       
        return spriteList

class SpriteCarousel(Carousel):
    def __init__(self,imgdir,*args):
        super(SpriteCarousel,self).__init__()
        print('caro wid pos:',self.pos)
        spriteList = SpriteAtlas.getSpriteListFromAtlas(imgdir,16)
        for i in spriteList:
            self.add_widget(i)

    def next(self,*args):
        self.load_next()

class SpriteStepAnimator(Widget):
    def __init__(self,imgdir,*args):
        super(SpriteStepAnimator,self).__init__()
        self.spriteList = SpriteAtlas.getSpriteListFromAtlas(imgdir,16)
        self.currentSpriteIndex = 0
        self.currentSprite = self.spriteList[self.currentSpriteIndex]
        self.currentSprite.x = self.x = Window.width/2
        self.add_widget(self.currentSprite)

    def animate(self, *args):
        if self.currentSpriteIndex + 1 >= len(self.spriteList):
            self.currentSpriteIndex = 0
        else:
            self.currentSpriteIndex += 1
        self.remove_widget(self.currentSprite)
        self.currentSprite = self.spriteList[self.currentSpriteIndex]
        self.currentSprite.pos = self.pos
        self.add_widget(self.currentSprite)
        
    def on_touch_down(self, touch, *args):
        super(SpriteStepAnimator,self).on_touch_down(touch)
        if self.collide_point(touch.x,touch.y):
            self.animate()
            
            
            
class SpriteAnimator(Widget):           
    def __init__(self,imgdir,*args):
        super(SpriteAnimator,self).__init__()
        self.spriteList = SpriteAtlas.getSpriteListFromAtlas(imgdir,16)
        self.currentSpriteIndex = 0
        self.currentSprite = self.spriteList[self.currentSpriteIndex]
        self.currentSprite.x = self.x = Window.width/2
        self.add_widget(self.currentSprite)
        Clock.schedule_interval(self.animate,12.0/60.0)
        
    def animate(self, *args):
        if self.currentSpriteIndex + 1 >= len(self.spriteList):
            self.currentSpriteIndex = 0
        else:
            self.currentSpriteIndex += 1
        self.remove_widget(self.currentSprite)
        self.currentSprite = self.spriteList[self.currentSpriteIndex]
        self.currentSprite.pos = self.pos
        self.add_widget(self.currentSprite)
        
class Manager(ScreenManager):
    def __init__(self, *args):
        super(Manager,self).__init__(*args)

        txtFontSiz = 50
        caroBtn = Button(text='carousel', font_size=txtFontSiz)
        caroBtn.background_color=[0,0,0,1]
        animBtn = Button(text='animate', font_size=txtFontSiz)
        animBtn.background_color=[0,0,0,1]
        
        bxlay = BoxLayout()
        
        bxlayOps = BoxLayout(orientation='vertical')
        bxlayOps.add_widget(caroBtn)
        bxlayOps.add_widget(animBtn)

        bxlayViews = BoxLayout(orientation='vertical')
        spriteCarousel = SpriteCarousel(imgdir='images\spritesheet_viewer\Old hero.png')
        caroBtn.bind(on_press=spriteCarousel.next)
        spriteCarousel.loop = True
        bxlayViews.add_widget(spriteCarousel)
        spriteAnimator = SpriteStepAnimator(imgdir='images\spritesheet_viewer\Old hero.png')
        animBtn.bind(on_press=spriteAnimator.animate)
        bxlayViews.add_widget(spriteAnimator)

        bxlay.add_widget(bxlayOps)
        bxlay.add_widget(bxlayViews)

        mainMenu = Screen()
        mainMenu.name = 'menu'
        mainMenu.add_widget(bxlay)
        self.add_widget(mainMenu)


class PixelImageApp(App):
    def build(self, *args):
        return Manager()

if __name__ == '__main__':
    PixelImageApp().run()
