import numpy as np


class Parameters:
    def __init__(self):
        """
        Class which holds all parameters to govern the simulation.
        """

        self.box_dimensions = np.array([8.5, 5, 3])     # The dimensions of the box (x, y, z).

        self.field_vector = np.array([2000, 0, 0])      # The vector of the field.
        self.charge = 1                                 # The charge of one needle

        self.factor = 1                                 # Prefactor of the potential => mue/(4*pi)
        self.kT = 1                                     # k * Temperature

        self.cpu_improve = True         # Stores all sphere positions fpr HS-Potential instead of recalculating them.

        self.multiple_dipoles = False                   # Turn to true if every sphere should be a dipole (buggy)

        self.convergence_interval_length = 20           # The interval where it checks the standard deviation
        self.convergence_threshold = 0.05               # Convergence threshold in % (standard deviation / mean)

        self.length = 2                                 # The length of the needles.
        self.width = 0.0892                             # The width of the needles.
        self.quantity = 15                              # The number of needles in the system.

    def calculate_needle_dimensions(self):
        """
        Calculates the dimension of one needle.

        Returns:
            - x - The number of spheres to one side of the middle sphere
            - r - The radius of the spheres
        """

        tmp_l = int(((self.length / self.width) - 1) / 2)
        return tmp_l, self.width / 2

    def get_log_str(self):
        """
        Creates a log-string with most of the important parameters.

        :returns: log-sting.
        """

        msg = "\nParameters Log\n"
        msg += "-------------------------------\n"
        msg += "Box Dimension:\t{box}\n".format(box=self.box_dimensions)
        msg += "Field:\t\t{field}\n".format(field=self.field_vector)
        msg += "Potential:\t{charge}\n".format(charge=self.charge)
        msg += "Width:\t\t{width}\n".format(width=self.width)
        msg += "Length:\t\t{length}\n".format(length=self.length)
        msg += "Quantity:\t{quantity}\n".format(quantity=self.quantity)
        msg += "kT:\t\t{kt} \n\n".format(kt=self.kT)
        msg += "Target SD:\t\t{TSD}\n".format(TSD=self.convergence_threshold)
        msg += "Convergence Interval:\t{CI}\n".format(CI=self.convergence_interval_length)
        msg += "-------------------------------\n"

        return msg
