# Author: Jaey Kim (jaeykimusa.github.io)


import logging
import colorlog
from colorlog.escape_codes import escape_codes  # Import the actual dictionary


# custom levels
SIMULATION_LEVEL = 21
CONTROLLER_LEVEL = 22


class PeriodFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str) and not record.msg.strip().endswith('.'):
            record.msg = f"{record.msg.strip()}."
        return True


class SimReporter:
    def __init__(self, simName: str = "defaultSim"):
        logging.addLevelName(SIMULATION_LEVEL, "SIMULATION")
        logging.addLevelName(CONTROLLER_LEVEL, "CONTROLLER")
        
        # helper methods to the Logger class
        def simulation(self, message, *args, **kws):
            if self.isEnabledFor(SIMULATION_LEVEL):
                self._log(SIMULATION_LEVEL, message, args, **kws)
        
        def controller(self, message, *args, **kws):
            if self.isEnabledFor(CONTROLLER_LEVEL):
                self._log(CONTROLLER_LEVEL, message, args, **kws)
        
        logging.Logger.simulation = simulation
        logging.Logger.controller = controller
        
        self.logger = logging.getLogger(simName)
        self.logger.setLevel(logging.DEBUG)
        
        # color map
        color_map = {
            'DEBUG':        'white',
            'INFO':         'green',
            'SIMULATION':   'cyan',
            'CONTROLLER':   'green',
            'WARNING':      'yellow',
            'ERROR':        'red',
            'CRITICAL':     'bold_red',
        }
        
        # colored log formatter - message color is controlled by extra['msg_color']
        log_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-10s | %(name)s: "
            "%(msg_color)s%(message)s",
            datefmt='%H:%M:%S',
            log_colors=color_map,
            reset=True,
            style='%'
        )
        
        self.logger.addFilter(PeriodFilter())
        
        stream_handler = colorlog.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(stream_handler)
    

    def simulationMsg(self, msg: str = "No in return."):
        self.logger.simulation(msg, extra={'msg_color': escape_codes['cyan']})
    

    def controllerMsg(self, msg: str = "No control input."):
        self.logger.controller(msg, extra={'msg_color': escape_codes['green']})
    

    def simulationErrMsg(self, msg: str = "No error message."):
        self.logger.simulation(
            f"[ERROR] {msg}",
            extra={'msg_color': escape_codes['red']}
        )
    

    def simulationWarnMsg(self, msg: str = "No warning message."):
        self.logger.simulation(
            f"[WARN] {msg}",
            extra={'msg_color': escape_codes['yellow']}
        )