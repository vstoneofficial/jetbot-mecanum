import  serial
import  struct

class MecanumRover_DCMotor:
    #各モータの目標速度格納メモリのアドレス
    LEFT_MOTOR = 'AC'
    RIGHT_MOTOR = 'AE'

    FORWARD_MOTOR = '1F'
    BACKWARD_MOTOR = '10'

    def __init__(self,driver,motornum):
        self.ser = driver

        if motornum == 0:
            self.motorAddr = self.LEFT_MOTOR
            self.motorId = self.FORWARD_MOTOR
        elif motornum == 1:
            self.motorAddr = self.RIGHT_MOTOR
            self.motorId = self.FORWARD_MOTOR
        elif motornum == 2:
            self.motorAddr = self.LEFT_MOTOR
            self.motorId = self.BACKWARD_MOTOR
        elif motornum == 3:
            self.motorAddr = self.RIGHT_MOTOR
            self.motorId = self.BACKWARD_MOTOR
        else:
            raise NameError('Motor chennel must be between 1 and 4 inclusive')

    def setSpeed(self,speed):
        if speed > 1300:
            speed=1300
        elif speed < -1300:
            speed = -1300
        cmd = 'w' + self.motorId + ' ' + self.motorAddr + ' ' + self.int2litteEndian(speed) + '\n'
        self.ser.write(cmd.encode('utf-8'))

    def int2litteEndian(self,speed):
        #リトルエンディアン(2バイト)に変換
        speed_bin = struct.pack('<h',speed)
        return speed_bin.hex()


class MecanumRover_MotorDriver:
    WRC_GAIN_ADDR = '20'

    def __init__(self, addr='/dev/ttyUSB_Rover', baud=115200, waitLimit=0.1, *args):
        try:
            self.ser = serial.Serial(addr,baud,timeout=waitLimit)
            self.motors = [MecanumRover_DCMotor(self.ser, m) for m in range(4)]
            #速度の比例ゲインを0に（0以外の場合、シリアルで操作ができない）
            start_cmd = 'w10 ' + self.WRC_GAIN_ADDR + ' 00000000\n'
            self.ser.write(start_cmd.encode('utf-8'))
            start_cmd = 'w1F ' + self.WRC_GAIN_ADDR + ' 00000000\n'
            self.ser.write(start_cmd.encode('utf-8'))
        except FileNotFoundError as e:
            print(e)

    def getMotor(self,num):
        if (num < 1) or (num > 4):
            raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
        return self.motors[num-1]
