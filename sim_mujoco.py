# Author: Jaey Kim (jaeykimusa.github.io)


from robot_description.go2_description import go2_mujoco 

from sim_reporter import SimReporter

import mujoco as mj 
import mujoco.viewer as mjv 
import logging 
from dataclasses import dataclass, field 


@dataclass
class SimConfig:
    """Configuration for the Go2 Simulation. """
    # default simulation settings
    dt: float = 0.002
    showSimMsg: bool = True
    show_contact_pts: bool = False
    show_joint_axes: bool = False
    transparent_robot: bool = False    # xray_mode: show axes + transparent
    # show_contact_forces: bool = False   //TODO: NOT IN USE
    # show_com: bool = False              //TODO: NOT IN USE


@dataclass
class SimPropty:
    """Dynamic simulation properties. """
    # kd: float = 0.1             //TODO: NOT IN USE
    # kp: float = 0.1             //TODO: NOT IN USE
    # use_gravity: bool = True    //TODO: NOT IN USE


@dataclass
class SimCamConfig:
    """Camera configuration for the simulation viewer. """
    # camera settings
    cam_azimuth: float = 135.0    # Horizontal angle (deg)
    cam_elevation: float = -20.0  # Vertical angle (deg)
    cam_distance: float = 3.0     # Distance from robot (meters)
    cam_target: list = field(default_factory=lambda: [0, 0, 0.3]) # Focus point
    # enable_recorder: bool = False //TODO: NOT IN USE


class WolfMiniSim:


    def __init__(
            this,
            simName: str = "defaultSim",
            simConfig: SimConfig | None = None, 
            simPropty: SimPropty| None = None, 
            simCamConfig: SimCamConfig | None = None,
            simReporter = SimReporter):
        
        this.simName = simName

        this.model = go2_mujoco.model
        this.data = go2_mujoco.data

        this.simConfig = simConfig or SimConfig()
        this.simPropty = simPropty or SimPropty()
        this.simCamConfig = simCamConfig or SimCamConfig()
        this.simReporter = simReporter

        # values from config obj
        this.dt = this.simConfig.dt; this.model.opt.timestep = this.simConfig.dt    # defaut to 0.002s

        this.viewer = None


    def reset(this):
        mj.mj_resetData(this.model, this.data)


    def get_state(this):
        return {
            "q": this.data.qpos.copy(),
            "qd": this.data.qvel.copy(),
            "qdd": this.data.qacc.copy(),
        }


    def apply_control(this, tau):
        this.data.ctrl[:] = tau


    def step(this):
        mj.mj_step(this.model, this.data)


    def render(this):
        if this.viewer is not None:
            this.viewer.sync()


    def launch_viewer(this, contactPts=False, jointAxes=False, robotTransprt=False):
        this.simReporter.simulationMsg("Launching simulation. ")
        
        try:
            # Launch viewer
            this.viewer = mjv.launch_passive(this.model, this.data)

            # Camera configuration
            this.viewer.cam.azimuth = this.simCamConfig.cam_azimuth
            this.viewer.cam.elevation = this.simCamConfig.cam_elevation
            this.viewer.cam.distance = this.simCamConfig.cam_distance
            this.viewer.cam.lookat[:] = this.simCamConfig.cam_target

            # Visualization flags
            this.viewer.opt.flags[mj.mjtVisFlag.mjVIS_JOINT] = this.simConfig.show_contact_pts
            this.viewer.opt.flags[mj.mjtVisFlag.mjVIS_CONTACTPOINT] = this.simConfig.show_joint_axes
            this.viewer.opt.flags[mj.mjtVisFlag.mjVIS_TRANSPARENT] = this.simConfig.transparent_robot

            this.simReporter.simulationMsg("Successfully launched simulation. ")
            return True

        except Exception as e:
            this.simReporter.simulationMsg("Failed to launch simulation. ")
            this.simReporter.simulationErrMsg(f"{e}")
            this.viewer = None
            return False


    def run(this, tau):
        this.launch_viewer(False, False, False)

        with this.viewer:
            while this.viewer.is_running():
                state = this.get_state()
                # tau = controller.compute_control(state)
                this.apply_control(tau)
                this.step()
                this.render()


    def close(this):
        this.viewer.close()


