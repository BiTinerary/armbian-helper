#from importlib import import_module
# import os
import sys
sys.dont_write_bytecode = True # Avoid compiled byte code clutter, when executing/importing scripts from /menus folder.

## The following can be incorporated in begining of main armbian-helper script
supportedBoards = [] # Dynamic array of supported boards. Useful in case community adds more support/board files.
for file in os.listdir('%s\menus' % os.getcwd()):
	if file.endswith('.py') and file != '__init__.py': # Don't include __init__.py. There's prolly a better way to do this.
		supportedBoards.append(file.replace('.py', ''))
		#!! File names need to be titled exactly as bash command would output !!#
		
boardName = 'OPiOne' # subsititute for bash command to get board name

if boardName in supportedBoards:
	board = import_module('menus.%s' % boardName) # Properly import **ONLY** host board info
else:
	print "board isn't supported" # There is no python, support script with ASCII art and pin info for your board.
	# Is the supporting python script named correctly?

print board.boardArray # function/array names should be identical regardless of board type within 'support' script
print board.outline # Example
