from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from pyglet import *
from PIL import Image
from collections import deque
import sys
import pygame
from pygame.locals import *




class Emitter():
    def __init__(self):
        self.particles = deque()
        
    def emit_particles(self,n,x):
        for _ in range(n): 
            p = Particle()
            p.pos=np.array([[x, -10.0, 0.0]])
            self.particles.append(p)

    
    def age_particles(self):
        for p in self.particles:
            p.change_age()
        
    def randomize_particles(self):
        particles2 = deque()
        for p in self.particles: 
            if (p.age < p.lifetime):
                p.randomize()
                particles2.append(p)
        self.particles = particles2

class Particle():
    def __init__(self):
        self.pos=np.array([[0.0, -10.0, 0.0]])
        self.v=np.array([0.0, 0.0, 0.0])
        self.age=0
        self.r=2.5
        self.red=np.random.normal(0,20)
        self.green=0.5
        self.blue=0
        self.lifetime =np.random.normal(0.7,0.1)
    def change_age(self):
        self.age += 0.01

    def randomize(self):
        rand_vec = np.array([np.random.normal(0,10), 6.0, 0.0])
        rand_vec = rand_vec / np.linalg.norm(rand_vec)

        t = ((self.lifetime - self.age)/self.lifetime)
        self.v = rand_vec * 0.8 * t
        self.pos = self.pos + self.v
        self.r = (t * 2.5)**1.8

        self.red=self.red+t*(255-self.red)
        if self.green>=0:
            self.green-=0.008



def main():

    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    gluPerspective(45, 1.25, 0.1, 500)
    glTranslatef(0, 0, -50)

    file=sys.argv[1]
    w, h = 256, 256
    image = Image.open(file)
    image = np.array(list(image.getdata()), np.uint8)
    texture = glGenTextures(1)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 1, w, h, GL_RGB, GL_UNSIGNED_BYTE, image)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)

    emitter = Emitter()

    emitter2 = Emitter()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        emitter.emit_particles(5,0)
        emitter.randomize_particles()

        emitter2.emit_particles(5,-20)
        emitter2.randomize_particles()

        glPushMatrix()
        glBegin(GL_QUADS)
        for p in emitter.particles:
            #print(p)
            glColor4d(p.red,p.green,p.blue,0.9)
            glTexCoord2d(0, 0)
            glVertex3f(*(p.pos[0] + np.array([-p.r, -p.r, 0])))
            glTexCoord2d(1, 0)
            glVertex3f(*(p.pos[0] + np.array([p.r, -p.r, 0])))
            glTexCoord2d(1, 1)
            glVertex3f(*(p.pos[0] + np.array([p.r, p.r, 0])))
            glTexCoord2d(0, 1)
            glVertex3f(*(p.pos[0] + np.array([-p.r, p.r, 0])))
        glEnd()
        glPopMatrix()

        emitter.age_particles()

        glPushMatrix()
        glBegin(GL_QUADS)
        for p in emitter2.particles:
            # print(p)
            glColor4d(p.red, p.green, p.blue, 0.9)
            glTexCoord2d(0, 0)
            glVertex3f(*(p.pos[0] + np.array([-p.r, -p.r, 0])))
            glTexCoord2d(1, 0)
            glVertex3f(*(p.pos[0] + np.array([p.r, -p.r, 0])))
            glTexCoord2d(1, 1)
            glVertex3f(*(p.pos[0] + np.array([p.r, p.r, 0])))
            glTexCoord2d(0, 1)
            glVertex3f(*(p.pos[0] + np.array([-p.r, p.r, 0])))
        glEnd()
        glPopMatrix()

        emitter2.age_particles()
        
        pygame.display.flip()
        pygame.time.wait(10)



main()