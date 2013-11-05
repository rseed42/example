# Self-made recursion-based walk function that allows us to
# filter out unwanted subdirectories in a natural manner
import os
# Do not use trailing slashes for subdirectories!
#TOP_DIR = os.path.expanduser('~/Tmp/topdir')
TOP_DIR = os.path.expanduser('/usr/bin')
EXCL_LIST = ['s01/q01/r01', 's02', 's03', 's04', 's06']
for i in xrange(len(EXCL_LIST)):
    EXCL_LIST[i] = TOP_DIR + '/' + EXCL_LIST[i]
#-------------------------------------------------------------------------------
# ident is passed by value
def recwalk(pardir, excl_list, ident):
#    print ident, pardir
    # Check if the parent directory is not on the exclusion list first and
    # abort the recursion if necessary
    # Check exclusions before proceeding.
    i = 0
    while i < len(excl_list):
        excl_path = excl_list[i]
#        print ident, '->', excl_path
        if excl_path.startswith(pardir):
            diff = excl_path[len(pardir):]
#            print ident, 'diff:', diff
            # We are in an excluded directory
            if not diff:
                 return
            i += 1
        else:
            del excl_list[i]
#            print ident, 'del'

    for sub in os.listdir(pardir):
        path = pardir + '/' + sub
        if os.path.isdir(path):
            # Need to copy the exclusion list since it is passed by reference
            if os.path.islink(path):
                continue
            recwalk(path, excl_list[:], ident+'    ')
        elif os.path.isfile(path):
            print path

#-------------------------------------------------------------------------------
recwalk(TOP_DIR, EXCL_LIST, '')
