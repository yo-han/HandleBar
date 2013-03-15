from app import *
from lib import *
import json, sys

path = sys.argv[1];
guess = guessit.guess_movie_info(path, info = ['filename'])

print json.dumps(guess)