from classes.Parameters import Parameters
from classes.GlobalValues import GlobalValues
from classes.Telegram import Telegram
from classes.Simulation import Simulation

start_p = Parameters()
# tele = Telegram()
tele = False

my_sim = Simulation(start_p, GlobalValues(start_p.convergence_interval_length))

my_sim.needles.plot_grid()
my_sim.simulate(tele)
my_sim.needles.plot_grid()

my_sim.gv.plot_total_energy()
my_sim.gv.plot_dd_energy()
my_sim.gv.plot_field_energy()
my_sim.gv.plot_mean_magnetic_potential()
