
# coding: utf-8

# In[16]:

from __future__ import print_function
import gdal
from gdalconst import *
import numpy as np
from scipy.sparse import csr_matrix
from scipy import sparse
import glob
from os import path


# In[2]:

def normalise_raster(ras):
    ras[ras==-9999] = np.nan  # NaN out missing data
    # normalise to [0, 1]
    normras = (ras - np.nanmin(ras)) / np.nanmax(ras)
    return normras

def threshhold_raster(ras, threshold):
    ras = np.nan_to_num(ras)
    ras[ras<threshold] = 0
    return ras

def get_selector_raster(filename, thresh=0.55):
    sel = gdal.Open(filename).ReadAsArray()
    sel = normalise_raster(sel)
    sel = threshhold_raster(sel, thresh)
    return sel


# In[3]:

def get_climate_layers(pathglob):
    cl = glob.glob(pathglob)
    cln = map(path.basename, cl)
    cln = map(lambda x: path.splitext(x)[0], cln)
    return dict(zip(cln, cl))


# In[4]:

cldict = get_climate_layers('Au_ClimLayers/bio*.asc')
selector = get_selector_raster("B.hybridumAu_avg.asc")


# In[5]:




# In[7]:




# In[12]:

layers={}
for cl, clpath in cldict.items():
    layer = gdal.Open(clpath).ReadAsArray().astype(np.float)
    layer *= selector
    layer[layer==0.] = np.nan
    layers[cl] = layer


# In[20]:

spsel = csr_matrix(selector)
x, y, w = sparse.find(spsel)


# In[22]:

with open("outmat.tab", 'w') as ofh:
    # Print header
    header = ['x', 'y', 'maxent_weight', ] + list(sorted(layers.keys()))
    print(*header, sep='\t', file=ofh)
    xs, ys, ws = sparse.find(spsel)
    for x, y, w in zip(xs, ys, ws):
        line = [x, y, w,]
        for cl, layer in sorted(layers.items()):
            line.append(layer[x, y])
        print(*line, sep='\t', file=ofh)
    


# In[ ]:

layer = gdal.Open(clpath).ReadAsArray().astype(np.float)
   layer *= selector
   layer[layer==0.] = np.nan
   sp = csr_matrix(layer)
   print cl, np.nanmean(layer), np.nanstd(layer)
   cl, clpath = list(cldict.items())[0]


# In[ ]:




# 
# # Algorithm
# 
# - Prepare input raster mask
#     - Read in maxent ouput
#     - Normalise to [0, 1]
#     - set NaN or things < threshold to 0
#     
# - prepare dict of matricies
#     
#     
# 
#     
# 

# In[ ]:



