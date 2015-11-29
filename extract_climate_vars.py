#!/usr/bin/env python

# Copyright 2015 Kevin Murray <spam@kdmurray.id.au>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, division
import glob
from os import path
import sys

import gdal
from gdalconst import *

import numpy as np
from scipy.sparse import csr_matrix
from scipy import sparse

import docopt

"""
Extract climate varaibles by maxent probablity rasters

Author: Kevin Murray
License: GNU GPL v3 or later
Requires: gdal, scipy, numpy, docopt
"""

CLI_USAGE = """
USAGE:
    extract_climate_vars.py [options] <selector> <layers> ...

OPTIONS:
    -o OUTFILE      Output file [default: stdout]
    -t THRESHOLD    Minimal maxent probablity to consider [default: 0.55].

<selector> should be a maxent output layer with postion proablities.

<layer> should be a bioclim or similar raster of the exact same size as
<selector>. More than one can be given. The basename of the layer will be used
as the column header in the output matrix.
"""


def normalise_raster(ras):
    ras[ras==-9999] = np.nan  # NaN out missing data
    # normalise to [0, 1]
    normras = (ras - np.nanmin(ras)) / np.nanmax(ras)
    return normras

def threshhold_raster(ras, threshold):
    ras = np.nan_to_num(ras)
    ras[ras<threshold] = 0
    return ras

def get_selector_raster(filename, threshold=0.55):
    sel = gdal.Open(filename).ReadAsArray()
    sel = normalise_raster(sel)
    sel = threshhold_raster(sel, threshold)
    return sel


def read_climate_layers(layers):
    cln = map(path.basename, layers)
    cln = map(lambda x: path.splitext(x)[0], cln)
    return dict(zip(cln, layers))

def get_weighted_layers(layers, selector):
    weighted_layers={}
    for cl, clpath in layers.items():
        layer = gdal.Open(clpath).ReadAsArray().astype(np.float)
        layer *= selector
        layer[layer==0.] = np.nan
        weighted_layers[cl] = layer
    return weighted_layers


def main(layers, selector, outfile, threshold=0.55):
    print("Reading climate layers", file=sys.stderr)
    layers = read_climate_layers(layers)
    print("Reading selector raster", file=sys.stderr)
    selector = get_selector_raster(selector, threshold=threshold)
    print("Calculating weighted climate layers", file=sys.stderr)
    layers = get_weighted_layers(layers, selector)

    if outfile == 'stdout':
        ofh = sys.stdout
    else:
        ofh = open(outfile, 'w')

    print("Writing output matrix", file=sys.stderr)
    header = ['x', 'y', 'maxent_weight', ] + list(sorted(layers.keys()))
    print(*header, sep='\t', file=ofh)
    xs, ys, ws = sparse.find(csr_matrix(selector))
    for x, y, w in zip(xs, ys, ws):
        line = [x, y, w,]
        for cl, layer in sorted(layers.items()):
            line.append(layer[x, y])
        print(*line, sep='\t', file=ofh)

    ofh.close()
    print("Done!", file=sys.stderr)


if __name__ == "__main__":
    opts = docopt.docopt(CLI_USAGE)
    layers = opts['<layers>']
    selector = opts['<selector>']
    outfile = opts['-o']
    threshold = float(opts['-t'])

    main(layers, selector, outfile, threshold)
