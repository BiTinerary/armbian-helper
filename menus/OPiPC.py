###########################
#
# ORANGE PI PC
#
#
###########################
outline = """  .----.--------------------------------------------------------.-.---.---.
  |    |                                                        | |IR |   |
  |    |                            GPIO                        | '---'   |
  |    '--------------------------------------------------------'         |
 .---.  ^PIN 1                                                 .---------------.
 |U  |                   <- USE ARROW KEYS ->                  |     USB       |
 |S  |                    SPACEBAR TO SELECT                   '---------------'
 |B  |                                                       .-----------------.
 '---'                    ORANGE PI PC                       |                 |
  .---.                                                      |                 |
  |   |                                                      |      ETH0       |
  |   |                                                      |                 |
  | C |                                                      |                 |
  | S |                                                      '-----------------'
  | I |                                                        .---------------.
  |   |                                                        |               |
  |   |                                                        |     USB       |
  '---'                                               .----.   |      X2       |
  |     .---.           .-------------.               | A  |   |               |
  |     | D |           |             |               | U  |   '---------------'
  |     | C |           |             |   .---.       | D  |              |   
  |     | I |    UART   |    HDMI     |   |MIC|       | I  |              |   
  '-----| N |-----------|             |---'---'-------| O  |--------------'   
        '---'           '-------------'               '----'                   """

menu = [
"GPIO",[0,7,3,65],
"IR",[0,66,2,71],
"USB",[4,63,6,80],
"ETH0",[7,61,13,80],
"USBX2",[14,63,19,80],
"AUDIO",[17,54,23,60],
"MIC",[20,42,22,47],
"HDMI",[18,24,23,39],
"UART",[21,17,21,21],
"CSI",[9,2,17,7],
"USBOTG",[4,1,8,6]
]

pins = [
'3.3 volts'					,-1,'5 volts'  					,-1,
'I2C0-SDA / PA12'			,12,'5 volts'						,-1,
'I2C0-SCK /PA11' 			,11,'Ground'						,-1,
'PMW1 / PA6'				,6, 'SPI1-CS / PA13'				,13,
'Ground'					,-1,'SPI1-CLK / PA14'				,14,
'UART2-RX / PA1'			,1, 'PD14'						,110,
'UART2-TX / PA0'			,0, 'Ground'						,-1,
'UART2-CTS / PA3'			,3, 'PC4'							,68,
'3.3 volts'					,-1,'PC7'							,71,
'SPI0-MOSI / PC0'			,64,'Ground'						,-1,
'SPI0-MISO / PC1'			,65,'UART2_RTS / PA2'				,2,
'SPI0-CLK / PC2'			,66,'SPI0-CS / PC3'				,67,
'Ground'					,-1,'PCM0-DIN / PA21'				,21,
'PCM0-CLK / I2C1-SDA / PA19',19,'PCM0-SYNC / I2C1-SCK / PA18'	,18,
'PA7'						,7, 'Ground'						,-1,
'PA8'						,8, 'PG8'							,200,
'PA9'						,9, 'Ground'						,-1,
'PA10'						,10,'PG9'							,201,
'PA20'						,20,'PG6'							,196,
'Ground'					,-1,'PG7'							,197
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
'Ground',	#nearest the DC barrel 
'RX',
'TX'		#nearest the HDMI
]

usb = """  .------.
 /      /|
.------. |
| USB2 | |
|------| '
| USB1 |/ 
'------'  
"""

boardArray = [outline, menu, pinsENG, pinsBGA, UART]

PINS = """                                   .-------.
                         3.3 volts | 1  2  | 5 volts
                    I2C_SDA / PA12 | 3  4  | 5 volts
                    I2C_SCK / PA11 | 5  6  | GND
                        PWM1 / PA6 | 7  8  | PA13 / SPI1_CS   / UART3_TX
                               GND | 9  10 | PA14 / SPI1_CLK  / UART3_RX
                    UART2_RX / PA1 | 11 12 | PD14
                    UART2_TX / PA0 | 13 14 | GND
                   UART2_CTS / PA3 | 15 16 | PC4
                         3.3 volts | 17 18 | PC7
                   SPI0-MOSI / PC0 | 19 20 | GND
                   SPI0-MISO / PC1 | 21 22 | PA2  / UART2_RTS
                    SPI0-CLK / PC2 | 23 24 | PC3  / SPI0_CS
                               GND | 25 26 | PA21 / PCM0_DIN
        PCM0-CLK / I2C1-SDA / PA19 | 27 28 | PA18 / PCM0_SYNC / SDA1_SCK
                               PA7 | 29 30 | GND
                               PA8 | 31 32 | PG8  / UART1_RTS
                               PA9 | 33 34 | GND
                              PA10 | 35 36 | PG9  / UART1_CTS
                              PA20 | 37 38 | PG6  / UART1_TX
                               GND | 39 40 | PG7  / UART1_RX
                                   '-------'                           
                                                                        
"""