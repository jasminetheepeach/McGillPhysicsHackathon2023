import argparse
import numpy
from argparse import ArgumentParser
from gooey import Gooey

@Gooey
def main():
    parser = ArgumentParser(prog = "LensingSimulator", description = 'Puts an image through the gravitational lensing of an inputted mass') 
    parser.add_argument('image_file', type = argparse.FileType("r"), help = "Image File to be Lensed")
    parser.add_argument('image_size', type = float, help = "Scale to change size of Image")
    parser.add_argument('mass', type = float, help = "The Mass of the Lensing Object")
    parser.add_argument('camera_to_mass', type = float, help = "The Distance from the Observer to the Mass")
    parser.add_argument('mass_to_object', type = float, help = "Distance from the Lensing Mass to the Lensed Image")
    parser.add_argument('mass_radius', type = float, help = "The Radius of the Lensing Mass")
    args = parser.parse_args()
    print(args.image_file)

main()