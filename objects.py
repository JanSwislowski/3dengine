import pygame
import math
from settings import *
class Camera:
    def __init__(self, position,camera_width,camera_height,camera_distance,camera_speed=5, camera_angle_speed=3):
        self.position = position
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.camera_distance = camera_distance
        self.surface= pygame.Surface((camera_width, camera_height))
        self.camera_speed= camera_speed
        self.angle_x = 0
        self.angle_y = 0
        self.camera_angle_speed = camera_angle_speed
        self.fov_x = math.atan(camera_width/camera_distance)
        self.fov_y= math.atan(camera_height/camera_distance)
    def refresh(self):
        self.surface.fill((0, 0, 0))
    def rotate_point(self, point):
        # Rotate point around the camera's position
        x = point[0] - self.position[0]
        y = point[1] - self.position[1]
        z = point[2] - self.position[2]

        # Apply rotation around the Y-axis (yaw)
        x_rotated = x * math.cos(self.angle_x) - z * math.sin(self.angle_x)
        z_rotated = x * math.sin(self.angle_x) + z * math.cos(self.angle_x)

        # Apply rotation around the X-axis (pitch)
        y_rotated = y * math.cos(self.angle_y) - z_rotated * math.sin(self.angle_y)
        z_rotated = y * math.sin(self.angle_y) + z_rotated * math.cos(self.angle_y)

        return (x_rotated, y_rotated, z_rotated)
    def blit_point(self, point):

        relative_position_x, relative_position_y, relative_position_z = self.rotate_point(point)
        if relative_position_z <= 0:
            return None

        x= self.camera_width//2 + relative_position_x * self.camera_distance / relative_position_z
        y= self.camera_height//2 + relative_position_y * self.camera_distance / relative_position_z

        return (x*screen_width/self.camera_width, y*screen_height/self.camera_height)

    def draw(self, screen,screen_width,screen_height):
        screen.blit(pygame.transform.scale(self.surface, (screen_width, screen_height)), (0, 0))

    def handle_input(self, keys):
        if keys[pygame.K_w]:
            #-math.sin(self.angle_xz)*self.camera_speed, -math.sin(self.angle_yz)*self.camera_speed
            vx=math.sin(self.angle_x)*self.camera_speed
            vy=math.sin(self.angle_y)*self.camera_speed
            vz=self.camera_speed
            self.move((0,0,vz))
            print(vx,vy,vz)
        if keys[pygame.K_s]:
            vx=math.sin(self.angle_x)*self.camera_speed
            vy=math.sin(self.angle_y)*self.camera_speed
            vz=(self.camera_speed)
            self.move((0,0,-vz))
            print(self.position)
        if keys[pygame.K_d]:
            vx=self.camera_speed
            self.move((vx,0,0))
        if keys[pygame.K_a]:
            vx=self.camera_speed
            self.move((-vx,0,0))
        if keys[pygame.K_q]:
            self.move((0,-self.camera_speed,0))
        if keys[pygame.K_e]:
            self.move((0,self.camera_speed,0))
        # if keys[pygame.K_w]:
        #     self.move((0, -self.camera_speed, 0))
        # if keys[pygame.K_s]:
        #     self.move((0, self.camera_speed, 0))
    def angles_delta(self,angle_1,angle_2):
        delta=angle_1-angle_2
        if delta>math.pi:
            delta-=math.pi*2
        if delta<-math.pi:
            delta+=math.pi*2
        return delta
    def handle_mouse(self, mouse_pos,screen_width,screen_height):
        self.angle_x=(mouse_pos[0]-screen_width//2)/(screen_width//2)*math.pi*2*self.camera_angle_speed
        self.angle_y=(mouse_pos[1]-screen_height//2)/(screen_height//2)*math.pi*2*self.camera_angle_speed
        self.angle_x%= math.pi*2
        self.angle_y%= math.pi*2
        #print(math.degrees(self.angle_x),math.degrees(self.angle_y))
    def move(self, delta_position):
        self.position = (self.position[0] + delta_position[0],self.position[1] + delta_position[1],self.position[2] + delta_position[2])
class edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.color = (255, 255, 255)
    def draw(self, camera, screen):
        start_pos = camera.blit_point(self.start)
        end_pos = camera.blit_point(self.end)
        if start_pos and end_pos:
            pygame.draw.line(screen, self.color, start_pos, end_pos,2)

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
        self.edges = [
            edge(self.points[0], self.points[1]),
            edge(self.points[1], self.points[2]),
            edge(self.points[2], self.points[3]),
            edge(self.points[3], self.points[0]),
            edge(self.points[4], self.points[5]),
            edge(self.points[5], self.points[6]),
            edge(self.points[6], self.points[7]),
            edge(self.points[7], self.points[4]),
            edge(self.points[0], self.points[4]),
            edge(self.points[1], self.points[5]),
            edge(self.points[2], self.points[6]),
            edge(self.points[3], self.points[7])
        ]
    def draw(self, camera,screen):
        for edge in self.edges:
            edge.draw(camera, screen)