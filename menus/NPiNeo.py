###########################
#
# NANOPI NEO
#
#
###########################

outline = """           .------------.  .----.
   .-------|            |--|    |-----------.
   |       |            |  |    |           |
   |       |            |  | U  |  A        |
   .-----. |   ETH0     |  | S  |  U        |
   |     | |            |  | B  |  D  U .---.
   |     | |            |  |    |  I  A |   |
   |     | |            |  |    |  O  R |   |
   |     | '------------'  '----'     T |   |
   |     |                              | U |
   | G   |                              | S |
   | P   |                              | B |
   | I   |         NANOPI NEO           | / |
   | O   |                              | I |
   |     |                              | 2 |
   |     |                              | S |
   |     |             .-------------.  |   |
   |     |             |             |  |   |
   |     |             |             |  |   |
   |     | <PIN 1      |   MICROSD   |  '---'
   '-----' .------.    |             |      |
   |       | USB  |    |             |      |
   '-------| OTG  |----'-------------'------'
           '------'                          """

menu = [ #areas to highlight
"ETH0",[0,11,8,25], 
"USB0",[0,27,8,33],
"AUDIO",[3,35,7,36],
"UART",[5,38,9,39],
"USB/I2S",[5,40,19,45],
"MICROSD",[16,23,22,38],
"USBOTG",[20,11,23,19],
"GPIO",[4,3,20,10]
]

pinsENG = [ '',#need dummy first string?
'3.3 volts',					'5 volts',
'I2C0-SDA / PA12',				'5 volts',
'I2C0-SCK /PA11',				'Ground',
'PMW1 / PA6', 					'SPI1-CS / PA13',
'Ground',						'SPI1-CLK / PA14',
'UART2-RX / PA1',				'PD14',
'UART2-TX / PA0', 				'Ground',
'UART2-CTS / PA3', 				'PC4',
'3.3 volts',					'PC7',
'SPI0-MOSI / PC0',				'Ground',
'SPI0-MISO / PC1',				'UART2_RTS / PA2',
'SPI0-CLK / PC2',				'SPI0-CS / PC3'
]

pinsBGA = [
-1,-1,
12,-1,
11,-1,
6,13,
-1,14,
1,110,
0,-1,
3,68,
-1,71,
64,-1,
65,2,
66,67
]

smallPinsENG = ['',
'5 volts',
'USB-DP1',
'USB-DM1',
'USB-DP2',
'USB-DM2',
'GPIOL11 / IR-RX',
'SPDIF-OUT / GPIOA17',
'PCM0-SYNC / I2S0-LRC',
'PCM0-CLK / I2S0-BCK',
'PCM0-DOUT / I2S0-SDOUT',
'PCM0-DIN / I2S0-DIN',
'Ground'
]

pinsAudio = [
'Mic-in Positive',
'Mic-in Negative',
'Line out Right',
'Ground',
'Line out left'
]

UART = [
'Ground',
'5 volts',
'TX',
'RX'
]

boardArray = [outline, menu, pinsENG, pinsBGA, smallPinsENG, pinsAudio, UART]