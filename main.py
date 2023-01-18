from simulation import Simulation

# The number of buses can be changed to any number
number_of_buses = 4

# Initialize simulation object and run it 
simulate = Simulation(nr_buses=number_of_buses)
simulate.run()

# Print the simulation results
print(f'\nResults with {number_of_buses} buses:\n')
print(f'{simulate.simulation_results}\n')