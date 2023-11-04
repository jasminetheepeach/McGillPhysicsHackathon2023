import argparse
import numpy
from argparse import ArgumentParser
from gooey import Gooey
from PIL import Image

@Gooey
def main():
    parser = ArgumentParser(prog = "LensingSimulator", description = 'Puts an image through the gravitational lensing of an inputted mass') 
    parser.add_argument('image_file', type = argparse.FileType("r"), help = "Image File to be Lensed")
    parser.add_argument('image_size', type = float, help = "Scale to change size of Image")
    parser.add_argument('mass', type = float, help = "The Mass of the Lensing Object")
    parser.add_argument('camera_to_mass', type = float, help = "The Distance from the Observer to the Mass")
    parser.add_argument('mass_to_object', type = float, help = "Distance from the Lensing Mass to the Lensed Image")
    parser.add_argument('mass_radius', type = float, help = "The Radius of the Lensing Mass")
    parser.add_argument('-x', '--output_image_size_x', type = int, help = "The X Co-ordinate of the Outputted Image", default = 1920)
    parser.add_argument('-y', '--output_image_size_y', type = int, help = "The Y Co-ordinate of the Outputted Image", default = 1080)

    args = parser.parse_args()
    image = Image.open(args.image_file.name)
    

main()