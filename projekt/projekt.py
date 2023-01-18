import numpy as np
import sys
from copy import deepcopy
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import argparse

WIDTH=1
HEIGHT=2

def bubble_sort(list):

   for iter_num in range(len(list)-1,0,-1):
      for idx in range(iter_num):
         if list[idx]>list[idx+1]:
            temp = list[idx]
            list[idx] = list[idx+1]
            list[idx+1] = temp
            yield list

def merge_sort(list, start, end):
    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1

    yield from merge_sort(list, start, mid)
    yield from merge_sort(list, mid + 1, end)
    yield from merge(list, start, mid, end)
    yield list



def merge(list, start, mid, end):
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if list[leftIdx] < list[rightIdx]:
            merged.append(list[leftIdx])
            leftIdx += 1
        else:
            merged.append(list[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(list[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(list[rightIdx])
        rightIdx += 1

    for i in range(len(merged)):
        list[start + i] = merged[i]
        yield list



def insertion_sort(input_list):
   yield input_list
   for i in range(1, len(input_list)):
      j = i-1
      nxt_element = input_list[i]

      while (input_list[j] > nxt_element) and (j >= 0):

          input_list[j+1] = input_list[j]
          j=j-1
          yield input_list
      input_list[j+1] = nxt_element
      yield input_list


def shell_sort(input_list):
   yield input_list
   gap = len(input_list) // 2
   while gap > 0:
      for i in range(gap, len(input_list)):
         temp = input_list[i]
         j = i

         while j >= gap and input_list[j - gap] > temp:
            input_list[j] = input_list[j - gap]
            j = j-gap
            input_list[j] = temp
            for k in range(3):
                yield input_list

      gap = gap//2
   yield input_list

def quick_sort(input_list, l, r):
	if l >= r:
		return
	x = input_list[l]
	j = l
	for i in range(l + 1, r + 1):
		if input_list[i] <= x:
			j += 1
			input_list[j], input_list[i] = input_list[i], input_list[j]
		yield input_list
	temp=input_list[l]

	input_list[l]=input_list[j]
	input_list[j]=temp

	yield from quick_sort(input_list, l, j-1)
	yield from quick_sort(input_list, j + 1, r)
	yield input_list
def selection_sort(input_list):
    yield input_list
    for i in range(len(input_list)):
        yield input_list

        min_idx = i
        yield input_list
        for j in range(i + 1, len(input_list)):
            if input_list[min_idx] > input_list[j]:
                min_idx = j
        temp=input_list[i]
        input_list[i]=input_list[min_idx]
        input_list[min_idx]=temp
        for k in range(8): #dodano radi realnosti mjerenja vremena
            yield input_list
        yield input_list



def animate(list,bars,iter,text,start):
    for k in range(len(bars)):
        if (bars[k].get_height()!=list[k]):
            bars[k].set_color("red")
        else:
            bars[k].set_color("blue")
        bars[k].set_height(list[k])
    iter[0]+=1
    text.set_text(("Time :"+str(round((time.perf_counter()-start),5))))


def main():
    list = []
    if (".txt" in sys.argv[1]):
        filename=sys.argv[1]
        f = open(str(filename), "r")
        input = f.readlines()
        for line in input:
            list.append(int(line))
    else:
        list = np.arange(int(sys.argv[1]))
        np.random.shuffle(list)
        list = list.tolist()



    start = time.perf_counter()
    if (sys.argv[2]=="compare"):
        generator = []
        generator.append(bubble_sort(deepcopy(list)))

        generator.append(merge_sort(deepcopy(list), 0, len(list) - 1))

        generator.append(insertion_sort(deepcopy(list)))
        generator.append(shell_sort(deepcopy(list)))
        generator.append(quick_sort(deepcopy(list), 0, len(list) - 1))
        generator.append(selection_sort(deepcopy(list)))
        fig, ax = plt.subplots(3, 2, figsize=(15, 15))
        names = ["Bubble sort", "Merge sort", "Insertion sort", "Shell sort", "Quick sort", "Selection sort"]
        animation = []
        for row in range(3):
            for col in range(2):
                bars = ax[row, col].bar(range(len(list)), list, align="edge", color="blue")
                text = ax[row, col].text(0.01, 0.95, "", transform=ax[row, col].transAxes)
                ax[row, col].set_title("ALGORITAM:" + names[col + row * 2])
                ax[row, col].axis("off")
                iter = [0]
                animation.append(
                    FuncAnimation(fig, func=animate, fargs=(bars, iter, text, start), frames=generator[col + row * 2],
                                  interval=0, repeat=False))

        plt.rcParams["figure.figsize"] = (20, 3)
        plt.show()
        return
    algo = sys.argv[2]
    if (algo=="bubble_sort"):
        generator=bubble_sort(deepcopy(list))
    elif(algo=="merge_sort"):
        generator=merge_sort(deepcopy(list),0,len(list)-1)
    elif(algo=="insertion_sort"):
        generator=insertion_sort(deepcopy(list))
    elif (algo=="shell_sort"):
        generator=shell_sort(deepcopy(list))
    elif(algo=="quick_sort"):
        generator=quick_sort(deepcopy(list),0,len(list)-1)
    elif (algo == "selection_sort"):
        generator = selection_sort(deepcopy(list))
    else:
        print("Unknown algorithm")
        return
    fig, ax = plt.subplots()
    bars=ax.bar(range(len(list)),list,align="edge",color="blue")
    text = ax.text(0.01, 0.95, "", transform=ax.transAxes)
    ax.set_title("ALGORITAM:"+algo)
    ax.axis("off")
    iter=[0]
    anim = FuncAnimation(fig, func=animate,fargs=(bars, iter,text,start), frames=generator,
                         interval=0,repeat=False)
    plt.rcParams["figure.figsize"] = (20, 3)
    plt.show()



main()
