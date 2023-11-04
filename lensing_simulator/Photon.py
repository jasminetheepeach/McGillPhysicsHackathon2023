import numpy

class Photon:
    G = 6.6743e-11

    def __init__(self, position, velocity, time_step):
        self.position = position
        self.velocity = velocity
        self.time_step = time_step
        self.hit = False

    def step(self, mass: float, mass_position):
        # acceleration = (Photon.G * mass) / numpy.linalg.norm(self.position - mass_position) ** 2
        acceleration = 0
        self.velocity += acceleration * self.time_step
        self.position += self.velocity * self.time_step

    def __str__(self):
        return f"Position: {self.position}, Velocity: {self.velocity}"