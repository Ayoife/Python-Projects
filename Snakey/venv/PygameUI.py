import pygame
from pygame.locals import *


class Button:

    def __init__(self, text, rect, fill=True, border=False, **kwargs):
        """Creates a pygame button"""
        self.rect = rect
        self.text = text
        self.fill = fill
        self.name = "consolas"
        self.border = border
        self.textsize = 20
        self.onclick = None
        self.onhover = None
        self.bold = True
        self.italic = False
        self.textcolor = (0, 0, 0)
        self.fillcolor = (255, 255, 255)
        self.hovercolor = (255, 255, 255)
        self.padx, self.pady = 0, 0
        self.mousex, self.mousey = 0, 0

        for k in kwargs:
            if k == 'border':
                self.border = kwargs[k]
            if k == 'onclick':
                self.onclick = kwargs[k]
            if k == 'onhover':
                self.onhover = kwargs[k]
            if k == 'textcolor':
                self.textcolor = pygame.Color(kwargs[k])
            if k == 'textsize':
                self.textsize = kwargs[k]
            if k == 'fillcolor':
                self.fillcolor = kwargs[k]
                self.hovercolor = kwargs[k]
            if k == 'hovercolor':
                self.hovercolor = kwargs[k]
            if k == 'font':
                self.name, self.bold, self.italic = kwargs[k]
            if k == 'padding':
                self.padx, self.pady = kwargs[k]
            
        self.color = self.fillcolor
        self.Font = pygame.font.SysFont(self.name, self.textsize, self.bold, self.italic)
        self.buttonRect = pygame.Rect(self.rect)

    def display(self, displaySurf, events):
        textSurf = self.Font.render(self.text, True, self.textcolor, None)
        textRect = textSurf.get_rect()
        if textRect.size > self.buttonRect.size:
            textSurf = pygame.transform.smoothscale(textSurf, self.buttonRect.size)
            textRect = textSurf.get_rect()
        textRect.topleft = (self.buttonRect.left+self.padx, self.buttonRect.top+self.pady)
        if self.fill: pygame.draw.rect(displaySurf, self.color, self.buttonRect)
        if self.border: pygame.draw.rect(displaySurf, self.border[0], self.buttonRect, self.border[1])
        displaySurf.blit(textSurf, textRect)

        for event in events:
            if event.type == MOUSEBUTTONUP:
                self.mousex, self.mousey = event.pos
                if self.buttonRect.collidepoint(self.mousex, self.mousey):
                    if self.onclick is not None: self.onclick()
            if event.type == MOUSEMOTION:
                self.mousex, self.mousey = event.pos
                
        if self.buttonRect.collidepoint(self.mousex, self.mousey):
            self.color = self.hovercolor
            if self.onhover is not None: self.onhover()
        else:
            self.color = self.fillcolor

class Text:
    
    def __init__(self, text, color, left, top, bold=False, italic=False, underline=False, bgcolor=None, font=("Helvetica",20), anchor='center'):
        """Creates a pygame text"""
        self.text = text
        self.color = color
        self.bgcolor = bgcolor
        self.bold = bold
        self.anchor = anchor
        self.underline = underline
        self.italic = italic
        self.left, self.top = left, top
        self.font = pygame.font.SysFont(font[0], font[1], bold, italic)

    def display(self, displaySurf):
        self.font.set_underline(self.underline)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        textSurf = self.font.render(self.text, True, self.color, self.bgcolor)
        textRect = textSurf.get_rect()
        
        if self.anchor == 'center':
            textRect.center = (self.left, self.top)
        if self.anchor == 'bottom':
            textRect.bottom = (self.left, self.top)
        if self.anchor == 'bottomleft':
            textRect.bottomleft = (self.left, self.top)
        if self.anchor == 'bottomright':
            textRect.bottomright = (self.left, self.top)
        if self.anchor == 'midbottom':
            textRect.midbottom = (self.left, self.top)
        if self.anchor == 'midright':
            textRect.midright = (self.left, self.top)
        if self.anchor == 'midleft':
            textRect.midleft = (self.left, self.top)
        if self.anchor == 'midright':
            textRect.midright = (self.left, self.top)
        if self.anchor == 'midtop':
            textRect.midtop = (self.left, self.top)
        if self.anchor == 'topleft':
            textRect.topleft = (self.left, self.top)
        if self.anchor == 'topright':
            textRect.topright = (self.left, self.top)
            
        displaySurf.blit(textSurf, textRect)

class Slider:

    def __init__(self, left, top, color, size=25, minvalue=0, maxvalue=100, shape="circle"):
        """Creates a functional slider"""
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.value = maxvalue
        self.shape = shape
        self.color = color
        self.size = size
        self.left = left
        self.top = top
        self.mouseIsDragged = False

    def display(self, display, events):
        pygame.draw.line(display, pygame.Color("BLACK"), (self.left, self.top), (self.left+self.maxvalue,self.top), 3)
        if self.shape == "rect":
            knobRect = pygame.Rect(self.left, self.top, self.size, self.size)
            knobRect.center = (self.left+self.value, self.top)
            pygame.draw.rect(display, self.color, knobRect)
        else:
            knobRect = pygame.draw.circle(display, self.color, (self.left+self.value, self.top), int(self.size/2))

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.mouseIsDragged = True
            if event.type == MOUSEBUTTONUP:
                self.mouseIsDragged = False
            if event.type == MOUSEMOTION and self.mouseIsDragged:
                if knobRect.collidepoint(event.pos):
                    self.value = ((min(self.left+self.maxvalue, max(self.left+self.minvalue, event.pos[0])))-self.left)+self.minvalue
        return self.value
        
