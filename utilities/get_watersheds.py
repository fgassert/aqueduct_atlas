'''

'''

import os
import urllib2
import pandas as pd
from multiprocessing import Pool

# working directory for files if different than where the script is
WORKING_DIRECTORY = "watersheds/"
# location of csv with latitude and longitude coordinates
LATLNG_CSV = "dam_locations.csv"

# field names for the ObjectID, Latitude, and Logitude in the csv
INDEX_FIELD = "OBJECT_ID"
LAT_FIELD = "lat"
LNG_FIELD = "long"

# additional parameters
SNAP_DISTANCE = 0.0083333 # decimal degrees
FORMAT = 'zip'

def downloader(args):
    try:
        # set up the file name to be the index and the format
        out = '%s.%s' % (args['idx'], args['f'])
        # make sure the file doesn't already exist
        if not os.path.exists(out):
            # set up the url
            u = "http://api.fgassert.com/?loc=%s,%s&d=%s&f=%s&force" % (
                args['lng'],args['lat'],args['d'],args['f'])

            # open the output file location
            with open(out,'wb') as f:
                # download the data from the url
                r = urllib2.urlopen(u)
                # and write it to file
                f.write(r.read())

    # catch and print out any errors rather than crashing
    except Exception as e:
        print e

def main(latlng_csv):
    os.chdir(WORKING_DIRECTORY)
    # read the csv into a dataframe
    df = pd.read_csv(latlng_csv)

    paramlist = []
    # set up the parameters for each of the files to be downloaded
    for i in range(df.shape[0]):
        paramlist.append( {'idx':df[INDEX_FIELD][i],
                'lat':df[LAT_FIELD][i],
                'lng':df[LNG_FIELD][i],
                'd':SNAP_DISTANCE,
                'f':FORMAT} )
   
    # rather than just downloading one at a time,
    # download up to 4 at a time: 
    # the function worker() is called on each set of parameters in paramlist
    #p = Pool(processes=1)
    result = map(downloader, paramlist)
    print result
    print "complete"

if __name__ == '__main__':
    # this is run when you run the script
    main(LATLNG_CSV)
