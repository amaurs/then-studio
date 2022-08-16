import numpy
import scipy
from scipy import ndimage
from scipy.spatial import distance
import random 
import colorsys
import math
import hilbert
w = 10
h = 10

width = 4096
height = 4096



def NN(A, start):
    """Nearest neighbor algorithm.
    A is an NxN array indicating distance between N locations
    start is the index of the starting location
    Returns the path and cost of the found solution
    """
    path = [start]
    cost = 0
    N = A.shape[0]
    mask = numpy.ones(N, dtype=bool)  # boolean values indicating which 
                                   # locations have not been visited
    mask[start] = False

    for i in range(N-1):
        last = path[-1]
        next_ind = numpy.argmin(A[last][mask]) # find minimum of remaining locations
        next_loc = numpy.arange(N)[mask][next_ind] # convert to original location
        path.append(next_loc)
        mask[next_loc] = False
        cost += A[last, next_loc]

    return path, cost

def paint_pixel(image, x, y, colors):
    print "(%s,%s)" % (x,y)
    theStack = [ (x, y) ]
    count = 0
    while len(theStack) > 0:
        
        x, y = theStack.pop()

        if sum(image[x,y]) > 0:
            continue
        print x,y
        image[x,y] = colors[count]
        count = count + 1
        if x > 0 and y> 0 and x < width - 1 and y < height - 1:
            theStack.append((x + random.randint(0, 1), y + random.randint(0, 1) ))  # right
            theStack.append((x + random.randint(0, 1), y - random.randint(0, 1))) # left
            theStack.append((x , y + 1 ))  # down
            theStack.append( (x - random.randint(0, 1) , y - random.randint(0, 1)) )  


def getRGBfromI(RGBint):
    Blue =  RGBint & 255
    Green = (RGBint >> 8) & 255
    Red =   (RGBint >> 16) & 255
    return (Red,Green,Blue)

def step (r,g,b, repetitions=1):
    lum = math.sqrt( .241 * r + .691 * g + .068 * b )
 
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
 
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)
 
    return (h2, lum, v2)

def order_by_hue():
    colours = []
    colours_final = []
    for number in range(width*height):
        rgb = getRGBfromI(number)
        colours.append(rgb)
    #colours.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb) )
    colours.sort(key=lambda (r,g,b): step(r,g,b,8)  )
    return colours

def order_tsp():
    colours = []
    for number in range(1,width*height):
        rgb = getRGBfromI(number)
        colours.append(rgb)

    colours_length = width*height
    A = numpy.zeros([colours_length,colours_length])
    for x in range(0, colours_length-1):
        for y in range(0, colours_length-1):
            A[x,y] = distance.euclidean(colours[x],colours[y])
 
    # Nearest neighbour algorithm
    path, _ = NN(A, 0)
 
    # Final array
    colours_nn = []
    for i in path:
        colours_nn.append(  colours[i]  )

    return colours_nn
def order_hilbert():
    colours = []
    for number in range(1,width*height):
        rgb = getRGBfromI(number)
        colours.append(rgb)
    colours.sort(key=lambda (r,g,b):hilbert.Hilbert_to_int([int(r*255),int(g*255),int(b*255)])  )
    return colours

def spiral(N, M):
    x,y = 0,0   
    dx, dy = 0, -1

    for dumb in xrange(N*M):
        if abs(x) == abs(y) and [dx,dy] != [1,0] or x>0 and y == 1-x:  
            dx, dy = -dy, dx            # corner, change direction

        if abs(x)>N/2 or abs(y)>M/2:    # non-square
            dx, dy = -dy, dx            # change direction
            x, y = -y+dx, x+dy          # jump

        yield x, y
        x, y = x+dx, y+dy

def paint_spiral(image,colors):

    order = spiral(height, width)
    print order
    index = 0
    for x,y in order:
        image[x,y] = colors[index]
        index += 1


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint


image_1 = numpy.zeros((height, width, 3))

colors = order_by_hue()
for i in range(100):
    print colors[i]
print len(colors)
#paint_pixel(image_1, random.randint(0, width), random.randint(0, height), colors)
paint_spiral(image_1,colors)

scipy.misc.imsave('spiral.png', image_1)


