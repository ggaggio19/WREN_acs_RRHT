import time
import WREN_shared
import threading

class PID:
    """PID Controller
    """

    def __init__(self, P=0.2, I=0.0, D=0.0):

        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.deadband = 0.0

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.deadband = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, SetPoint, feedback_value):
        """Calculates PID value for given reference feedback

        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}

        .. figure:: images/pid_1.png
           :align:   center

           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        """
        error = SetPoint - feedback_value

        if error < self.deadband:
            error = 0

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time

    def setDeadBand(self, deadband):
        """ Added by LT, use to avoid jitter around the setpoint due to noise on the feedback"""
        self.deadband = deadband


class PID_run_Thread (threading.Thread):

    def __init__(self,rate,DC,KP,KI,KD,deadband,DC_channel):
        super().__init__()
        self.rate = rate
        self.daemon = True
        self.DC = DC
        self.cleartorun = False
        self.dt = min(1/self.rate,0.1)
        self.tolerance = self.dt/100
        self.DC_channel = DC_channel
        #Set up PID controller
        self.PID = PID(KP, KI, KD)
        self.PID.setSampleTime(self.dt)
        self.PID.setDeadBand(deadband)

    def run(self):
        while True:
            if self.cleartorun:
                st = time.perf_counter()
                time.sleep(self.dt / 2)
                while(time.perf_counter()-st) < self.dt + self.tolerance:
                    pass
                if self.DC == 1:
                    self.PID.update(WREN_shared.DC1_pos_dem, WREN_shared.DC1_pos_feedback)
                elif self.DC == 2:
                    self.PID.update(WREN_shared.DC2_pos_dem, WREN_shared.DC2_pos_feedback)
                self.DC_channel.setTargetVelocity(self.PID.output)

            else:
                if self.DC == 1:
                    self.cleartorun = WREN_shared.DC1_cmd_connected & WREN_shared.DC1_enc_connected
                elif self.DC == 2:
                    self.cleartorun = WREN_shared.DC2_cmd_connected & WREN_shared.DC2_enc_connected
                else:
                    print("DC number parameter error, cannot run PID control")
                time.sleep(1)


