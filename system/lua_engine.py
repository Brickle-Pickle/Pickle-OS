# lua_engine.py -> A simple Lua-to-Python transpiler and executor.
import re

class LuaScript:
    def __init__(self, filepath):
        self.filepath = filepath
        self.globals = {}
        self.code_py = ""
        self._load_and_transpile()
        self._execute_init()

    def _load_and_transpile(self):
        content = self._try_read(self.filepath)
        if content is None and self.filepath.startswith("/"):
            # Try without leading slash
            content = self._try_read(self.filepath[1:])
        
        # Try finding relative to current working directory explicitly
        if content is None:
             import uos
             try:
                 cwd = uos.getcwd()
                 # Try joining cwd with filepath (handling leading slash)
                 p = self.filepath if not self.filepath.startswith("/") else self.filepath[1:]
                 full_path = cwd + "/" + p
                 content = self._try_read(full_path)
             except:
                 pass

        if content is None:
            print(f"Error: Could not read {self.filepath}")
            # Debug info
            try:
                import uos
                print(f"CWD: {uos.getcwd()}")
                print(f"Files in CWD: {uos.listdir()}")
            except:
                pass
            return

        lua_code = content
        lines = lua_code.split('\n')
        py_lines = []
        indent = 0
        
        # Basic regex patterns
        # Note: This is a very limited subset of Lua for the specific use case.
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                py_lines.append("")
                continue

            # Calculate indent for this line
            current_indent = "    " * indent

            # Handle Comments (Full line)
            if line.startswith("--"):
                # Special Directive for Python Globals
                if line.startswith("-- py:"):
                    # Use current_indent instead of nothing, so it sits correctly inside functions
                    py_lines.append(current_indent + line[6:].strip())
                else:
                    py_lines.append("    " * indent + "# " + line[2:])
                continue

            # Strip inline comments
            if "--" in line:
                line = line.split("--")[0].strip()
                if not line: # If line becomes empty
                    continue

            # Handle indentation for the current line
            # current_indent = "    " * indent

            # Handle 'end' (dedent)
            
            # Handle 'end' (dedent)
            if line.startswith("end"):
                indent = max(0, indent - 1)
                py_lines.append("    " * indent + "# end")
                continue
            
            # Handle 'else' (dedent temporarily + indent)
            if line.startswith("else") and not line.startswith("elseif"):
                py_lines.append("    " * (indent - 1) + "else:")
                continue
            
            # Handle 'elseif'
            if line.startswith("elseif"):
                # convert "elseif condition then" to "elif condition:"
                cond = line[6:-4].strip() # remove elseif and then
                cond = self._map_operators(cond)
                py_lines.append("    " * (indent - 1) + f"elif {cond}:")
                continue

            # Handle indentation for the current line
            current_indent = "    " * indent
            
            # Handle Function Definition
            # function name(args)
            match_func = re.match(r"function\s+(\w+)\s*\((.*)\)", line)
            if match_func:
                name = match_func.group(1)
                args = match_func.group(2)
                py_lines.append(f"{current_indent}def {name}({args}):")
                indent += 1
                continue
            
            # Handle If
            # if condition then
            if line.startswith("if ") and line.endswith(" then"):
                cond = line[3:-5].strip()
                cond = self._map_operators(cond)
                py_lines.append(f"{current_indent}if {cond}:")
                indent += 1
                continue
                
            # Handle Single-line If: if cond then stmt end
            # Very basic support: assumes " then " and " end" exist
            if line.startswith("if ") and " then " in line and line.endswith(" end"):
                parts = line.split(" then ")
                cond = parts[0][3:].strip()
                stmt = parts[1][:-4].strip() # remove end
                cond = self._map_operators(cond)
                stmt = self._map_operators(stmt)
                py_lines.append(f"{current_indent}if {cond}: {stmt}")
                continue
                
            # Handle While
            # while condition do
            if line.startswith("while ") and line.endswith(" do"):
                cond = line[6:-3].strip()
                cond = self._map_operators(cond)
                py_lines.append(f"{current_indent}while {cond}:")
                indent += 1
                continue

            # Handle Return
            if line.startswith("return "):
                val = line[7:].strip()
                val = self._map_operators(val)
                py_lines.append(f"{current_indent}return {val}")
                continue

            # Handle Variable Declaration (local)
            # local x = 10 -> x = 10
            if line.startswith("local "):
                line = line[6:]
            
            # General Operator Mapping for the rest of the line
            line = self._map_operators(line)
            
            py_lines.append(f"{current_indent}{line}")

        self.code_py = "\n".join(py_lines)
        # Debug: print(self.code_py) 

    def _try_read(self, path):
        try:
            with open(path, 'r') as f:
                return f.read()
        except OSError:
            return None

    def _map_operators(self, text):
        # Maps Lua operators to Python
        text = text.replace("~=", "!=")
        text = text.replace(" nil", " None")
        text = text.replace("true", "True")
        text = text.replace("false", "False")
        # 'and', 'or', 'not' are the same usually, assuming spaces around them
        # Basic check for 'then' if it was missed (e.g. inline)
        return text

    def _execute_init(self):
        try:
            # We execute the code to define functions and variables in self.globals
            exec(self.code_py, self.globals)
        except Exception as e:
            print(f"Lua Transpilation/Execution Error: {e}")
            print("Generated Python Code:")
            print(self.code_py)

    def call(self, func_name, *args):
        if func_name in self.globals:
            try:
                return self.globals[func_name](*args)
            except Exception as e:
                print(f"Error calling {func_name}: {e}")
                return None
        else:
            # print(f"Function {func_name} not found in Lua script.")
            return None
