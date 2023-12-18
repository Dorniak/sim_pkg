import rclpy
from rclpy.node import Node
from my_msgs.srv import SimPID  # Importa el mensaje de servicio personalizado

from matplotlib import pyplot as plt
from utils.Performance import Performance
from utils.Controller import Controller

class SimPIDService(Node):
    def __init__(self):
        super().__init__('sim_pid_node')
        self.srv = self.create_service(SimPID, '/serv/sim_pid', self.sim_pid_callback)

        # Initialization of Performance, Controller, etc.
        self.P = Performance()
        self.controller = Controller()

        self.velocidad = []
        self.ut = []
        self.coordenadax = []

        self.Velocidad_de_referencia = 50.0

    def sim_pid_callback(self, request, response):
        # Obtain Kp, Ki, Kd from the request
        Kp = request.Kp
        Ki = request.Ki
        Kd = request.Kd

        # Initialize the controller with the provided gains
        self.controller.Init(Kp, Ki, Kd)
        self.controller.Set_reference(self.Velocidad_de_referencia)

        # Execute controller cycles
        for ite in range(320):
            x, y = self.controller.Exec_controller_cycleJE()
            self.velocidad.append(x)
            self.ut.append(y)
            self.coordenadax.append(ite)

        # Calculate performance metrics
        self.P.Init(self.velocidad, self.Velocidad_de_referencia)
        overshoot, d, ess, Ts = self.P.Calcula_indexes()

        # Assign calculated values to response
        response.overshoot = overshoot
        response.d = d
        response.ess = ess
        response.TS = Ts

        # Clear lists for next service call
        self.velocidad.clear()
        self.ut.clear()
        self.coordenadax.clear()

        return response


def main(args=None):
    rclpy.init(args=args)
    sim_pid_service = SimPIDService()
    rclpy.spin(sim_pid_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
