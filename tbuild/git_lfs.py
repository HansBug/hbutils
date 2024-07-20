import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Custom Git version reporter", add_help=False)
    parser.add_argument('command', nargs='*', help="Command to execute")

    args, unknown = parser.parse_known_args()

    if '--version' in sys.argv:
        print("git version 2.30.0")
        sys.exit(0)
    elif args.command == ['lfs', 'version']:
        print("git-lfs/2.13.3 (GitHub; linux amd64; go 1.16.2)")
        sys.exit(0)
    else:
        print("Unknown command", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
