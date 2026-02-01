# Author: Jaey Kim (jaeykimusa.github.io)


from sim_mujoco import WolfMiniSim, SimConfig
from sim_reporter import SimReporter

import numpy as np
import mujoco as mj

SIM_NAME = "Example Run"

def main():
    

    simConfig = SimConfig(
        show_contact_pts=False, 
        show_joint_axes=False, 
        transparent_robot=False,
        )
    
    
    simReporter = SimReporter(simName=SIM_NAME)
    
    mj_sim = WolfMiniSim(simName=SIM_NAME, simConfig=simConfig, simReporter=simReporter)

    # mj_sim.launch_viewer()
    zero_torques = np.zeros(12)
    mj_sim.run(zero_torques)


if __name__ == "__main__":
    main()
