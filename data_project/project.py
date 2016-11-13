import matplotlib.pyplot as plt
import numpy as np
import pdb
from astropy.io import fits
import glob

def get_header(fls):
    header = []
    for f in fls:
        x = fits.open(f)
        header.append(x[0].header)
        x.close()
    return header

def get_data(fls):
    data = []
    for f in fls:
        x = fits.open(f)
        data.append(x[0].data)
        x.close()
    return data

''' Make data cube '''
fls = glob.glob('../data/*.fits')
d = np.array(get_data(fls))
h = get_header(fls)

''' Pull dimensions, time series, etc. '''
dim = d.shape[1]
images = d.shape[0]
cadence = 12.
time_h = (np.arange(images)*cadence)/60. # time [hours]
time_m = (np.arange(images)*cadence) # time [minutes]

''' Indices for potential flares '''
th = 4500.
flare = np.where(d > th)
i = flare[1]
j = flare[2]
k = flare[0]

def background():
    ''' images '''
    fig = plt.figure()
    plt.imshow(np.power(d[0], 0.5), cmap = 'gray')
    plt.axis('off')
    plt.savefig('background.png',bbox_inches='tight')

def flare():
    ''' flare! '''
    fig = plt.figure()
    im = np.abs(d[k[0]])
    plt.imshow(np.power(im, 0.5), cmap = 'gray')
    plt.axis('off')
    #plt.savefig('flare.png',bbox_inches='tight')

blah = flare()

def make_movie():
    ''' attempt to make a movie (fail) '''
    my_movie = d[(i[0]-7):(i[0]+7)]
    for a in range(0,len(my_movie)):
        plt.imshow(np.power(my_movie[a],0.5),cmap='gray')
        #plt.savefig('movie' + str(a+1) + '.png')
    return my_movie

def single():
    ''' Single plot for extracting flare begin/end times '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ts = (d[:,i[0],j[0]])
    ax.plot(np.arange(0,images), ts/np.max(ts))
    ax.tick_params(labelsize='small')
    x1=4100
    x2=4200
    ax.set_xbound(lower=x1,upper=x2)
    ax.set_ybound(lower=-0.1,upper=1.1)
    ax.set_xticks(np.arange(x1,x2,10))
    ax.set_xlabel('time [minutes]',size='small')
    ax.set_ylabel('intensity [arbitrary]',size='small')
    ax.set_title('Pixel at [' + str(j[0]) + ',' + str(k[0]) + ']')
    plt.show()

def candidates():
    ''' Lots of plots for potential flare candidates '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    for a in range(0,len(i)):
        ts = (d[:,i[a],j[a]])
        ax.plot(time_h, ((ts/np.max(d)) + a))
        x.append(10)
        y.append(len(i)-0.8)
        ax.text(0.1, a+0.8, '[' + str(i[a]) + ',' + str(j[a]) + ']')
    ax.set_ylim(-0.1,len(i))
    ax.tick_params(labelsize='small')
    ax.set_xticks(np.arange(time_h[0],time_h[-1],20))
    ax.ticklabel_format(style='sci')
    ax.set_xlabel('time [hours] since ' + str(h[0]['DATE-OBS']),size='small')
    ax.set_ylabel('intensity [arbitrary]',size='small')
    ax.set_title('Flare candidates')
    #plt.show()
    plt.savefig('fig1.png')
