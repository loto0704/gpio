#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# GPIOのピン番号を定義
PIN = 18

# 周波数を定義
Hz = 50

# CPUの温度を取得
def get_CPU_Temperature():
    temp = "0"

    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        for t in f:
            temp=t[:2] + "." + t[2:5]

    return float(temp)


# PWM実行
def exec_pwm():
    # GPIO設定
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)

    p = GPIO.PWM(PIN, Hz)

    try:
        Duty = 100 # 出力（最初小さいと回らない可能性があるので100%にセット）
        p.start(Duty)
        time.sleep(30)

        while True:
            CPU_Temp = get_CPU_Temperature()
            if CPU_Temp < 35.0:
                Duty = 40
            elif CPU_Temp < 40.0:
                Duty = 50
            elif CPU_Temp < 45.0:
                Duty = 75
            else:
                Duty = 100

            print(str(CPU_Temp) + ' : ' + str(Duty))
            p.ChangeDutyCycle(Duty)
            time.sleep(10)

    except Exception as e:
        print ("[例外発生] fan_control.py を終了します。")
        print ("Exception : " + str(e))
        print ("     Type : " + str(type(e)))
        print ("     Args : " + str(e.args))
        print ("  Message : " + str(e.message))

    except KeyboardInterrupt:
        pass


    finally:
        # PWMを終了
        p.stop()

        # GPIO開放
        GPIO.cleanup()
        print('finally実行')

if __name__ == "__main__":
    time.sleep(1)
    exec_pwm()
