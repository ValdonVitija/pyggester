import sys
from pyggester.cli import get_app


PYGGESTER_LOGO = """
                                            _____             
_____________  ________ _______ ______________  /_____________
___  __ \_  / / /_  __ `/_  __ `/  _ \_  ___/  __/  _ \_  ___/
__  /_/ /  /_/ /_  /_/ /_  /_/ //  __/(__  )/ /_ /  __/  /    
_  .___/_\__, / _\__, / _\__, / \___//____/ \__/ \___//_/     
/_/     /____/  /____/  /____/                                
"""


def main():
    args = " ".join(sys.argv[1:])
    if (not args or "--help" in args) and len(sys.argv) < 3:
        print(PYGGESTER_LOGO)
    get_app()


if __name__ == "__main__":
    main()
