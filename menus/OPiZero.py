
###########################
#
# ORANGE PI ZERO
#
#
###########################


outline = """         .----.  .---------------.
 .-------|    |--|               |--------------.
 |       |    |  |               |   U          |
 .--.    |USB |  |     ETH0      |   A    .-----.
 |  |    |    |  |               |   R    |     |
 |  |    |    |  |               |   T    |     |
 |  |    '----'  |               |        |     |
 |U |            |               |        |     |
 |S |            '---------------'        |     |
 |B |   .-----.                           |     |
 |/ |   |WIFI |  USE ARROW KEYS TO MOVE   |  G  |
 |A |   |     |    SPACEBAR TO SELECT     |  P  |
 |U |   '-----'                           |  I  |
 |D |     .---------------.               |  O  |
 |I |     |               |   .------.    |     |
 |O |     |               |   |      |    |     |
 |/ |     |               |   |      |    |     |
 |T |     |ORANGE PI ZERO |   |      |    |     |
 |V |     |               |   |      |    |     |
 |  |     |               |   |      |    |     |
 |  |     |               |   |      |    |     |
 |--'   .------.----------'   '------'    '-----'
 |      |  USB |                          PIN 1^|
 '------|  OTG |--------------------------------'
        '------'                                 """

menu = [ #areas to highlight indexed at top left = 0,0 = y,x
"USB",[0,9,6,15], 
"ETH0",[0,17,8,34],
"UART",[2,37,5,38],
"GPIO",[3,42,21,48],
"USBOTG",[21,8,24,16],
"USB/AUDIO",[3,1,22,5],
"WIFI",[9,8,12,15]
]

pinsENG = ['',
'3.3 volts',					'5 volts',
'I2C0-SDA / PA12',				'5 volts',
'I2C0-SCK /PA11',				'Ground',
'PMW1 / PA6', 					'UART1-RX / PG7',
'Ground',						'UART1-TX / PG6',
'UART2-RX / PA1',				'PA7',
'UART2-TX / PA0', 				'Ground',
'UART2-CTS / PA3', 				'IC21-SCK / PA15',
'3.3 volts',					'I2C1-SDA / PA19',
'SPI1-MOSI / PA15',				'Ground',
'SPI1-MISO / PA16',				'UART2_RTS / PA2',
'SPI1-CLK / PA14',				'SPI1-CS / PA13',
'Ground',						'PA10',
]

pinsBGA = [
-1,-1,
12,-1,
11,-1,
6,199,
-1,198,
1,7,
0,-1,
3,15,
-1,19,
15,-1,
16,2,
14,13,
-1,10
]

pinsUSB = [
'5 volts',
'Ground',
'USB-DM2',
'USB-DP2',
'USB-DM3',
'USB-DP3',
'Line out Right',
'Line out Left',
'TV out',
'Mic bias',
'Mic in Positive',
'Mic in Negative',
'IR-RX'
]

UART = [
'Ground', 
'RX',
'TX'
]

boardArray = [outline, menu, pinsENG, pinsBGA, pinsUSB, UART]