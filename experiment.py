from model import *
import sys

if __name__=="__main__":
    _, file, iterations = sys.argv
    victoria = GeoVictoria(file)
    
    for i in range(int(iterations)):
        victoria.step()
