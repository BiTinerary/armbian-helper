###########################
#
# ORANGE PI ONE
#
#
###########################
outline = """    .-----.--------------------------------------------------.-------.
    |     |                       GPIO                       | <PIN 1|
    |     |                                                  |       |
    |     '--------------------------------------------------'       |
    |                                                                |
  .-----------.                                                      |
  |    USB    |                                                      |
  '-----------'                                                      |
 .--------------.          ORANGE PI ONE                             |
 |              |                                                    |
 |              |                                                    |
 |    ETH0      |                                                    |
 |              |                   .-------------.                  |
 |              |                   |             |                  |
 '--------------'                   |             |      .----.      |
    |  UART                         |             |      |  D |      |
    |           .-------------.     |   MICROSD   |      |  C |      |
    | .-----.   |             |     |             |      |  - |      |
    | | USB |   |    HDMI     |     |             |      |  I |      |
    '-| OTG |---|             |-----'-------------'------|  N |------'
      '-----'   |             |                          '----'       
                '-------------'                                       """

menu = [
"GPIO",[0,10,3,62],
"MICROSD",[12,36,19,51],
"HDMI",[16,16,22,31],
"USBOTG",[17,6,20,13],
"UART",[15,7,15,11],
"ETH0",[8,1,14,17],
"USB",[5,2,7,15]
]


pinsENG = ['',
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
'SPI0-CLK / PC2',				'SPI0-CS / PC3',
'Ground',						'PCM0-DIN / PA21',
'PCM0-CLK / I2C1-SDA / PA19',	'PCM0-SYNC / I2C1-SCK / PA18',
'PA7', 							'Ground',
'PA8', 							'PG8',
'PA9', 							'Ground',
'PA10',							'PG9',
'PA20',							'PG6',
'Ground',						'PG7'
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
66,67,
-1,21,
19,18,
7,1,
8,200,
9,-1,
10,201,
20,196,
-1,197
]

UART = [
'Ground',
'RX',
'TX'
]

boardArray = [outline, menu, pinsENG, pinsBGA, UART]