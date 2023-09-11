import sys

from PygameUI import *

WINDOWWIDTH = 500
WINDOWHEIGHT = 500

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


def main():
    pygame.init()

    pygame.display.set_caption("Color Picker")
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    r, g, b = 0, 0, 0
    redSlider = Slider(100, 100, RED, maxvalue=255, shape="circle", size=80)
    greenSlider = Slider(100, 200, GREEN, maxvalue=255, shape="circle", size=80)
    blueSlider = Slider(100, 300, BLUE, maxvalue=255, shape="circle", size=80)
    colorText = Text('', BLACK, 250, 400, bold=True, font=("Helvetica", 50))

    while True:
        DISPLAY.fill((r, g, b))
        EVENTS = pygame.event.get()
        colorText.text = f"{r} {g} {b}"
        r = redSlider.display(DISPLAY, EVENTS)
        g = greenSlider.display(DISPLAY, EVENTS)
        b = blueSlider.display(DISPLAY, EVENTS)
        colorText.display(DISPLAY)

        for event in EVENTS:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
