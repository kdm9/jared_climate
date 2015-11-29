# Climate Variable Extraction and Coordinate Calculation Script
# Authors __________ and Jared Streich
# Version 1.0.0

############################################# Import Python Things #############################################
from python import python things

####################################### Set Values for Analysis Pipeline #######################################

# Minimum Prediction Percent by Maxent to be a numerator
MinPredNumer = 0.55

# Largest Value in Data Matrix to be a denominator
PredDenom = 254

# Minimum Reported Data value in Input_Matrix.txt File that is calculated as significant
MinPred = MinPredNumer/PredDenom


######################################### Set Used Files to Variables #########################################

# An output file (heatmap of geographic predictions) from Maxent that shows probability of species occurrence, converted to a text file before this script is run.
Input_Matrix = open("/directory/to/input_matrix.txt", "r")

# A file to be produced and written to composed of extracted climate variables and matrix coordinates of the locations above a predicted threshold
Output_Matrix = open("/directory/to/output_matrix.txt/", "w")

# Ideal structure for "Output_Matrix.txt" by column (separated by tab), location number simply starts at 1. Column header can be file name for BioClim arrays
# Location Number(1-n)   Input_Matrix Row    Input_Matrix Column    Actual Longitude    Actual Latitude    Bio1Value   ----->   Bio19Value  Bio1Value*InputVariable_Bias.txt  ------>   Bio19Value*InputVariable_Bias.txt 

# Actual Sample Coordinates

# A bias file to multiply the extracted variables that come from the Maxent Run. This will be created before running this script
Input_Variable_Bias_File = open("/directory/to/Input_Variable_Bias_File.txt", "w")


# Directory to where the Climate Raster layers are stored
Climate_Directory = (/directory/to/raw/climate/layers/)



################################################ Start Script ################################################

## Get row and column position of cell above

while step ==0:
  for row in Input_Matrix:
    for i in row:
        if i >= MinPred:
            index(i) = Ind
            Output_Matrix.write( a number )            ## Location number, but starts at 1 and ends when all predicted locations are entered, not a specific number, the naming of each data point starts here
            Output_Matrix.write(Ind)                   ## Write row and column position to Output_Matrix.txt columns 2 and 3
        else:
            step = 1:

## Get values in each BioClim climate matrix based on the Index Coordinates (Rows and Columns) position in step 0
 while step ==1:
    for *.txt in Climate_Directory:
        for row in *.txt:            ## Each of 19 different equally sized matrices I'm extracting climate values from (climate layer raster files converted to text files)
            -some command here-:     ## Use the index from columns 2 and 3 of Output_Matrix.txt to extract from each climate layer.txt and write that value to a further right column in Output_matrix.txt
            i[row] in *.txt:
                Output_Matrix.write(columns 6 to 25)  ## Columns 6-25 because of 19 bioclim variables. Will be increased to more variables later, 40-50 variables are expected in the sort of near future.
                step = 2:

## Take the extracted Bioclim Values in Columns 6 - 25 and Multiply them by the bias values in Input_Variable_Bias_File.txt, composed of decimal numbers to reduce values to their contribution to species distribution
 while step ==2:
    for i in columns 6-25 in output_matrix.txt
        for j in colums 1 - 19 in Input_Variable_Bias_File
            i * j = BiasVar
                Output_Matrix.write(BiasVar columns 26 - 45) ##


