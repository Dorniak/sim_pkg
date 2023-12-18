from utils.DC_motor_sim import DC_motor_sim
class Controller:
    def __init__(self):
        self.Kp = 0.0
        self.Ki = 0.0
        self.Kd = 0.0
        self.E = [0.0, 0.0]  # Error variables
        self.Ei = 0.0
        self.Ed = 0.0
        self.Angular_speed_reference = 0.0
        self.Controller_T = 0.001
        self.motor_sim = DC_motor_sim()
        self.motor_speed_anterior = 0

    def Init(self, new_Kp, new_Ki, new_Kd):
        self.Kp = new_Kp
        self.Ki = new_Ki
        self.Kd = new_Kd

        # Init controller variables of error
        self.E[0] = 0.0
        self.E[1] = 0.0
        self.Ei = 0.0
        self.Ed = 0.0

        # motor_sim = DC_motor_sim()
        # Inicializar el motor
        self.motor_sim.init()

    def Set_reference(self, Angular_speed):
        self.Angular_speed_reference = Angular_speed

    def Exec_controller_cycle(self):
        # Compute speed error
        motor_speed = DC_motor_sim.Give_me_speed(self.motor_sim)
        self.E[1] = self.Angular_speed_reference - motor_speed
        self.Ei = self.Ei + self.E[1]
        self.Ed = (self.E[1] - self.E[0]) / self.Controller_T

        # Prepare last error for next cycle
        self.E[0] = self.E[1]

        # Compute controller output
        new_motor_voltage = self.Kp * self.E[0] + self.Ki * self.Ei + self.Kd * self.Ed
        DC_motor_sim.Set_ea(self.motor_sim, new_motor_voltage)
        DC_motor_sim.Exec_cycle(self.motor_sim)
        # print("Current speed: ", motor_speed)
        # print("salida PID: ", new_motor_voltage)
        return motor_speed, new_motor_voltage

    def Exec_controller_cycleJE(self):
        # Compute speed error
        motor_speed = DC_motor_sim.Give_me_speed(self.motor_sim)

        P = (self.Angular_speed_reference - motor_speed) * self.Kp;
        I = self.E[0] + (self.Kp * 0.1 / self.Ki) * (self.Angular_speed_reference - motor_speed)
        D = ((self.Kd / (self.Kd + (8 * 0.1))) * self.E[1]) - (self.Kp * self.Kd * 8 / (self.Kd + (8 * 0.1))) * (
                    motor_speed - self.motor_speed_anterior)

        # Prepare last error for next cycle
        self.E[0] = I
        self.E[1] = D
        self.motor_speed_anterior = motor_speed
        # Compute controller output
        new_motor_voltage = P + I + D
        DC_motor_sim.Set_ea(self.motor_sim, new_motor_voltage)
        DC_motor_sim.Exec_cycle(self.motor_sim)
        # print("Current speed: ", motor_speed)
        # print("salida PID: ", new_motor_voltage)
        return motor_speed, new_motor_voltage
    

if __name__ == '__main__':
    controller = Controller()
    Kp=0.1#0.1#0.5
    Ki=7#0.008#0.004
    Kd=0.6#0.0#0.º
    controller.Init(Kp, Ki, Kd)
    print('Init')
    controller.Set_reference(50.0)