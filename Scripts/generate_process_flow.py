import os
import ast
from collections import defaultdict
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_MD = os.path.join(PROJECT_ROOT, 'ProcessFlow.MD')

EXCLUDE_DIRS = {'venv', '__pycache__', 'logs', 'static', 'test_workflows', 'projects', 'n8n_builder.egg-info', '.git', '.pytest_cache'}

FASTAPI_DECORATORS = {'get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'websocket', 'api_route'}

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = set()
        self.raises = set()
        self.handles = set()
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            self.calls.add(ast.unparse(node.func))
        elif isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        self.generic_visit(node)
    def visit_Raise(self, node):
        if node.exc:
            if isinstance(node.exc, ast.Call):
                if isinstance(node.exc.func, ast.Name):
                    self.raises.add(node.exc.func.id)
                elif isinstance(node.exc.func, ast.Attribute):
                    self.raises.add(ast.unparse(node.exc.func))
        self.generic_visit(node)
    def visit_Try(self, node):
        for handler in node.handlers:
            if handler.type:
                if isinstance(handler.type, ast.Name):
                    self.handles.add(handler.type.id)
                elif isinstance(handler.type, ast.Attribute):
                    self.handles.add(ast.unparse(handler.type))
        self.generic_visit(node)

class ModuleAnalyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.imports = set()
        self.third_party_imports = set()
        self.classes = {}
        self.class_bases = {}
        self.functions = {}
        self.function_docstrings = {}
        self.class_docstrings = {}
        self.calls = defaultdict(set)
        self.raises = defaultdict(set)
        self.handles = defaultdict(set)
        self.endpoints = set()
        self.entry_points = set()
        self.globals = {}
        self.constants = {}
        self.module_docstring = None
        self.current_class = None
        self.current_function = None
        self._find_module_docstring = True
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
            if not alias.name.startswith('.') and not alias.name.startswith(self.filename.split(os.sep)[0]):
                if not alias.name.split('.')[0] in ('os', 'sys', 'ast', 'collections', 're', 'typing', 'datetime', 'time', 'json', 'logging', 'uuid', 'concurrent', 'threading', 'pathlib', 'dataclasses', 'enum'):
                    self.third_party_imports.add(alias.name)
    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
            if not node.module.startswith('.') and not node.module.startswith(self.filename.split(os.sep)[0]):
                if not node.module.split('.')[0] in ('os', 'sys', 'ast', 'collections', 're', 'typing', 'datetime', 'time', 'json', 'logging', 'uuid', 'concurrent', 'threading', 'pathlib', 'dataclasses', 'enum'):
                    self.third_party_imports.add(node.module)
    def visit_ClassDef(self, node):
        self.classes[node.name] = node.lineno
        self.class_docstrings[node.name] = ast.get_docstring(node).split('\n')[0] if ast.get_docstring(node) else ''
        self.class_bases[node.name] = [ast.unparse(base) for base in node.bases] if node.bases else []
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None
    def visit_FunctionDef(self, node):
        func_name = node.name
        self.functions[func_name] = node.lineno
        self.function_docstrings[func_name] = ast.get_docstring(node).split('\n')[0] if ast.get_docstring(node) else ''
        visitor = FunctionCallVisitor()
        visitor.visit(node)
        for call in visitor.calls:
            self.calls[func_name].add(call)
        for exc in visitor.raises:
            self.raises[func_name].add(exc)
        for exc in visitor.handles:
            self.handles[func_name].add(exc)
        # FastAPI endpoint detection
        if node.decorator_list:
            for dec in node.decorator_list:
                if isinstance(dec, ast.Attribute) and dec.attr in FASTAPI_DECORATORS:
                    self.endpoints.add(func_name)
                elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and dec.func.attr in FASTAPI_DECORATORS:
                    self.endpoints.add(func_name)
        # CLI entry point detection
        if func_name == 'main' or (node.name == '__main__'):
            self.entry_points.add(func_name)
        self.current_function = func_name
        self.generic_visit(node)
        self.current_function = None
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name.isupper():
                self.constants[name] = getattr(node.value, 'value', None)
            else:
                self.globals[name] = getattr(node.value, 'value', None)
        self.generic_visit(node)
    def visit_Expr(self, node):
        if self._find_module_docstring and isinstance(node.value, ast.Str):
            self.module_docstring = node.value.s.split('\n')[0]
            self._find_module_docstring = False
        self.generic_visit(node)

def find_py_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if filename.endswith('.py'):
                yield os.path.join(dirpath, filename)

def analyze_codebase(root):
    modules = {}
    for pyfile in find_py_files(root):
        rel_path = os.path.relpath(pyfile, root)
        try:
            with open(pyfile, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filename=pyfile)
            analyzer = ModuleAnalyzer(rel_path)
            analyzer.visit(tree)
            modules[rel_path] = analyzer
        except Exception as e:
            print(f"Error parsing {rel_path}: {e}")
    return modules

def write_process_flow_md(modules, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Project Process Flow\n\n")
        f.write(f"Generated by Scripts/generate_process_flow.py\n\n")
        f.write(f"## Module Summary\n\n")
        for mod, analyzer in modules.items():
            f.write(f"- **{mod}**: {len(analyzer.classes)} classes, {len(analyzer.functions)} functions, {len(analyzer.imports)} imports\n")
        f.write(f"\n---\n\n")
        for mod, analyzer in modules.items():
            f.write(f"## Module: `{mod}`\n\n")
            if analyzer.module_docstring:
                f.write(f"*Module docstring:* {analyzer.module_docstring}\n\n")
            if analyzer.imports:
                f.write(f"**Imports:** {', '.join(sorted(analyzer.imports))}\n\n")
            if analyzer.third_party_imports:
                f.write(f"**Third-party packages:** {', '.join(sorted(analyzer.third_party_imports))}\n\n")
            if analyzer.constants:
                f.write(f"**Constants:**\n")
                for cname, val in analyzer.constants.items():
                    f.write(f"  - `{cname}` = {val}\n")
                f.write("\n")
            if analyzer.globals:
                f.write(f"**Global Variables:**\n")
                for gname, val in analyzer.globals.items():
                    f.write(f"  - `{gname}` = {val}\n")
                f.write("\n")
            if analyzer.classes:
                f.write(f"**Classes:**\n")
                for cname, lineno in analyzer.classes.items():
                    doc = analyzer.class_docstrings.get(cname, '')
                    bases = analyzer.class_bases.get(cname, [])
                    base_str = f" (inherits: {', '.join(bases)})" if bases else ''
                    doc_str = f" - {doc}" if doc else ''
                    f.write(f"  - `{cname}` (line {lineno}){base_str}{doc_str}\n")
                f.write("\n")
            if analyzer.functions:
                f.write(f"**Functions:**\n")
                for fname, lineno in analyzer.functions.items():
                    doc = analyzer.function_docstrings.get(fname, '')
                    endpoint = ' [FastAPI endpoint]' if fname in analyzer.endpoints else ''
                    entry = ' [Entry point]' if fname in analyzer.entry_points else ''
                    doc_str = f" - {doc}" if doc else ''
                    f.write(f"  - `{fname}` (line {lineno}){endpoint}{entry}{doc_str}\n")
                f.write("\n")
            if analyzer.calls:
                f.write(f"**Function Call Graph:**\n")
                for fname, calls in analyzer.calls.items():
                    if calls:
                        f.write(f"  - `{fname}` calls: {', '.join(sorted(calls))}\n")
                f.write("\n")
            if analyzer.raises:
                f.write(f"**Functions that raise exceptions:**\n")
                for fname, excs in analyzer.raises.items():
                    if excs:
                        f.write(f"  - `{fname}` raises: {', '.join(sorted(excs))}\n")
                f.write("\n")
            if analyzer.handles:
                f.write(f"**Functions that handle exceptions:**\n")
                for fname, excs in analyzer.handles.items():
                    if excs:
                        f.write(f"  - `{fname}` handles: {', '.join(sorted(excs))}\n")
                f.write("\n")
            f.write(f"---\n\n")
        # Optionally, add a Mermaid diagram for top-level function calls
        f.write("## Top-Level Call Graph (Mermaid)\n\n")
        f.write("```mermaid\ngraph TD\n")
        for mod, analyzer in modules.items():
            for fname, calls in analyzer.calls.items():
                for call in calls:
                    f.write(f"    {mod.replace('/', '_').replace('.', '_')}_{fname} --> {call}\n")
        f.write("```\n")
    print(f"Process flow written to {output_path}")

def main():
    modules = analyze_codebase(PROJECT_ROOT)
    write_process_flow_md(modules, OUTPUT_MD)

if __name__ == "__main__":
    main() 