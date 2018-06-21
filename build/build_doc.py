import afs
import sys
import pydoc

def output_help_to_file(filepath, request):
    with open(filepath, 'w') as f:
        sys.stdout = f
        pydoc.help(request)
    sys.stdout = sys.__stdout__


output_help_to_file('afs.config_handler.txt', 'afs.config_handler')
output_help_to_file('afs.models.txt', 'afs.models')
