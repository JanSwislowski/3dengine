import pygame
from objects import *
from settings import *
if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hello World")

    camera=Camera((0, 0, 0), camera_screen_width, camera_screen_height, camera_distance,camera_speed, camera_angle_speed)
    Cubes = [Cube((0, 0, 100),20),]
    point=(0, 0, 100)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        mouse_position=pygame.mouse.get_pos()
        camera.handle_input(keys)
        camera.handle_mouse(mouse_position,screen_width,screen_height)
        camera.refresh()
        for i in Cubes:
            i.draw(camera,screen)
        a=camera.blit_point(point)
        if a:
            pygame.draw.circle(screen,(255,0,0), a,5)
        # camera.draw(screen, screen_width, screen_height)
        pygame.display.flip()
    pygame.quit()