#!/usr/bin/python
import subprocess, curses, curses.panel, os
from importlib import import_module
from time import sleep
#################################################
# put menu.py here#
############################################
COLUMNS=79 #default tty size - 1 
LINES=24

def make_panel(h,l, y,x, str):
	win = curses.newwin(h,l, y,x)
	win.erase()
	win.box()
	win.addstr(2, 10, str)
	panel = curses.panel.new_panel(win)
	return win, panel

def test(stdscr,board):
	setupScreen(stdscr)
	menuitems=getBoardMenu(board)		#return array of menu item strings
	currentMenuItem=menuitems[0]		#declare starting point
	highlightMenu(currentMenuItem,stdscr,board)
	try:
		mainMenu(stdscr, currentMenuItem, menuitems)
	except KeyboardInterrupt:
		curses.endwin()
		quit()

def gpioMenu(screen, board):
	helpwin,helppanel = make_panel(20,45,3,20, '')
	helppanel.hide()
	defwin,defpanel = make_panel(24,75,0,0, 'DEFINITIONS:')
	defpanel.hide()
	screen.erase()
	warning="White arrow on board always points to pin 1"
	screen.addstr(0,COLUMNS/2-len(warning)/2,warning,curses.A_BOLD)
	pinNumbers=board[3]
	pinNames=board[2]
	offset=1
	for x in range(0,len(pinNumbers)+1): #create pin numbers
		if x % 2==1: 				#right side
			screen.addstr((x+offset-(x/2)), (COLUMNS/2-1), str(x), curses.A_BOLD)			 #put even numbers on right side 
			screen.addstr((x+offset-(x/2)), (COLUMNS/2-4)-len(pinNames[x]), pinNames[x])	 #names on right side at the right offset
		else:
			screen.addstr((x+offset-(x/2)), (COLUMNS/2+2), str(x), curses.A_BOLD) 			#put odd numbers on left side
			screen.addstr((x+offset-(x/2)), (COLUMNS/2+7), pinNames[x])						#names on left side
	#now draw a box
	screen.addstr(offset,36,'.-------.') 							#top bar
	screen.addstr(offset+len(pinNumbers)/2+1,36,"'-------'")		#bottom bar
	screen.vline(offset+1,36,'|',len(pinNumbers)/2)					#left side
	screen.vline(offset+1,44,'|',len(pinNumbers)/2)					#right side
	index=4											#place on screen to draw
	screen.chgat(index/2,15,25,curses.A_STANDOUT)	#first pin
	while True:
		pinStats(index, screen)
		c = screen.getch()
		
		if c == curses.KEY_RIGHT:
			helppanel.hide()
			defpanel.hide()
			screen.hline(24,0," ",COLUMNS)
			index=index+1
			#if index >=44:
			if index >= len(pinNumbers)+4:		#out of bounds on bottom
				index=4							#wrap to top left 
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		if c == curses.KEY_LEFT:
			helppanel.hide()
			defpanel.hide()
			screen.hline(24,0," ",COLUMNS)
			if index <5:						#out of bounds on top 
				index= len(pinNumbers)+4		#wrap selection to bottom right
			index = index-1
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		
		if c == curses.KEY_UP:
			helppanel.hide()
			defpanel.hide()
			screen.hline(24,0," ",COLUMNS)
			index = index-2
			if index <4: 						#out of bounds on the top
				index=len(pinNumbers)+3			#wrap selection to bottom right
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		
		if c == curses.KEY_DOWN:
			helppanel.hide()
			defpanel.hide()
			screen.hline(24,0," ",COLUMNS)
			index = index+2
			if index >=len(pinNumbers)+4:		#out of bottom bounds
				index=4							#wrap selection to top left
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		
		if c == 27: #escape key to quit
			clearScreen(screen)
			return
###########################################
#
# s = intitialize
# u = uninitialize
# i = input
# o = output
# 1 = set high
# 0 = set low
# r = read pin value
#
# h = help menu, basically this prompt
#
###############################################
		if c == 115: # ord('s')
			screen.hline(24,0," ",79) #clear line completely
			if pinNumbers[(index-4)] == -1:
				response = "cannot init this pin"
				pass
			elif createPinsysfs(pinNumbers[(index-4)]) == 0:
				response = "successfully initialized pin " + str((index+3)/2)
			screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
		if c == 117: # 'u'
			screen.hline(24,0," ",79) #clear line completely
			if pinNumbers[(index-4)] == -1:
				response = "cannot uninit this pin"
				pass
			elif removePinsysfs(pinNumbers[(index-4)]) == 0:
				response = "successfully uninitialized pin " + str((index+3)/2)
			screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
		if c == 114: # 'r'
			if pinNumbers[(index-4)] == -1:
				response = "This pin's state is not able to be changed"
				pass
			else:
				screen.hline(24,0," ",79)
				value = readPinsysfs(pinNumbers[(index-4)])
				if value is None:
					response = "This pin is not initialized"
				else:
					response = "Pin "+str(index-3)+"'s value is "+str(value)
			screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
		if c == 105: # 'i'
			screen.hline(24,0," ",79) #clear line completely
			if pinNumbers[(index-4)] == -1:
				response = "This pin's state is not able to be changed"
				pass
			else:
				value = directionPinsysfs(pinNumbers[(index-4)],'in')
				if value == 0:
					response = "Pin "+str(index-3)+" is an input pin and can sink up to 10 milliamps"
				if value == -1:
					response = "Pin is already set to input"
			screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
		if c == 111: # 'o'
			if pinNumbers[(index-4)] == -1:
				response = "This pin's state is not able to be changed"
				screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
				pass
			else:
				screen.hline(24,0," ",79) #clear line completely
				value = directionPinsysfs(orangepiPCPins[(index-3)*2-1],'out')
				if value == 0:
					response = "Pin "+str(index-3)+" is an output pin and can source up to 10 milliamps"
				if value == -1:
					response = "Pin is already set to output"
				screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
				
				
		if c == 49: # '1'
			screen.hline(24,0," ",79) #clear line completely
			response=''
			if orangepiPCPins[(index-3)*2-1] == -1:
				response = "This pin's state is not able to be changed"
			elif os.path.isdir('/sys/class/gpio/gpio'+str(orangepiPCPins[(index-3)*2-1])) == False: #not configured
				createPinsysfs(orangepiPCPins[(index-3)*2-1])
			elif readSysfs(orangepiPCPins[(index-3)*2-1], 'direction') == 'in':
				response = "This pin is an input and cannot be set to 1 (3.3 volts)"
				screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
			else:
				
				value = valuePinsysfs(orangepiPCPins[(index-3)*2-1],'On')
				if value == 0:
					response = "Pin "+str(index-3)+"'s value is set to 1 (3.3 volts)"
				if value == -1:
					response = "Pin's value is already at 1"
			screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
				
		if c == 48: # '0'
			screen.hline(24,0," ",79) #clear line completely
			if orangepiPCPins[(index-3)*2-1] == -1:
				response = "This pin's state is not able to be changed"
			elif os.path.isdir('/sys/class/gpio/gpio'+str(orangepiPCPins[(index-3)*2-1])) == False: #not configured
				createPinsysfs(orangepiPCPins[(index-3)*2-1])
			elif readSysfs(orangepiPCPins[(index-3)*2-1],'direction').strip('\n')=='in':
				response = "This is set to input and cannot be pulled low"
			else:
				value = valuePinsysfs(orangepiPCPins[(index-3)*2-1],0)
				if value == 0:
					response = "Pin "+str(index-3)+"'s value is set to 0 (ground)"
				if value == -1:
					response = "Pin's value is already at 0"
			screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
		
		if c == 104: # 'h'
			helpMenu(helpwin,gpio)
			#helpwin.erase()
			#helpwin,helppanel = make_panel(20,45,3,20, 'AVAILABLE COMMANDS:')
			'''
			helpwin.addstr(2,10,"AVAIALBLE COMMANDS: ")
			helpwin.addstr(4,10,"s - initialize pin")
			helpwin.addstr(5,10,"u - unitialiaze pin")
			helpwin.addstr(6,10,"r - read pin's current value")
			helpwin.addstr(7,10,"i - set pin direction input")
			helpwin.addstr(8,10,"o - set pin direction output")
			helpwin.addstr(9,10,"1 - set pin high")
			helpwin.addstr(10,10,"0 - set pin low")
			helpwin.addstr(12,2,"press any arrow key to close this window")
			helpwin.addstr(14,2,"press m if this you need more help", curses.A_BOLD)
			'''
			helppanel.show()
			helpwin.refresh()
			updateScreen(screen)
			
			c = helpwin.getch()
			if c == 109: #'m'
				#defwin,defpanel = make_panel(24,75,0,0, 'DEFINITIONS:')
				
				#defwin.erase()
				defwin.addstr(2,10, "DEFINITIONS:")
				
				defwin.addstr(3,4,"The row of pins on the board have several functions", curses.A_BOLD)
				defwin.addstr(4,4,"The ones marked Ground, 5 volts, and 3.3 volts can't be changed", curses.A_BOLD)
				defwin.addstr(5,4,"The other ones can either be general purpose inputs or outputs", curses.A_BOLD)
				defwin.addstr(6,4,"They are called GPIO", curses.A_BOLD)
				defwin.addstr(7,4,"Some GPIO are part of other systems, such as SPI, I2C, and I2S", curses.A_BOLD)
				defwin.addstr(8,4,"----------------------------------------------------------------",curses.A_BOLD)
				defwin.addstr(9,4,"Pin names are derived from a formula based on the H3 CPU:",curses.A_BOLD)
				defwin.addstr(10,4,"(position of letter in alphabet - 1) * 32 + pin number",curses.A_BOLD)
				defwin.addstr(11,4,"So PG14 would be pin number 206",curses.A_BOLD)
				defwin.addstr(12,4,"Pins have to be initialized before they can be used",curses.A_BOLD)
				defwin.addstr(13,4,"Echo your calculated pin number to /sys/class/gpio/export",curses.A_BOLD)
				defwin.addstr(14,4,"This creates the directory /sys/class/gpio/gpio206",curses.A_BOLD)
				defwin.addstr(15,4,"Now you can change the properties of the pins",curses.A_BOLD)
				defwin.addstr(16,4,"By echoing values to the files in that directory",curses.A_BOLD)
				defwin.addstr(17,4,"----------------------------------------------------------------",curses.A_BOLD)
				defwin.addstr(18,4,"For more information, google 'gpio with sysfs'",curses.A_BOLD)
				defwin.addstr(19,4,"With patience, you can learn it. Believe in yourself",curses.A_BOLD)
				defwin.addstr(21,4,"PRESS ANY ARROW KEY TO EXIT THIS PROMPT", curses.A_STANDOUT)
				defwin.refresh()
				defpanel.show()
				updateScreen(screen)
			helpwin.timeout(-1)

def helpMenu(window, gpio):
	#window.erase()
	for x in range(len(gpio)):
		if x == 0:
			window.addstr(2+x,45/2-(len(gpio[0])-2),gpio[0],curses.A_BOLD)
		else:
			window.addstr(2+x,10,str(gpio[x]))


def mainMenu(stdscr, currentMenuItem, menuitems):
	while True:
		changed=0
		c = 0
		c = stdscr.getch()						#get a character

		if c == curses.KEY_RIGHT:
			try:
				currentMenuItem=menuitems[menuitems.index(currentMenuItem)+1]
			except:
				currentMenuItem=menuitems[0] #loop it
			changed=1
		if c == curses.KEY_LEFT:
			try:
				currentMenuItem=menuitems[menuitems.index(currentMenuItem)-1]
			except:
				currentMenuItem=menuitems[0] #loop it
			changed=1
		if c ==  32: #enter or spacebar for selection
			stdscr.addstr(10,20,"YOU HAVE SELECTED: %s" %currentMenuItem, curses.A_BOLD)
			if currentMenuItem=="GPIO":
				gpioMenu(stdscr,board)
				currentMenuItem=menuitems[0]
				#highlightMenu(currentMenuItem,stdscr,board)
			if currentMenuItem=="USB":
				#manually plug things into these ports and figure out their lsusb bus id
				#then tell the user what is plugged in and at what speed
				#same thing with USB2.0, but maybe use one of those cool cube things from asciio
				pass
			if currentMenuItem=="ETH0":
				#display ifconfig?
				#make sure its active with dmesg | grep
				#state speed
				#options like nmtui for setting up a static ip
				#dnsmasq configs?
				pass
			if currentMenuItem=="USBX2":
				#same as USB
				pass
			if currentMenuItem=="AUDIO":
				#alsamixer prompt (not sure how do swing that)
				#speaker-test
				#TV out does not work on mainline
				pass
			if currentMenuItem=="MIC":
				#arecord
				#simple visualizer? with alsa api?
				pass
			if currentMenuItem=="HDMI":
				#h3disp? does that work on mainline?
				#check /boot/boot.cmd to make sure sane settings
				# Recompile with:
				# mkimage -C none -A arm -T script -d /boot/boot.cmd /boot/boot.scr
				#check device tree
				#make sure dtc is installed
				#fancy string search sed -i stuff
				pass
			if currentMenuItem=="CSI":
				pass
			if currentMenuItem=="USBOTG":
				usbMenu(stdscr)
				'''
				possible legacy drivers:
					g_ether
					g_serial
						warning that this already is set up
					g_mass_storage
						cdrom=y, for booting ISOs
					g_hid
					g_midi
				possible configfs stuff:
					literally anything
				options for dns server with g_ethernet
				options for iptables routing to use device as usb-ethernet dongle
				directions for possible network sharing setups on linux, windows, mac
				modify /etc/modules
				'''
		updateScreen(stdscr)
		if(changed==1):
			highlightMenu(currentMenuItem,stdscr,board)	#display selection
		if c == 27: #escape key to quit
			curses.endwin()
			quit()

def pinStats(pin,screen):
	for x in range(0,5):
		screen.addstr(x,0,'             ')
	actualpin = orangepiPCPins[(pin-3)*2-1]  #get actual pin number, aka PC7=71 or whatever
	if actualpin == -1:
		slot1="cant change"
		screen.addstr(0,0,slot1,curses.A_STANDOUT)
		updateScreen(screen)
		return
	else:
		slot1='sysfs#: '
		screen.addstr(0,0,slot1+str(actualpin),curses.A_STANDOUT)
		if os.path.isdir('/sys/class/gpio/gpio'+str(actualpin)) == False:#no config dir
			configured1="This pin not"
			configured2="configured"
			screen.addstr(1,0,configured1,curses.A_STANDOUT)
			screen.addstr(2,1,configured2,curses.A_STANDOUT)
		else:
			success="configured"
			screen.addstr(1,0,success,curses.A_STANDOUT)
			#file = '/sys/class/gpio/gpio'+str(actualpin)+'/value'
			#p = subprocess.Popen(["cat",file],stdout=subprocess.PIPE)
			#out, err = p.communicate()
			status = "cur val: " + str(readPinsysfs(actualpin))  
			screen.addstr(2,0,status,curses.A_STANDOUT) 
			status2 = "cur dir: "
			file = '/sys/class/gpio/gpio'+str(actualpin)+'/direction'
			p = subprocess.Popen(['cat',file],stdout=subprocess.PIPE)
			out, err = p.communicate()
			status2 += out.strip('\n')
			screen.addstr(3,0,status2,curses.A_STANDOUT) 
			status3= "activelow: "
			activelow=str(readSysfs(actualpin,'active_low').strip('\n'))
			screen.addstr(4,0,status3+activelow,curses.A_STANDOUT)
	updateScreen(screen)

def highlightMenu(menuitem,screen,board): #need to pass it stdscr
	'''
	takes a string which is in an array and highlights the element it is referring to as described in the array
	"STRING"[starty,startx,endy,endx]
	
	   startx
	starty-> .------------------.
	         |                  |
	         |                  |
	         .------------------. <---endy
	                            ^endx
	'''
	for x in range(0,len(board[0].split('\n'))): #redraw screen with outline
		screen.addstr(x,0,board[0].split('\n')[x])
	counter = 0
	for x in range(board[1][board[1].index(menuitem)+1][0],board[1][board[1].index(menuitem)+1][2]+1): #only highlight the areas that need it
		screen.addstr((board[1][board[1].index(menuitem)+1][0])+counter,board[1][board[1].index(menuitem)+1][1],board[0].split('\n')[x][board[1][board[1].index(menuitem)+1][1]:board[1][board[1].index(menuitem)+1][3]], curses.A_BOLD | curses.A_STANDOUT)
		counter=counter+1
	updateScreen(screen)
def setupScreen(screen):
	try:
		curses.curs_set(0)
		screen.nodelay(1)
	except:
		pass
	curses.start_color()
	curses.use_default_colors() 
	for i in range(0, curses.COLORS):
		curses.init_pair(i+1, i, 0)
	#screen.bkgd(' ', curses.color_pair(0 ) )

def clearScreen(screen):
	for x in range(0,25):
		screen.hline(x,0,' ',COLUMNS) 		#erase entire screen
		screen.chgat(x,0,curses.A_NORMAL)	#reset to normal attributes

def updateScreen(screen):
	curses.panel.update_panels()
	screen.refresh()

def getBoardMenu(board):
	menuitems=[]
	for x in range(0,len(board[1]),2): #get menu item titles
		menuitems.append(board[1][x])  
	return menuitems
def createPinsysfs(pin):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == False:
		command = 'echo ' + str(pin) + ' > /sys/class/gpio/export'
		subprocess.call(command,shell=True)
		return 0
	else:
		return -1

def removePinsysfs(pin):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		command = 'echo ' + str(pin) + ' > /sys/class/gpio/unexport'
		subprocess.call(command,shell=True)
		return 0
	else:
		return -1

def directionPinsysfs(pin,direction):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		command = 'echo ' + str(direction) + ' > /sys/class/gpio/gpio' + str(pin) + '/direction'
		subprocess.call(command, shell=True)
		return 0
	else:
		return -1

def valuePinsysfs(pin, value):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		if value == "True" or value == "On" or value ==  1:
			value = 1
		else:
			value = 0
		command = 'echo ' + str(value) + ' > /sys/class/gpio/gpio'+str(pin)+'/value'
		subprocess.call(command,shell=True)
		if readSysfs(pin, 'direction') == 'in': #can't set input high
			return -1
		return 0
	else:
		return -1

def readPinsysfs(pin):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		file = '/sys/class/gpio/gpio'+str(pin)+'/value'
		p = subprocess.Popen(["cat",file],stdout=subprocess.PIPE)
		out, err = p.communicate()
		return out.strip('\n')

def readSysfs(pin, filename):
	file = '/sys/class/gpio/gpio'+str(pin)+'/'+str(filename)
	p = subprocess.Popen(["cat",file],stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out.strip('\n')


def readFile(filename):
	with open(filename,"r+") as a:
		lines = a.readlines()
	return lines

def writeFile(filename,strings):
	with open(filename,"w+") as a:
		a.write(strings)
	a.close()

def replaceModules(replace): #modify boot modules
	original = readfile('/etc/modules')
	newstring = ''
	for line in original:
		if line.strip('\n') == replace:
			newstring += replace + '\n'
		newstring += line
	writefile('/etc/modules',newstring)
#modprobe ir_lirc_codec

def runCommand(command):
	command=command.split(' ')
	p = subprocess.Popen(command,stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

	help = subprocess.Popen(command,stdout=subprocess.PIPE)
	out = p.communicate
	for line in out[0].split('\n'):
		print line

def Bash(command):
	return subprocess.check_output(['bash','-c',command]).strip('\n').split('\n')

def findThis(command,pattern):
	try:
		Bash(command).index(pattern) 
		return 1
	except:
		return -1

def usbMenu(screen):
	screen.erase()
	#lsmod | grep -m1 g_
	currentGadget = "Current loaded gadget: "
	currentGadget += Bash("lsmod | grep -m1 g_ | awk '{print $1}'")[0] #current module loaded
	kernel = Bash("uname -r")[0]
	directory = "/lib/modules/" + kernel + "/kernel/drivers/usb/gadget/legacy"
	try:
		functionsSupported = Bash("ls "+directory)
		for x in range(len(functionsSupported)):
			functionsSupported[x] = functionsSupported[x].strip('.ko') #now its a nice list of gadgets
	except:
		functionsSupported = ["no usb gadget modules in your kernel"]
	title = "microUSB / USB OTG functions"
	screen.addstr(0,80/2-len(title)/2,title,curses.A_BOLD)
	screen.hline(1,0,'-',79)
	screen.addstr(2,80/2-len(currentGadget)/2,currentGadget,curses.A_BOLD)
	for x in range(len(functionsSupported)):
		screen.addstr(5+x,80/2-len(functionsSupported[x]),functionsSupported[x], curses.A_BOLD)
	
	#gadgetfs setup:
	try:
		Bash("modprobe libcomposite")
		Bash("mount -t configfs none /sys/kernel/config")#mount none cfg -t configfs?
		if findThis("ls /sys/kernel/config","usb_gadget") == 1:
			gadgetfs = "gadgetFS supported on this kernel"
	except:
		gadgetfs = "no gadgetFS support available"
	FUNCTIONS_USER_ENABLED=[]
#setup -> go through list of gadgets -> finish
#https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt
#https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget-ecm
#https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget-acm
#https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget-mass-storage

#this is where i got the initial stuff from: 
#https://github.com/ckuethe/usbarmory/wiki/USB-Gadgets
#http://isticktoit.net/?p=1383

#https://www.kernel.org/doc/Documentation/ABI/testing/

#nice demo here: https://s3.amazonaws.com/connect.linaro.org/sfo15/Presentations/09-23-Wednesday/SFO15-311-%20ConfigFS%20Gadgets-%20An%20Introduction.pdf
def setupGadget(serial=8349982, manuf="testing", product="multigadget"):
	topdir = "/sys/kernel/config/usb_gadget"
	Bash("mkdir -p "+topdir+"/g1")
	Bash("echo 0x1d6b > "+topdir+"/g1/idVendor") # Linux Foundation
	Bash("echo 0x104 > "+topdir+"/g1/idProduct") # Multifunction Composite Gadget
	Bash("echo 0x0100 > "+topdir+"/g1/bcdDevice") # v1.0.0
	Bash("echo 0x0200 > "+topdir+"/g1/bcdUSB") # USB2
	
	Bash("mkdir -p "+topdir+"/g1/strings/0x409") #0x409 for english language strings
	Bash("echo "+str(serial)+" > "+topdir+"/g1/strings/0x409/serialnumber")
	Bash("echo "+str(manuf)+" > "+topdir+"/g1/strings/0x409/manufacturer")
	Bash("echo "+str(product)+" > "+topdir+"/g1/strings/0x409/product")

def gadgetRNDIS():
	topdir = "/sys/kernel/config/usb_gadget/g1/"
	Bash("mkdir -p "+topdir+"functions/rndis.usb0")
	Bash("mkdir -p "+topdir+"configs/c.1")
	Bash("mkdir -p "+topdir+"configs/c.1/strings/0x409")
	Bash("echo 'Config 1: RNDIS network' > "+topdir+"configs/c.1/strings/0x409/configuration")
	Bash("echo 500 > "+topdir+"configs/c.1/MaxPower")
	Bash("ln -s "+topdir+"functions/rndis.usb0 "+topdir+"configs/c.1")
	#check for /etc/network/interfaces for a usb0 device and set that up according to user input
	#ex: static, dhcp, static but dnsmasq enabled, brctl, iptables for weird usb/ethernet dongle
	#static: address  netmask
	#dhcp: ifup usb0
	#static, but dnsmasq being served from 0.0.0.0
	#ifconfig usb0 0.0.0.0; ifconfig eth0 0.0.0.0; brctl addbr br0; brctl addif br0 eth0; brctl addif br0 usb0; ifup br0
	#iface br0 inet dhcp
	#	bridge_ports eth0 usb0
	#ifup br0

def finishGadget():
	topdir = "/sys/kernel/config/usb_gadget/g1/"
	Bash("echo 500 > "+topdir+"configs/c.1/MaxPower") # not until after right before attachment
	Bash("ls /sys/class/udc > "+topdir+"UDC") #finally attach functions to the hardware
	#if 'ethernet' in FUNCTIONS_USER_ENABLED:
		#ifup usb0

def disableGadget():
	Bash("echo '' > "+topdir+"UDC") #unlink 

if __name__ == '__main__':
	curses.wrapper(test,board)
