'''
云台串口通信
----------------------------
作者: 阿凯爱玩机器人
微信: xingshunkai
邮箱: xingshunkai@qq.com
更新日期: 2022/03/03
'''
import serial

# 云台串口配置
GIMBAL_UART_PORT =  'COM3' # 舵机串口号
GIMBAL_UART_BAUDRATE = 9600 # 舵机的波特率

# 初始化串口

# gimbal_uart = serial.Serial(port=GIMBAL_UART_PORT, baudrate=GIMBAL_UART_BAUDRATE,\
# 					parity=serial.PARITY_NONE, stopbits=1,\
# 					bytesize=8,timeout=0)

gimbal_uart = serial.Serial(port=GIMBAL_UART_PORT, baudrate=GIMBAL_UART_BAUDRATE,timeout=0)

# 设置舵机角度
def set_gimbal_raw_angle(angle_down, angle_up):
	result=gimbal_uart.write(f"{int(angle_down)},{int(angle_up)},1,0E".encode("utf-8"))
	print(f"{int(angle_down)},{int(angle_up)},1,0E")
	print("写总字节数:",result)