import sys
import os 
import os.path
from fontTools.ttLib import TTFont
from fontTools.misc.textTools import binary2num, num2binary

# Helper to find files
def getFiles(path, extension):
    if not extension.startswith('.'):
        extension = '.' + extension
    if extension == '.ufo':
        return [dir for (dir, dirs, files) in os.walk(path) if dir[-len(extension):] == extension]
    else:
        return [os.sep.join((dir, file)) for (dir, dirs, files) in os.walk(path) for file in files if file[-len(extension):] == extension]

def setUseTypoMetricsFalse(fontPath, outDirectory):
    # Get Font object from path
    font = TTFont(fontPath)
    
    # Make new pathname to save fixed font
    oldD, f = os.path.split(fontPath)
    new = os.path.join(outDirectory, f)
    
    # Get the OS/2 Table
    os2 = font["OS/2"]
    
    # Make sure that we only fix fonts with an OS/2 table version 
    # that is 4 or greater
    if os2.version >= 4:
        
        # Get the binary representation of fsSelection
        b = num2binary(os2.fsSelection,16)
        
        # Make a new binary representation of fsSelection that sets
        # the Use Typo Metrics bit to false (0)
        nb = b[:9] + '0' + b[10:]
        
        # Give the font the new fsSelection
        os2.fsSelection = binary2num(nb)
        
        # Save font to new path
        font.save(new)
    else:
        print fontPath + " OS/2 table version is less than 4, nothing to fix."
    

def main():
    # make output dir
    d = os.getcwd() + '/fixed'
    try:
        os.makedirs(d)
    except OSError:
        if not os.path.isdir(d):
            raise
    
    # make sure output dir contains no otfs or ttfs
    files = getFiles(d, 'otf')
    files += getFiles(d, 'ttf')
    if len(files) != 0:
        for file in files:
            os.remove(file)
    
    # Get to work
    print "Setting Use Typo Metrics to False"
    print "---------------------------------"
    print "Working from:"
    print os.getcwd()
    files = getFiles(os.getcwd(), 'otf')
    files += getFiles(os.getcwd(), 'ttf')
    print "Found these fonts to fix:"
    print files
    for file in files:
        print "Fixing: " + file
        setUseTypoMetricsFalse(file, d)
    print "---------------------------------"
    print "Done. Fixed files in: " + d


if __name__ == "__main__":
    main()