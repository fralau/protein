"""
The terminal client
"""
import sys
import traceback
import yaml
import pprint

import argparse
import json
import hjson


from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


from .core import Interpreter
from .util import load_yaml

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="YAML Preprocessor: modules, parameters, env(), and conditional blocks"
    )
    parser.add_argument("file", help="Path to the YAML config file")
    parser.add_argument("-o", "--output", help="Write rendered output to file")
    parser.add_argument("--show-raw", action="store_true", help="Show original YAML before processing")
    parser.add_argument(
        "-f", "--format",
        choices=["yaml", "json", "hjson", "python"],
        default="yaml",
        help="Output format (default: yaml)"
    )
    args = parser.parse_args()

    yamlpp = load_yaml(args.file)
    
    if args.show_raw:
        console.print(
            Panel(
                Syntax(yamlpp, "yaml", theme="monokai", line_numbers=True),
                title="[bold magenta]Original YAML[/bold magenta]"
            )
        )

    try:
        interpreter = Interpreter(yamlpp)
        tree = interpreter.render_tree()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        traceback.print_exc()   # print on stderr
        raise SystemExit(1)

    # Format conversion
    if args.format == "yaml":
        rendered = yaml.dump(tree, sort_keys=False)
        syntax_lang = "yaml"
    elif args.format == "json":
        rendered = json.dumps(tree, indent=2)
        syntax_lang = "json"
    elif args.format == "hjson":
        rendered = hjson.dumps(tree, indent=2)
        syntax_lang = "json"  # hjson is close enough for syntax highlighting
    elif args.format == "python":
        rendered = pprint.pformat(tree, indent=2, width=80)
        syntax_lang = "python"

    # Pretty print if interactive
    syntax = Syntax(rendered, syntax_lang, theme="monokai", line_numbers=True)
    if sys.stdout.isatty():
        console.print(Panel(syntax, title=f"[bold green]Rendered {args.format.upper()}[/bold green]"))
    else:
        print(rendered)

    # Write to file if requested
    if args.output:
        with open(args.output, "w") as f:
            f.write(rendered)
        console.print(f"[bold yellow]Written to {args.output}[/bold yellow]")
