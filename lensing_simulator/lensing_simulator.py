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
    parser.add_argument('image_file', type = argparse.FileType("r"), help = "Image file to be lensed (.jpg)")
    parser.add_argument('output_file', type = argparse.FileType("w"), help = "Name of the image file that will be output (no file extension)")
    parser.add_argument('image_size', type = float, help = "Horizontal size of the image", default = 4)
    parser.add_argument('mass', type = float, help = "The mass of the lensing object")
    parser.add_argument('camera_to_mass', type = float, help = "Distance from the observer to the mass")
    parser.add_argument('mass_to_object', type = float, help = "Distance from the mass to the image")
    parser.add_argument('mass_radius', type = float, help = "The radius of the lensing mass")
    parser.add_argument('-mx', '--mass_x', type = float, help = "The X co-ordinate of the mass", default = 0)
    parser.add_argument('-my', '--mass_y', type = float, help = "The Y co-ordinate of the mass", default = 0)
    parser.add_argument('-x', '--output_image_size_x', type = int, help = "The X co-ordinate of the outputted image", default = 500)
    parser.add_argument('-y', '--output_image_size_y', type = int, help = "The Y co-ordinate of the outputted image", default = 500)
    parser.add_argument('-t', '--time_step', type = float, help = "The time step. Lower value results in a more accurate simulation but longer time taken.", default = 0.01)
    parser.add_argument('-l', '--time_step_limit', type = float, help = "The limit of the number of time steps allowed to occur", default = 1000)
    parser.add_argument('-f', '--field_of_view', type = float, help = "The horizontal angle viewed", default = 135)
    parser.add_argument('-p', '--near_clipping_plane_distance', type = float, help = "The distance to the near clipping plane", default = 1)

    args = parser.parse_args()

    # Extract arguments
    image = Image.open(args.image_file.name)
    image_size = args.image_size
    image_distance = args.camera_to_mass + args.mass_to_object
    mass = args.mass
    radius = args.mass_radius
    mass_position = numpy.array([args.mass_x, args.mass_y, args.camera_to_mass])
    fov = args.field_of_view
    x = args.output_image_size_x
    y = args.output_image_size_y
    output = Image.new("RGB", (x, y))
    output_file = args.output_file
    near_clipping_plane_distance = args.near_clipping_plane_distance
    time_step = args.time_step
    time_limit = args.time_step_limit

    # Log arguments
    output_file.write('\n'.join(str(args).strip("Namespace()").split(", ")))

    # Calculate length of image
    image_x_length = image_size / 2
    image_y_length = (image.size[1] / image.size[0]) * (image_size / 2)

    # Rat Tracing ???????
    # Generate rays
    rays = list()
    plane_horizontal_length = 2 * near_clipping_plane_distance * math.tan(math.radians(fov / 2))
    plane_vertical_length = plane_horizontal_length * y / x
    print("Step 1: Generating rays")
    for i in range(0, x):
        # Print progress
        if i % (x // 10) == 0:
            print(f"{i * y} / {x * y}")
        # Create list for this row
        rays.append(list())
        # Calculate the height of this row
        y_position = plane_vertical_length * ((i / x) - 0.5)
        for j in range(0, y):
            # Calculate the horizontal position of this column
            x_position = plane_horizontal_length * ((j / y) - 0.5)
            # Create direction of this ray
            direction = numpy.array([x_position, y_position, near_clipping_plane_distance])
            # Instantiate and add to list
            rays[i].append(Photon(direction, direction / numpy.linalg.norm(direction), time_step))
    print("Finished.")

    # Trace rays
    num_hit = 0
    total_rays = x * y
    t = 0
    print("Step 2: Tracing rays")
    while num_hit < total_rays and t < time_limit:
        if t % 5 == 0:
            print(f"{num_hit} / {total_rays}, t={t}")
        for i in range(0, x):
            for j in range(0, y):
                photon = rays[i][j]
                if not photon.hit:
                    photon.step(mass, mass_position)
                    # If the photon has gone further than the image
                    if photon.position[2] >= image_distance:
                        # Determine if the ray is in the bounds of the image
                        hit_x = photon.position[0]
                        hit_y = photon.position[1]
                        if (hit_x < image_x_length and hit_x > -image_x_length) and (hit_y < image_y_length and hit_y > -image_y_length):
                            # Translate from world space coordinates to image space coordinates
                            image_x = int(((hit_x + image_x_length) / (2 * image_x_length)) * image.size[0])
                            image_y = int(((hit_y + image_y_length) / (2 * image_y_length)) * image.size[1])
                            output.putpixel((j, i), image.getpixel((image_x, image_y)))
                        photon.hit = True
                        num_hit += 1
                    # If the photon has collided with the mass
                    if numpy.linalg.norm(photon.position - mass_position) < radius:
                        output.putpixel((j, i), (255, 255, 255))
                        photon.hit = True
                        num_hit += 1
                    # If the photon flew too far off into the space
                    if numpy.linalg.norm(photon.position) > 1.5 * image_distance:
                        photon.hit = True
                        num_hit += 1
        t += 1
    print("Finished.")

    output.save(output_file.name + ".jpg", quality = 95)
    output.show()

main()