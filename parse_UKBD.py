# https://regex101.com/r/PQ9g6g/5

import os.path
import sys
import re
from maps import shift_map, mod_keys, base_keys

help_info = '''
  Usage: parse_UKBD [OPTIONS] [INPUT FILE]
    -o fileName.txt   Output file
    -v                Verbose  (Default if -o is not present.)
    -c                Confirm targets before file I/O.
    -t                Tuple mode (mod_key_1, ..., mod_key_N, base_key)
    -h                Help
    
  This program parses hex data from captured USB keyboard packets. Each line of input should have one base key and up to one mod key. Each line should be 4 or 8 bytes. Tuple mode is harder to read, but should offer more context if mod keys are important.

'''

# run options
cl_args = {}

# run states (environment assumptions)
run_state = None
'''
run_input_only = 0
run_options_input = 1
run_options_output_input = 2
'''

# Returns a dictionary with the results of parsing the command line args, and sets the program's run_state.
def parse_args():
  global run_state
  global cl_args
  cl_args_regex = '^(?P<HELP>-*h(?:elp)?)(?:.*)|(?:(?: |^)(?P<OPT>(?: ?-*[ovcht])+)(?:(?: |^)(?P<OUT>[\w\-.]+|[\'\"][\w\-. ]+[\'\"]))?)?(?: |^)(?P<IN>[\w\-.]+|[\'\"][\w\-. ]+[\'\"])?$'
  cl_args = ' '.join(sys.argv[1:])
  cl_args_matches = re.search(cl_args_regex, cl_args)
  cl_args = {
    'HELP' : cl_args_matches.group('HELP'),
    'OPT' : cl_args_matches.group('OPT'),
    'OUT' : cl_args_matches.group('OUT'),
    'IN' : cl_args_matches.group('IN'),
    'ERROR' : False,
    'o' : False,
    'v' : False,
    'c' : False,
    'h' : False,
    't' : False
  }
  
  # Was the input file specified?
  if cl_args['IN']:
    # Were any options specified?
    if cl_args['OPT']:
      # Attempt to parse option flags.
      for i in cl_args['OPT']:
        if i not in ' -ovcht':
          cl_args['ERROR'] = True
          break
        if i in cl_args:
          cl_args[i] = True
      # Check if an output file was specified.
      if not cl_args['ERROR']:
        # Output file expected.
        if cl_args['o']:
          if not cl_args['OUT']:
            cl_args['ERROR'] = True
          run_state = 'run_options_output_input'
        else:
          # Output file not expected.
          if cl_args['OUT']:
            cl_args['ERROR'] = True
          run_state = 'run_options_input'
    else:
      run_state = 'run_input_only'
  else:
    cl_args['ERROR'] = True
  return not cl_args['ERROR']



def main():
  if not parse_args():
    print(help_info)
  
  print(cl_args, run_state)



if __name__ == '__main__':
  main()
