
# This is a module template for developpers
# You can delete this file without any problem

# The python file name is the command name (module_example.py -> module_example)
# Don't use generic names to avoid conflicts with existing commands
# Use this folder (modules) to create your own modules or download new
# The default folder (default) is used for default linux like terminal commands

# For more information about modules, see the documentation on github

# default function run when calling the module
def run_command(args): # args is the command line arguments
    if not args:
        print("Just a module example - show command usage : module_example <args>")
        return
    
    # if args are provided, print them
    else:
        print(f"Module example command received: {args}")
        return