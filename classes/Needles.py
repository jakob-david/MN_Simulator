import random
import numpy as np
import matplotlib.pyplot as plt

from classes.Needle import Needle


class Needles:

    def __init__(self, p):
        """
        Class that represents all needles of the system. Saved in an array.

        :param p: The parameters of the system (class: Parameters)
        """

        self.needles = []   # The array that holds all needles.
        self.p = p

        calc_length, calc_radius = p.calculate_needle_dimensions()

        tmp_l = calc_radius * 2 * calc_length

        for i in range(0, p.quantity):
            print("Placed needle nr.: " + str(i + 1))
            while True:  # Loop as long as it needs till a random position of a needle is accepted.
                x = random.uniform(tmp_l, p.box_dimensions[0] - tmp_l)
                y = random.uniform(tmp_l, p.box_dimensions[1] - tmp_l)
                z = random.uniform(tmp_l, p.box_dimensions[2] - tmp_l)

                theta, phi = get_random_parameters()

                # Here the length of each needle can also be randomised
                needle = Needle(x, y, z, theta, phi, calc_radius, calc_length, p.charge)

                if p.cpu_improve:  # Could also be before the if statement
                    data_x, data_y, data_z = needle.get_coordinate()
                    needle.data_x = data_x
                    needle.data_y = data_y
                    needle.data_z = data_z

                if needle.check_overlap(self.needles, p.cpu_improve):
                    self.needles.append(needle)
                    break

    def get(self):
        """
        Gets the needles array.

        :return: array of needles.
        """

        return self.needles

    def get_by_id(self, idx):
        """
        Gets one needle of the array by its id.

        :param idx: The id of the needle.

        :return: The needle with that id.
        """

        return self.needles[idx]

    def append(self, needle):
        """
        Appends one needle to the array of needles.

        :param needle: The needle to be appended.
        """

        self.needles.append(needle)

    def calc_total_energy(self, gv, field_vector, factor, multiple_dipoles, cpu_improve):
        """
        Calculates the total energy of the current state of the system.

        :param gv: The global variables (class: GlobalVariables)
        :param field_vector: The vector of the field.
        :param factor: Prefactor of the potential [mue/(4*pi)]
        :param multiple_dipoles: Turn to true if every sphere should be a dipole.
        :param cpu_improve: Stores all sphere positions fpr HS-Potential instead of recalculating them.

        :return: Total energy of the system.
        """

        sum_field = 0
        sum_dd = 0

        for i in range(0, len(self.needles)):
            for j in range(i, len(self.needles)):
                if i == j:
                    continue
                # sum += calc_potential(needles[i], needles[j], factor)
                sum_dd += self.get_by_id(i).calc_dd_potential(self.get_by_id(j), factor, multiple_dipoles, cpu_improve)
            sum_field += self.get_by_id(i).calc_field_potential(field_vector)

        gv.E_F = sum_field
        gv.E_DD = sum_dd
        return sum_dd + sum_field

    def get_mean_magnetic_potential(self):
        """
        Gets the mean magnetic potential.\n
        Comment: not really compatible with "multiple" dipoles per needle

        :return: mean magnetic potential.
        """

        my_sum = 0
        for needle in self.needles:
            x, y, z = needle.polar2cart(needle.charge)
            my_sum += x

        return my_sum / len(self.needles)

    def get_coordinates(self):
        """
        Gets all coordinates for every sphere.

        :return: All sphere coordinates.
        """

        data_x = []
        data_y = []
        data_z = []

        for needle in self.needles:

            tmp_x, tmp_y, tmp_z = needle.get_coordinate()

            data_x.append(tmp_x)
            data_y.append(tmp_y)
            data_z.append(tmp_z)

        return data_x, data_y, data_z

    def get_coordinates_from_memory(self):
        """
        Gets all coordinates for every sphere from memory.

        :return: All sphere coordinates.
        """

        data_x = []
        data_y = []
        data_z = []

        for needle in self.needles:
            data_x.append(needle.data_x)
            data_y.append(needle.data_y)
            data_z.append(needle.data_z)
        return data_x, data_y, data_z

    def plot_grid(self, use_for_gif=False):
        """
        Plots all needles in a 3D grid.

        :param use_for_gif: Turn to true in order to save the plots to generate a gif later on.
        """

        if self.p.cpu_improve:
            data_x, data_y, data_z = self.get_coordinates_from_memory()
        else:
            data_x, data_y, data_z = self.get_coordinates()

        fig = plt.figure(figsize=(15, 10))  # control plot size
        ax = plt.axes(projection='3d')
        ax.set_xlim3d(0, self.p.box_dimensions[0])
        ax.set_ylim3d(0, self.p.box_dimensions[1])
        ax.set_zlim3d(0, self.p.box_dimensions[2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.scatter3D(data_x, data_y, data_z, c=data_z)

        if use_for_gif:
            plt.savefig("./gif/picture_for_giv_" + str(use_for_gif) + ".png")
        else:
            plt.show()

        plt.close(fig)


def get_random_parameters():
    """
    Gets random parameters for a needle.

    :return: random needle parameters.
    """

    phi = np.random.random() * 2. * np.pi
    cos_theta = 2 * np.random.random() - 1

    return np.arccos(cos_theta), phi
