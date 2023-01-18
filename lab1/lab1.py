import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import sys

def objekt(v_lista,f_lista, translacija, rotacija):
    glPushMatrix()
    #print(translacija)
    #print(rotacija)
    glTranslate(translacija[0], translacija[1], translacija[2])
    glRotatef(rotacija[1],rotacija[0][0],rotacija[0][1],rotacija[0][2])
    glBegin(GL_TRIANGLES)
    glColor3fv((0.5, 0.5, 0.5))
    for k in range (len(f_lista)):
        for j in range(3):
            glVertex3fv(v_lista[f_lista[k][j]-1])
    glEnd()
    glPopMatrix()


def linija(translacijska_lista):
    glPushMatrix()
    glBegin(GL_LINES)
    glColor3fv((22, 3, 0))
    for k in range(len(translacijska_lista) - 1):
        glVertex3fv(translacijska_lista[k])
        glVertex3fv(translacijska_lista[k+1])
    glEnd()
    glPopMatrix()


def tangenta(tocka1, tocka2):
    faktor=1.5
    glPushMatrix()
    glColor3fv((0,100,1))
    glBegin(GL_LINES)
    for k in range(len(tocka1)):
        glVertex3fv(tocka1[k])
        glVertex3fv(tocka1[k]+tocka2[k]*faktor)
    glEnd()
    glPopMatrix()


def main():
    # citanje
    #print("ime filea:")
    filename = str(sys.argv[1])
    f = open(filename, "r")
    input = f.readlines()
    v_lista=[]
    f_lista=[]
    for line in input:
        if line[0]=="v":
            tmp=line.split()[1:]
            tmp2=[]
            for k in tmp:
                tmp2.append(float(k))
            v_lista.append(tmp2)
        elif line[0]=="f":
            tmp = line.split()[1:]
            tmp2 = []
            for k in tmp:
                tmp2.append(int(k))
            f_lista.append(tmp2)

    B=1/6*np.array([[-1,3,-3,1],
       [3,-6,3,0],
       [-3,0,3,0],
       [1,4,1,0]])
    B_crtano=1/2*np.array([[-1,3,-3,1],
              [2,-4,2,0],
              [-1,0,1,0]])
    v1=[0,0,0]
    v2 = [0, 10, 5]
    v3 = [10, 10, 10]
    v4 = [10, 0, 15]
    v5 = [0, 0, 20]
    v6 = [0, 10, 25]
    v7 = [10, 10, 30]
    v8 = [10, 0, 35]
    v9 = [0, 0, 40]
    v10 = [0, 10, 45]
    v11= [10, 10, 50]
    v12 = [10, 0, 55]
    kontrolne=[v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12]
    B_crtano=np.array(B_crtano)
    B=np.array(B)
    kontrolne=np.array(kontrolne)
    tocke = []
    rotacijska_lista = []
    putanja_lista = []
    ciljna_orijentacija_lista = []
    for k in range(9):
        tocka1=kontrolne[k]
        tocka2=kontrolne[k+1]
        tocka3=kontrolne[k+2]
        tocka4=kontrolne[k+3]
        tocke=[tocka1,tocka2,tocka3,tocka4]
        t=0
        korak=0.01
        s=[0,0,1] #pocetni vektor
        e=[] #zeljena orijentacija
        s=np.array(s)
        while (t<1):
            ciljna_orijentacija=np.dot(np.array([t*t*t,t*t,t,1]),np.dot(B,tocke))
            #print(orijentacija)
            putanja=np.dot(np.array([t*t,t,1]),np.dot(B_crtano,tocke))
            #vektor_os=np.cross(s,ciljna_orijentacija)
            kut=np.arccos(np.dot(s,ciljna_orijentacija)/(np.linalg.norm(s)*np.linalg.norm(ciljna_orijentacija)))
            e=putanja
            #print(s)
            #print(e)
            os_rotacije = np.array([[s[1]*e[2]-e[1]*s[2]],[-(s[0]*e[2]-e[0]*s[2])],[s[0]*e[1]-s[1]*e[0]]])
            rotacijska_lista.append((os_rotacije,(kut*57.2957795)))
            putanja_lista.append(putanja)
            ciljna_orijentacija_lista.append(ciljna_orijentacija)
            t+=korak
            s=ciljna_orijentacija+putanja

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)

    glTranslatef(0,0,-90)
    n=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        linija(ciljna_orijentacija_lista)
        #tangenta(ciljna_orijentacija_lista, putanja_lista)
        objekt(v_lista, f_lista, ciljna_orijentacija_lista[n], rotacijska_lista[n])
        pygame.display.flip()
        pygame.time.wait(10)
        n+=1
        n=n%len(putanja_lista)


main()