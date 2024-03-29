from contract.contract import Contract
from config.config import Config
import sys

def usage(args):
  space = " "*len(args[0])
  print("USAGE: ")
  print(f"{args[0]} config.json")
  print(f"{space  } ^^^^^^^^^^^")
  print(f"{space  } path to the configuration file")

def main():
  if len(sys.argv) <= 0:
    usage(sys.argv)
    return
  
  config = Config.from_json_file(sys.argv[1], publish=True)
  print(f"Deployed to {config.contract.address} ✅")

if __name__ == "__main__":
  main()