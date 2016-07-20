import argparse
import sys
import subprocess

parser = argparse.ArgumentParser(description = 'stashcp')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('-r', action='store_true', help='recursively copy')
parser.add_argument('-s', dest='source', help='source')
parser.add_argument('-d', dest='destination', help='destination')
parser.add_argument('--closest', action='store_true')
args=parser.parse_args()

def find_closest():
    closest=subprocess.Popen(['./get_best_stashcache.py', '0'], stdout=subprocess.PIPE)
    cache=closest.communicate()[0].split()[0]
    return cache

if not args.closest:
    if args.source is None or args.destination is None:
        parser.error('without --closest, *both* -s source *and* -d destination are required')
else:
    print find_closest()
    sys.exit()


