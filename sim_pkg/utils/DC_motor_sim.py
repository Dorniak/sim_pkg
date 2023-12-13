class DC_motor_sim:
    def __init__(self):
        self.R = 1.11  # Ohm
        self.L = 0.0002  # H
        self.J = 6.77E-6  # Kgm²
        self.fv = 1.66E-5  # Nm/(Rad/s)
        self.K = 0.0364  # Nm/A or V/(Rad/s)
        self.ea = 0.0
        self.w = [0.0, 0.0]  # tk angular speed
        self.i = [0.0, 0.0]  # tk current

    def init(self):
        self.R = 1.11
        self.L = 0.0002
        self.J = 6.77E-6
        self.fv = 1.66E-5
        self.K = 0.0364
        self.ea = 0.0
        self.w = [0.0, 0.0]
        self.i = [0.0, 0.0]

    def Set_ea(self, new_ea):
        self.ea = new_ea
        # Saturation effect due to battery limits
        if self.ea > 24.0:
            self.ea = 24.0
        if self.ea < -24.0:
            self.ea = -24.


    def Give_me_speed(self):
        return self.w[0]

    def Exec_cycle(self):
        # Motor behavior considering T = 0.0001s
        self.w[0] = self.w[1]
        self.i[0] = self.i[1]
        self.w[1] = 0.999755 * self.w[0] + 14.769238 * self.K * self.i[0]
        self.i[1] = 0.574072 * self.i[0] + 0.383719 * (self.ea - self.K * self.w[1])