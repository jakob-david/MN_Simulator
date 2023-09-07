from classes.Needle import Needle
from classes.Needles import Needles

import random
import numpy as np
import os
import imageio.v2 as imageio
import shutil


class Simulation:

    def __init__(self, p, gv):
        """
        Class that governs the simulation of the system.

        :param p: The parameters that govern the simulation. (class Parameters)
        :param gv: Saves all relevant parameters throughout the simulations. (class GlobalValues)
        """

        self.p = p
        self.gv = gv
        self.needles = Needles(p)

        gv.E_tot = self.needles.calc_total_energy(self.gv, self.p.field_vector, self.p.factor, self.p.multiple_dipoles,
                                                  self.p.cpu_improve)

    def simulate(self, telegram, use_for_gif=False):
        """
        Simulates the system.

        :param telegram: A telegram object in order to be able to send Telegram images.
        :param use_for_gif: Set to true if a gif should be generated.
        """

        if use_for_gif:
            if not os.path.exists("./gif"):
                os.makedirs("./gif")

        i = 0
        self.gv.start_timer()
        while True:
            print("step: " + str(i + 1))
            if self.next_step():
                print(" New total energy: " + str(self.gv.E_tot))
                self.gv.append_energies()
                self.gv.add_step(i + 1)

                if use_for_gif:
                    self.needles.plot_grid(i+1)

            # Check convergence
            self.gv.add_ci_step()
            self.gv.append_mean_magnetic_potential_x(self.needles.get_mean_magnetic_potential())

            if self.gv.ci_step >= self.p.convergence_interval_length:
                self.gv.calculate_ci_parameters()
                if self.gv.ci_stddev_norm <= self.p.convergence_threshold:

                    self.gv.stop_timer()

                    msg = self.gv.get_str_ci_parameter_converged()
                    print(msg)

                    if telegram is not False:
                        telegram.set_message(msg)
                        telegram.send_message()

                    break

                else:
                    msg = self.gv.get_str_ci_parameter_not_converged()
                    print(msg)
                    self.gv.set_ci_step_to_zero()

            i += 1

        if use_for_gif:
            self.gif()

    def next_step(self):
        """
        Performs one step during the simulations.
        """

        index = random.randint(0, len(self.needles.get()) - 1)
        old_needle = self.needles.get().pop(index)

        x = old_needle.pos_x
        y = old_needle.pos_y
        z = old_needle.pos_z
        r = old_needle.radius
        tmp_l = old_needle.length
        charge = old_needle.charge

        theta, phi = get_random_parameters()

        new_needle = Needle(x, y, z, theta, phi, r, tmp_l, charge)

        if self.p.cpu_improve:
            data_x, data_y, data_z = new_needle.get_coordinate()
            new_needle.data_x = data_x
            new_needle.data_y = data_y
            new_needle.data_z = data_z

        if not new_needle.check_overlap(self.needles.get(), self.p.cpu_improve):
            self.needles.append(old_needle)
            return False
        else:
            self.needles.append(new_needle)

        e_tot_new = self.needles.calc_total_energy(self.gv, self.p.field_vector, self.p.factor, self.p.multiple_dipoles,
                                                   self.p.cpu_improve)

        if e_tot_new < self.gv.E_tot:
            self.gv.E_tot = e_tot_new
            return True

        d_e = self.gv.E_tot - e_tot_new

        if np.exp(d_e / self.p.kT) >= random.random():
            self.gv.E_tot = e_tot_new

            return True
        else:
            self.needles.get().pop(len(self.needles.get()) - 1)
            self.needles.append(old_needle)
            return False

    def gif(self):
        """
        Generates a gif of the simulations over time and saves it as simulation.gif.
        """

        images = list()
        for i in self.gv.steps_array:
            images.append(imageio.imread("gif/picture_for_giv_" + str(i) + ".png"))
        imageio.mimsave("simulation.gif", images)

        shutil.rmtree("./gif")


def get_random_parameters():
    """
    Generates random parameters for a new needle orientation.
    """

    phi = np.random.random() * 2. * np.pi
    cos_theta = 2 * np.random.random() - 1

    return np.arccos(cos_theta), phi
