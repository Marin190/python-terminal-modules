# Modules for python-terminal

A list of modules for [python-terminal](https://github.com/Marin190/python-terminal) to extend terminal capabilities.

## Installation

1. Clone the python terminal repository:
```bash
git clone https://github.com/Marin190/python-terminal
cd terminal
```

2. Download the wanted modules python file in modules/ folder.
3. Install dependencies of the module if needed:
```bash
pip install -r requirements.txt
```
4. Run the terminal:
```bash
python terminal.py
```

## Commands

Refere to the README file of the module or the --help command if exist.

## Creating Custom Modules

You can extend the terminal's functionality by creating custom modules. Modules should be placed in the `modules` directory.

### Module Structure

Create a new Python file in the `modules` directory and refer to the modules/module_example.py for the basic structure.

### Module Guidelines

1. **File Name**: The module file name will be the command name (e.g., `mymodule.py` creates the `mymodule` command)

2. **Required Function**: Each module must have a `run_command(args)` function
   - `args`: String containing everything after your command name
   - The function handles all the module's logic

3. **Error Handling**: Always include proper error handling and usage messages

4. **Dependencies**: If your module requires external packages:
   - Document them in your module's header
   - Add them to the project's requirements.txt
   - Handle import errors gracefully

5. **Documentation**: Include:
   - Module description
   - Usage instructions
   - Examples
   - Required arguments
   - Optional flags


### Testing Your Module

1. Place your module in the `modules` directory
2. Start the terminal
3. Use `modules reload` to load your new module
4. Test your command
5. Use `modules list` to verify it's loaded

## License

This project is licensed under the MIT License - see the LICENSE file for details. 