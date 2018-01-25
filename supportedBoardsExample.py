from importlib import import_module
import os

supportedBoards = []

for file in os.listdir('%s\menus' % os.getcwd()):
	if file.endswith('.py') and file != '__init__.py':
		supportedBoards.append(file.replace('.py', ''))

print supportedBoards
boardName = 'OPiOne'

if boardName in supportedBoards:
	board = import_module('menus.%s' % boardName)
else:
	print "board isn't supported"

print board.boardArray
print board.outline