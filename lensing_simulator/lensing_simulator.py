import argparse
import math
import numpy
from Photon import Photon
from argparse import ArgumentParser
from gooey import Gooey
from PIL import Image

@Gooey
def main():
    # Arguments
    parser = ArgumentParser(prog = "LensingSimulator", description = 'Puts an image through the gravitational lensing of an inputted mass') 
    parser.add_argument('image_file', type = argparse.FileType("r"), help = "Image File to be Lensed")
    parser.add_argument('image_size', type = float, help = "Scale to change size of Image")
    parser.add_argument('mass', type = float, help = "The Mass of the Lensing Object")
    parser.add_argument('camera_to_mass', type = float, help = "The Distance from the Observer to the Mass")
    parser.add_argument('mass_to_object', type = float, help = "Distance from the Lensing Mass to the Lensed Image")
    parser.add_argument('mass_radius', type = float, help = "The Radius of the Lensing Mass")
    parser.add_argument('-x', '--output_image_size_x', type = int, help = "The X Co-ordinate of the Outputted Image", default = 1920)
    parser.add_argument('-y', '--output_image_size_y', type = int, help = "The Y Co-ordinate of the Outputted Image", default = 1080)
    parser.add_argument('-t', '--time_step', type = float, help = "The time step", default = 0.01)
    parser.add_argument('-f', '--field_of_view', type = float, help = "The horizontal angle viewed", default = 135)
    parser.add_argument('-p', '--near_clipping_place_distance', type = float, help = "The distance to the near clipping place", default = 1)

    args = parser.parse_args()

    # Extract arguments
    image = Image.open(args.image_file.name)
    image_scale = args.image_size
    image_distance = args.camera_to_mass + args.mass_to_object
    mass = args.mass
    radius = args.radius
    mass_position = numpy.array([0, 0, args.camera_to_mass])
    fov = args.field_of_view
    x = args.output_image_size_x
    y = args.output_image_size_y
    output = Image.new("RGB", (x, y))
    near_clipping_plane_distance = args.near_clipping_place_distance
    time_step = args.time_step

    # Rat Tracing ???????
    # Create rays
    rays = list()
    plane_horizontal_length = 2 * near_clipping_plane_distance * math.tan(math.radians(fov / 2))
    plane_vertical_length = plane_horizontal_length * y / x
    for i in range(0, x):
        rays[i] = list()
        y_position = plane_vertical_length * ((i / x) - 0.5)
        for j in range(0, y):
            x_position = plane_horizontal_length * ((j / y) - 0.5)
            direction = numpy.array([x_position, y_position, near_clipping_plane_distance])
            rays[i][j] = Photon(direction, direction / numpy.linalg.norm(direction), time_step)
    
main()