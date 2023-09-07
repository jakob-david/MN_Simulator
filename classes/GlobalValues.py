import math
import statistics
import time
import matplotlib.pyplot as plt


class GlobalValues:
    def __init__(self, ci_length):
        """
        Class that stores all relevant variables generated during the simulation.

        :param ci_length: The interval where it checks the standard deviation.
        """

        # Info:
        # -----------------------------
        # p....convergence interval
        # dd...dipole dipole
        # -----------------------------

        # static variables
        # -----------------------------
        self.ci_length = ci_length          # The length of the interval where it checks the standard deviation.
        # -----------------------------

        # global variables
        # -----------------------------
        self.E_tot = math.inf               # The total energy of the current system.
        self.E_DD = 0                       # The total dipole-dipole potential of the current system.
        self.E_F = 0                        # The total field potential with the needles of the current system.

        self.ci_step = 0                    # The current step with respect to the current convergence interval.
        self.ci_stddev = 0                  # The standard deviation of the last completed convergence interval.
        self.ci_mean = 0                    # The mean of the last completed convergence interval.
        self.ci_stddev_norm = 0             # The (sd / mean) of the last completed convergence interval.

        self.t_start = 0                    # The starting time of the simulation.
        self.t_end = 0                      # The end time of the simulation.
        # -----------------------------

        # global arrays
        # -----------------------------
        self.total_energy_array = []        # Every total energy of the system. (added when change occurs)
        self.dd_energy_array = []           # Every dipole-dipole potential of the system. (added when change occurs)
        self.field_energy_array = []        # Every field potential of the system. (added when change occurs)

        self.convergence_interval = []      # The total energies in the current convergence interval.
        self.mean_magnetic_potential = []   # The mean magnetic potential of every convergence interval.

        self.steps_array = []               # Every step where a new total energy was accepted.
        # -----------------------------

    def append_mean_magnetic_potential_x(self, x):
        """
        Appends a mean magnetic potential to the array.

        :param x: The mean magnetic potential to be added.
        """

        self.mean_magnetic_potential.append(x)

    def append_energies(self):
        """
        Appends to the respective array the:
            - Current total energy of the system.
            - Current dipole-dipole potential.
            - Current field potential with needles.
        """

        self.total_energy_array.append(self.E_tot)
        self.dd_energy_array.append(self.E_DD)
        self.field_energy_array.append(self.E_F)

    def add_step(self, i):
        """
        Adds a step to the step array.

        :param i: The step to be added.
        """

        self.steps_array.append(i)

    def add_ci_step(self):
        """
        Increases the step counter for the convergence interval by 1.
        """

        self.ci_step += 1

    def set_ci_step_to_zero(self):
        """
        Sets the step counter for the convergence interval to zero.
        """

        self.ci_step = 0

    def calculate_ci_parameters(self):
        """
        Calculates all relevant parameters related to the convergence interval.
        """

        self.ci_stddev = statistics.stdev(self.get_ci())
        self.ci_mean = statistics.mean(self.get_ci())
        self.ci_stddev_norm = abs(self.ci_stddev / self.ci_mean)

    def start_timer(self):
        """
        Saves the starting time of simulation. (Must be called)
        """

        self.t_start = time.time()

    def stop_timer(self):
        """
        Saves the end time of simulation. (Must be called)
        """

        self.t_end = time.time()

    def get_ci(self):
        """
        Gets the Convergence interval for the total energy array.

        :return: current convergence interval.
        """

        return self.total_energy_array[-self.ci_length:]

    # Plotting methods
    # -----------------------------
    def plot_total_energy(self):
        """
        Makes a plot of the total energy with respect to time.
        """

        fig = plt.figure(figsize=(15, 10))  # control plot size
        plt.plot(self.steps_array, self.total_energy_array)
        plt.xlabel('number of steps')
        plt.ylabel('energy')
        plt.show()
        plt.close(fig)

    def plot_dd_energy(self):
        """
        Makes a plot of the dipole-dipole potential with respect to time.
        """

        fig = plt.figure(figsize=(15, 10))  # control plot size
        plt.plot(self.steps_array, self.dd_energy_array)
        plt.xlabel('number of steps')
        plt.ylabel('dipole dipole energy')
        plt.show()
        plt.close(fig)

    def plot_field_energy(self):
        """
        Makes a plot of the field energy with respect to time.
        """

        fig = plt.figure(figsize=(15, 10))  # control plot size
        plt.plot(self.steps_array, self.field_energy_array)
        plt.xlabel('number of steps')
        plt.ylabel('field energy')
        plt.show()
        plt.close(fig)

    def plot_mean_magnetic_potential(self):
        """
        Makes a plot of the mean magnetic potential with respect to time.
        """

        tmp_x = []
        for i in range(0, len(self.mean_magnetic_potential)):
            tmp_x.append(i)

        fig = plt.figure(figsize=(15, 10))  # control plot size
        plt.plot(tmp_x, self.mean_magnetic_potential)
        plt.xlabel('number of steps')
        plt.ylabel('mean magnetic potential')
        plt.show()
        plt.close(fig)

    # To String methods
    # -----------------------------
    def get_str_ci_parameter_converged(self):
        """
        Makes a sting with usefully information when the system converged.

        :return: string.
        """

        msg = "\n==============================\n"
        msg += "CONVERGED......\n"
        msg += "Standard Deviation: {sd}\n".format(sd=self.ci_stddev)
        msg += "Mean: {mean}\n".format(mean=self.ci_mean)
        msg += "Standard Deviation / Mean: {sd_mean}\n".format(sd_mean=self.ci_stddev_norm)
        msg += "==============================\n"

        return msg

    def get_str_ci_parameter_not_converged(self):
        """
        Makes a sting with usefully information when the system is not yet converged.

        :return: string.
        """

        msg = "\n-------------------------------\n"
        msg += "NOT converged......\n"
        msg += "Standard Deviation: {sd}\n".format(sd=self.ci_stddev)
        msg += "Mean: {mean}\n".format(mean=self.ci_mean)
        msg += "Standard Deviation / Mean: {sd_mean}\n".format(sd_mean=self.ci_stddev_norm)
        msg += "-------------------------------\n"

        return msg

    def get_log_str(self):
        """
        Makes a log-sting with usefully information.

        :return: log-string.
        """

        msg = "\nGlobal Variables Log\n"
        msg += "-------------------------------\n"
        msg += "Time:\t{time} [s]\n".format(time=self.t_end - self.t_start)
        msg += "Steps:\t{steps}\n".format(steps=self.steps_array[-1])
        msg += "-------------------------------\n"

        return msg
