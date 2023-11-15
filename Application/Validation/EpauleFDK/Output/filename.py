import os

# checks the output file name, if a file with the same name already exists, creates a new file with a number at the end
def name(context, Basename, ext):
    i = 0
    Path = str(Basename[0]) + "." + str(ext[0])
    FileName = str(Basename[0])
    
    while os.path.exists(os.path.join(Path)):
        i += 1
        Path =str(Basename[0]) + "_" + str(i) + "." + str(ext[0])
        FileName = str(Basename[0]) + "_" + str(i)
        
    return FileName