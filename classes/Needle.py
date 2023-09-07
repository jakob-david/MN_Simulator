import numpy as np
import math


class Needle:
    def __init__(self, pos_x, pos_y, pos_z, theta, phi, radius, length, charge):
        """
        Class to represent one needle. Each needle consists of linear aligned sphere.

        :param pos_x: The x position of the middle sphere.
        :param pos_y: The y position of the middle sphere.
        :param pos_z: The z position of the middle sphere.
        :param theta: The angle theta of the needle in radians.
        :param phi: The angle phi of the needle in radians.
        :param radius: The radius of each sphere.
        :param length: The length of the needle.
        :param charge: The charge of the needle.
        """

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z

        self.theta = theta
        self.phi = phi
        self.radius = radius
        self.length = length

        self.charge = charge

        # needed for CPU.improve
        self.data_x = []    # The x position for all spheres.
        self.data_y = []    # The y position for all spheres.
        self.data_z = []    # The z position for all spheres.

    def check_overlap(self, needles, cpu_improve):
        """
        Checks if two needles overlap.

        :param needles: The needle with which this needle is checked for overlapping.
        :param cpu_improve: Stores all sphere positions fpr HS-Potential instead of recalculating them.

        :return: True if there is no overlap.
        """

        if cpu_improve:
            x1, y1, z1 = get_coordinate_from_memory(self)
        else:
            x1, y1, z1 = self.get_coordinate()

        r1 = self.radius
        # *2 because of the definition of the data model and +1 because of the sphere in the middle
        l1 = (self.length * 2) + 1

        for i in range(0, len(needles)):  # Loop over all needles

            if cpu_improve:
                x2, y2, z2 = get_coordinate_from_memory(needles[i])
            else:
                x2, y2, z2 = needles[i].get_coordinate

            r2 = needles[i].radius
            l2 = (needles[i].length * 2) + 1
            for m in range(0, l1):  # Loop over all spheres in the "new" needle
                for n in range(0, l2):  # Loop over all spheres of the "old" needle

                    distance = np.linalg.norm(np.array([x1[m] - x2[n], y1[m] - y2[n], z1[m] - z2[n]]))
                    if distance <= r2 + r1:
                        return False

        return True

    def calc_dd_potential(self, other_needle, factor, multiple_dipoles, cpu_improve):
        """
        Calculates the dipole-dipole potential

        :param other_needle: The needle for which the potential is calculated.
        :param factor: Prefactor of the potential [mue/(4*pi)]
        :param multiple_dipoles: Turn to true if every sphere should be a dipole.
        :param cpu_improve: Stores all sphere positions for HS-Potential instead of recalculating them.

        :return: The potential between the two needles.
        """

        if not multiple_dipoles:  # possible improvement
            # Get parameter for the first needle
            x, y, z = self.polar2cart(self.charge)
            m1 = np.array([x, y, z])
            p1 = np.array([self.pos_x, self.pos_y, self.pos_z])

            # Get parameter for the second needle
            x, y, z = other_needle.polar2cart(other_needle.charge)
            m2 = np.array([x, y, z])
            p2 = np.array([other_needle.pos_x, other_needle.pos_y, other_needle.pos_z])

            r = p1 - p2
            r_norm = np.linalg.norm(r)

            return factor * ((np.dot(m1, m2) / r_norm ** 3) - 3 * ((np.dot(m1, r) * np.dot(m2, r)) / r_norm ** 5))

        else:

            if cpu_improve:  # possible improvement
                x1, y1, z1 = get_coordinate_from_memory(self)
                x2, y2, z2 = get_coordinate_from_memory(other_needle)
            else:
                x1, y1, z1 = self.get_coordinate()
                x2, y2, z2 = other_needle.get_coordinate()

            my_sum = 0

            for i in range(0, len(x1)):
                x, y, z = self.polar2cart(self.charge)
                m1 = np.array([x, y, z])
                p1 = np.array([x1[i], y1[i], z1[i]])
                for j in range(0, len(x2)):
                    x, y, z = other_needle.polar2cart(other_needle.charge)
                    m2 = np.array([x, y, z])
                    p2 = np.array([x2[j], y2[j], z2[j]])

                    r = p1 - p2
                    r_norm = np.linalg.norm(r)

                    my_sum += factor * (
                                (np.dot(m1, m2) / r_norm ** 3) - 3 * ((np.dot(m1, r) * np.dot(m2, r)) / r_norm ** 5))

            return my_sum

    def calc_field_potential(self, field_vector):
        """
        Calculates the potential of the field with the needles.

        :param field_vector: The field vector.

        :return: The potential of the field.
        """

        needle = self
        x, y, z = needle.polar2cart(needle.charge)
        n = np.array([x, y, z])
        return np.dot(n, field_vector)

    def get_coordinate(self):
        """
        Gets the coordinate of all spheres of one needle.

        Returns:
            - x - x-coordinate of the middle sphere.
            - y - y-coordinate of the middle sphere.
            - z - z-coordinate of the middle sphere.
        """

        needle = self

        data_x = []
        data_y = []
        data_z = []

        data_x.append(needle.pos_x)
        data_y.append(needle.pos_y)
        data_z.append(needle.pos_z)

        for i in range(1, needle.length + 1):
            x, y, z = needle.polar2cart(needle.radius * i * 2)
            data_x.append(x + needle.pos_x)
            data_y.append(y + needle.pos_y)
            data_z.append(z + needle.pos_z)

            x, y, z = needle.polar2cart(needle.radius * -i * 2)
            data_x.append(x + needle.pos_x)
            data_y.append(y + needle.pos_y)
            data_z.append(z + needle.pos_z)

        return data_x, data_y, data_z

    def polar2cart(self, r):
        """
        Returns the cartesian coordinates of the middle sphere.

        :param r: The length of the vector.

        :return: The cartesian coordinates of the middle sphere. (array)
        """

        theta = self.theta
        phi = self.phi

        return [
            r * math.sin(theta) * math.cos(phi),
            r * math.sin(theta) * math.sin(phi),
            r * math.cos(theta)
        ]


def get_coordinate_from_memory(needle):
    """
    Gets the coordinate of all spheres of one needle for memory.

    Returns:
            - x - x-coordinate of the middle sphere.
            - y - y-coordinate of the middle sphere.
            - z - z-coordinate of the middle sphere.
    """

    return needle.data_x, needle.data_y, needle.data_z
