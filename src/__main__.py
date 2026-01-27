"""Py-Drive entry point script."""
# src/___main__.py

from src import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__=="__main__":
    main()