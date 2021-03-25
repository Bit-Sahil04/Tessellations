# Requires pygame==2.0

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # hide pygame greeting
import pygame
import pygame.locals
import random
import argparse


def get_10print_mask(res, args):
    xoff, yoff = (0, 0)

    size = args.size
    density = args.density
    thickness = args.thickness
    inverted = args.inverted
    Lbias = args.Lbias

    drawLine = True
    color = (255, 255, 255)

    surf = pygame.Surface(res)
    surf.fill((0, 0, 0))

    while drawLine:
        if random.randint(0, 1 + Lbias):
            pygame.draw.line(surf, color,
                             (0 + xoff, 0 + yoff), (size + xoff, size + yoff), thickness)
        else:
            pygame.draw.line(surf, color,
                             (0 + xoff, size + yoff), (size + xoff, 0 + yoff), thickness)

        xoff += size / density
        if xoff > res[0]:
            yoff += size / density
            xoff = 0
        if yoff > res[1]:
            drawLine = False

    # Creating a mask for our surface
    surf.set_colorkey((0, 0, 0))
    masksurf = pygame.mask.from_surface(surf)
    if inverted:
        masksurf.invert()

    return masksurf.to_surface()


def main(img_path, args):
    pygame.init()
    pygame.display.set_caption("10Print Filter - Bit Sahil04")
    imgsurface = pygame.image.load(img_path)
    width, height = imgsurface.get_size()
    win = pygame.display.set_mode((width, height))
    surfmask = get_10print_mask((width, height), args)
    imgsurface.blit(surfmask, (0, 0), special_flags=pygame.locals.BLEND_RGB_MIN)
    win.blit(imgsurface, (0, 0))
    clock = pygame.time.Clock()

    if not args.no_save:
        pygame.image.save(win, f"output--{img_path}")

    while not args.no_preview:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                exit()

        clock.tick(10)
        pygame.display.flip()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='10-Print Image Filter by Bit-Sahil04')
    parser.add_argument("-size", help="Size of strokes default=10", default=10, type=int)
    parser.add_argument("-density", help="density of strokes default=1", default=1, type=float)
    parser.add_argument("-thickness", help="width of strokes default=1", default=1, type=int)
    parser.add_argument("--inverted", help="Invert Mask", action="store_true")
    parser.add_argument("-Lbias", help="Bias left-to-right stroke probability", default=1, type=int)

    parser.add_argument("--no-save", help="Disable Saving", action="store_true")
    parser.add_argument("--no-preview", help="Disable Preview", action="store_true")
    parser.add_argument("path", help="Path of the Image")
    args = parser.parse_args()
    main(args.path, args)
