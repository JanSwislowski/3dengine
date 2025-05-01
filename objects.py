import pygame
import math
class Camera:
    def __init__(self, position,camera_width,camera_height,camera_distance,camera_speed=5, camera_angle_speed=0.1):
        self.position = position
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.camera_distance = camera_distance
        self.surface= pygame.Surface((camera_width, camera_height))
        self.camera_speed= camera_speed
        self.angle_xz = 0
        self.angle_yz = 0
        self.camera_angle_speed = camera_angle_speed
    def refresh(self):
        self.surface.fill((0, 0, 0))
    def blit_point(self, point):
        relative_position_x = point[0] - self.position[0]
        relative_position_y = point[1] - self.position[1]
        relative_position_z= point[2] - self.position[2]

        x= self.camera_width//2 + relative_position_x * self.camera_distance / relative_position_z
        y= self.camera_height//2 + relative_position_y * self.camera_distance / relative_position_z

        pygame.draw.circle(self.surface, (255, 0, 0), (x, y), 2)

    def draw(self, screen,screen_width,screen_height):
        screen.blit(pygame.transform.scale(self.surface, (screen_width, screen_height)), (0, 0))
    def handle_input(self, keys):
        if keys[pygame.K_w]:
            self.move((math.sin(self.angle_xz)*self.camera_speed, 0, math.cos(self.angle_xz)*self.camera_speed))
        if keys[pygame.K_s]:
            self.move((math.sin(self.angle_yz-math.pi)*self.camera_speed, 0, math.cos(self.angle_yz-math.pi)*self.camera_speed))
        # if keys[pygame.K_w]:
        #     self.move((0, -self.camera_speed, 0))
        # if keys[pygame.K_s]:
        #     self.move((0, self.camera_speed, 0))
    def handle_mouse(self, mouse_pos,screen_width,screen_height):
        self.angle_xz=(mouse_pos[0]-screen_width//2)/(screen_width//2)*math.pi*2*self.camera_angle_speed
        self.angle_yz=(mouse_pos[1]-screen_height//2)/(screen_height//2)*math.pi*2*self.camera_angle_speed
    def move(self, delta_position):
        self.position = (self.position[0] + delta_position[0],self.position[1] + delta_position[1],self.position[2] + delta_position[2])

class Cube:
    def __init__(self, position,edge_length=50):
        self.position = position
        self.size = edge_length
        self.color = (255, 0, 0)
        self.points = [
            (self.position[0] - self.size / 2, self.position[1] - self.size / 2, self.position[2] - self.size / 2),
            (self.position[0] + self.size / 2, self.position[1] - self.size / 2, self.position[2] - self.size / 2),
            (self.position[0] + self.size / 2, self.position[1] + self.size / 2, self.position[2] - self.size / 2),
            (self.position[0] - self.size / 2, self.position[1] + self.size / 2, self.position[2] - self.size / 2),
            (self.position[0] - self.size / 2, self.position[1] - self.size / 2, self.position[2] + self.size / 2),
            (self.position[0] + self.size / 2, self.position[1] - self.size / 2, self.position[2] + self.size / 2),
            (self.position[0] + self.size / 2, self.position[1] + self.size / 2, self.position[2] + self.size / 2),
            (self.position[0] - self.size / 2, self.position[1] + self.size / 2, self.position[2] + self.size / 2)
        ]
    def draw(self, camera):
        for point in self.points:
            camera.blit_point(point)