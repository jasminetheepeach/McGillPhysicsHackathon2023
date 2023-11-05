import numpy

class Photon:
    def __init__(self, position, velocity, time_step):
        self.position = position
        self.velocity = velocity
        self.time_step = time_step
        self.hit = False

    def step(self, mass: float, mass_position):
        # acceleration = (m  / distance squared) * unit vector pointing towards the mass
        # acceleration = (m  / ||p1 - p0|| ^ 2                                      ) * (p1 - p0) / ||p1 - p0||
        acceleration = (mass / numpy.linalg.norm(mass_position - self.position) ** 2) * ((mass_position - self.position) / numpy.linalg.norm(mass_position - self.position))
        self.velocity += acceleration * self.time_step
        self.position += self.velocity * self.time_step

    def __str__(self):
        return f"Position: {self.position}, Velocity: {self.velocity}"