#!/usr/bin/env python3

'''
----------------------------------------------------------------
Author : Alexis Rodriguez
Start date : 2020-02-26
End date : 

****************************************************************
Description : This tool will provide its user's with an easier 
way to gather information during the information gathering 
phase of a penetration test. The user has access to all tools 
installed on there machine must only worry about passing
invalid arguments to the prompts. 

****************************************************************
----------------------------------------------------------------
'''
try:
	# > import all objects from interface module
	from interface import *
	# > import sys for 
	import sys
	# > import os for performing terminal commands
	import os
	# > import threading for threading operations
	import threading
	# > import subprocess for executing bash commands
	import subprocess as subp
	# > import readline to add arrow key functionality
	import readline
# > check for importing error
except ImportError:
	print('%s [-] Error importing a module %s' % (fg(196), attr(0)))
	os.system('exit')

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 		Conv3ni3nt Class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Conv3ni3nt:
	def __init__(self, interface_obj):
		'''
		Initializing all necessary variables for this class

		params : the interface object that was instantiated in main
		'''
		
		# > create object to interact with interface
		self.interface = interface_obj
		# > print out signature screen
		self.interface.signature()
		# > list of tools that were entered
		self.tool_list = None


	def get_tools(self):
		'''
		displays the tools prompt and stores the tools in a list
		and returns the tool list
		'''

		# > display select tools prompt
		self.interface.tools_prompt()
		# > the tools that are specified
		tools = input('%sConv3%s> ' % (fg(self.interface.gray), attr(0)))
		# > if the user types in exit
		if 'exit' in tools:
			# > exit program
			sys.exit(0)
		else:
			# split the tools specified into a list
			received_tools = tools.split()
		# > set tool list
		self.tool_list = received_tools
		# > return tool list
		return received_tools


	def get_tool_options(self):
		'''
		will display the tool options prompt and record the options that were passed

		'''

		# > clear the terminal screen
		os.system('clear')
		# > print out my signature
		self.interface.signature()
		# > our list containing the options for each tool
		options_list = []
		# > prompt user for help menu
		print('%stype "help" for menu%s' % (fg(self.interface.rancolor), attr(0)))
		# > iterate over every tool and prompt user for the desired options
		for tool in self.tool_list:
			# > this addition is simply formating for our colored module
			tool = '%s' + tool + '%s'
			# > store user input in variable
			tool_option = input('enter ' + tool % (fg(self.interface.rancolor), attr(0)) + ' options : ')

			# > if exit is the inputed option, exit the program
			if 'exit' in tool_option:
				# > exit program
				sys.exit(0)
			else:
				# > append options to our list containing all tool options
				options_list.append(tool_option)
		# > return list of options
		return options_list


	def generate_file_name(self, tool_name, tool_options):
		'''
		this is another auxiliary function for generating convient file names
		Params : tool that is being used, the tools options
		'''
		# > if the option contains the following string
		# > cut the string out of the option
		if 'http://' in tool_options:
			# > getting appropiate substring
			tool_options = tool_options[7:]
		# > return the file name
		return tool_name + ' ' + tool_options


	def start_tool(self, tool, tool_options):
		'''
		start the tool with the options that were specified
		
		Params : the name of the tool, the options for the tool
		'''

		# > subprocess.run requires a list when stdout is not directed to shell
		# > so converting our command string to a list)
		command = (tool + ' ' + ''.join(tool_options)).split()
		# > if user types in help, display the tools menu
		if tool_options == 'help':
			# > call the tool without any arguments
			# > which will display menu for most tools
			subp.run(tool, shell=True)
			# > prompt user to verify if they would like to go back to the tool options screen 
			go_back = input('%stype "back" to go back to tool prompt: %s' % (fg(self.interface.red), attr(0)))
			# > if input is back then display options screen
			if go_back.strip() == 'back':
				# > return to previous display
				self.return_to_options_prompt(tool)
		# > if the use does not type in help, do the following
		else:
			# > try opening file
			try:
				# > get file name to create
				file_name = self.generate_file_name(tool, tool_options)
			# throw exception
			except:
				print('%Serror creating file%s' % (fg(self.interface.lightyellow), attr(0)))
				# > exit program
				os.system('clear')
			# > create thread
			thread = threading.Thread(target=self.create_thread,
										args=(file_name, command,))
			# > start thread
			thread.start()


	def return_to_options_prompt(self, tool):
		'''
		this is an auxiliary function for returning to the tool prompt display

		params : tool that is currently being used
		'''

		# > display tool options prompt
		tool_options = self.get_tool_options()
		# > a little recursion going on here
		self.start_tool(tool, tool_options)


	def create_thread(self, file_arg, command):
		'''
		start each tool on a different thread

		params : the name of thee file, the command to execute
		'''

		# > open file created for writing
		with open(file_arg, 'w') as tool_file:
		# > use the tool with its options and direct output to file
			subp.run(command,
				# > redirecting stdout to file
				stdout=tool_file, 
				# > redirecting std err to stdout
				stderr=subp.STDOUT,
				# > save data a normal text
				text=True)


# %%%%%%%%%%%%%%%%
# 		MAIN      
# %%%%%%%%%%%%%%%%
def initiate():
	# > clear screan
	os.system('clear')
	# > instantiate Interface object
	display = Interface()
	# > instantiate Conv3i3nt object
	conv3_obj = Conv3ni3nt(display)
	# > returns list of inputed tools
	tools_lst = conv3_obj.get_tools()
	# > returns a list of options specified for each tool
	tool_options = conv3_obj.get_tool_options()
	# > zip up both the tool and tool options
	# > and send the variable to the function that'll start the tool
	for tool, options in zip(tools_lst, tool_options):
		# > call function to which start tool
		conv3_obj.start_tool(tool, options)

	display.success_bar()


if __name__ == '__main__':
	initiate()