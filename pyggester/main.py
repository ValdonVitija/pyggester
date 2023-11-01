import sys

PYGGESTER_LOGO = """
                                      _               
 ____  _   _  ____  ____ _____  ___ _| |_ _____  ____ 
|  _ \| | | |/ _  |/ _  | ___ |/___|_   _) ___ |/ ___)
| |_| | |_| ( (_| ( (_| | ____|___ | | |_| ____| |    
|  __/ \__  |\___ |\___ |_____|___/   \__)_____)_|    
|_|   (____/(_____(_____|                                                    
"""


def main():
    args = " ".join(sys.argv[1:])
    if (not args or "--help" in args) and len(sys.argv) < 3:
        print(PYGGESTER_LOGO)
    # call the cli app starter
    pass


if __name__ == "__main__":
    main()
