# https://regex101.com/r/PQ9g6g/5

import os.path
import sys
import re
from maps import shift_map, mod_keys, base_keys

help_info = '''
  Usage: parse_UKBD [OPTIONS] [INPUT FILE]
    -o fileName.txt   output file
    -v                verbose  (Default if -o is not present.)
    -t                tuple mode (mod_key_1, ..., mod_key_N, base_key)
    -h                help
    
  This program parses hex data from captured USB keyboard packets. Each line of input should have one base key and up to one mod key. Each line should be 4 or 8 bytes. Tuple mode is harder to read, but should offer more context if mod keys are important.

'''

# run options
cl_args_regex = '^(?P<HELP>-{0,2}h(?:elp)?)(?:.*)|(?:(?: |^)(?P<OPT>(?: ?-{0,2}[ovht])+)(?:(?: |^)(?P<OUT>[\w\-.]+|[\'\"][\w\-. ]+[\'\"]))?)?(?: |^)(?P<IN>[\w\-.]+|[\'\"][\w\-. ]+[\'\"])?$'
cl_args = ' '.join(sys.argv[1:])
cl_args_matches = re.search(cl_args_regex, cl_args)
cl_args_HELP = cl_args_matches.group('HELP')
cl_args_OPT = cl_args_matches.group('OPT')
cl_args_OUT = cl_args_matches.group('OUT')
cl_args_IN = cl_args_matches.group('IN')
cl_args = {
  'HELP' : cl_args_matches.group('HELP'),
  'OPT' : cl_args_matches.group('OPT'),
  'OUT' : cl_args_matches.group('OUT'),
  'IN' : cl_args_matches.group('IN'),
  'ERROR' : False,
  'o' : False,
  'v' : False,
  'h' : False,
  't' : False
}

# run states (environment assumptions)
run_state = None
'''
run_input_only = 0
run_options_input = 1
run_options_output_input = 2
'''

# Was the input file specified?
if cl_args['IN']:
  # Were any options specified?
  if cl_args['OPT']:
    # Attempt to parse option flags.
    for i in cl_args['OPT']:
      if i not in ' -ovht':
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

print(cl_args, run_state)





'''
(?=(?:-{0,2}[ot(?P<V>v)]{1,3}))?(?=(?P<T>-{0,2}t))?(?=(?:-{0,2}o))?
(?=(?P<T>-{0,2}t))?(?=(?:-{0,2}o))?

^(?:.*-{0,2}(?P<OPT>[ovht]{1,4})((?<=o)[ovht]*\s+(?P<OF>[\w\-. ]+))?)\s*(?P<IF>[\w\-. ]+)?$

^(?:.*?-{0,2}(?P<OPT>[ovht]+))*\s(?P<IN>[\w\-. ]+)$
^(?:-{0,2}(?P<OPT>[ovht]+)[ \t]+)*(?:(?<=o)([ovht]*[ \t]+(?P<OUT>[\w\-. ]+)[ \t]*))*(?P<IN>[\w\-. ]+)?$

(?P<HELP>-{0,2}h(?:elp)?)|(?:-{0,2}(?P<OPT>[vt]+)\s(?P<IN>[\w\-. ]+))
(?P<HELP>-{0,2}h(?:elp)?)|(?P<OPT> ?-{0,2}[vt]+)*\s(?P<IN>[\w\-. ]+)
(?P<HELP>-{0,2}h(?:elp)?)|(?P<OPT>(-{0,2}[vt]+ )*)(?P<IN>[\w\-.]+|"[\w\-. ]+")

(?P<HELP>-{0,2}h(?:elp)?)(?:.*)|(?P<OPT>(?:-{0,2}[vt]+ )*)(?P<IN>[\w\-.]+|"[\w\-. ]+")

(?P<HELP>-{0,2}h(?:elp)?)(?:.*)|(?P<OPT>(?:-{0,2}[ovt]+ )*)(?<=o)(?: (?P<OUT>[\w\-.]+|"[\w\-. ]+") )(?P<IN>[\w\-.]+|"[\w\-. ]+")
(?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?'OPT'(?: ?-{0,2}[ovt]+)*)(?<=o)(?: (?'OUT'[\w\-.]+|['"][\w\-. ]+['"]) )(?'IN'[\w\-.]+|['"][\w\-. ]+['"])

(?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?'OPT'(?:-{0,2}[ovt]+))+ ((?<=o)(?:(?'OUT'[\w\-.]+|['"][\w\-. ]+['"]) ))?(?'IN'[\w\-.]+|['"][\w\-. ]+['"])

(?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?:(?'OPT'(?:-{0,2}[ovt]+))+ ((?<=o)(?:(?'OUT'[\w\-.]+|['"][\w\-. ]+['"]) ))?)?(?'IN'[\w\-.]+|['"][\w\-. ]+['"])

  (?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?:(?'OPT'(?:-{0,2}[ovt]+))+ ((?<=o)(?:(?'OUT'[\w\-.]+|['"][\w\-. ]+['"]) ))?)?(?'IN'[\w\-.]+|['"][\w\-. ]+['"])(?'junk'(?:.)*)?
  (?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?:(?'OPT'(?:-{0,2}[ovt]+))+ (?'OUT'(?<=o)[\w\-.]+|['"][\w\-. ]+['"] )?)?(?'IN'[\w\-.]+|['"][\w\-. ]+['"])(?'junk'(?:.)*)?
  
    (?'HELP'-{0,2}h(?:elp)?)(?:.*)| |((?'OPT'(?:-{0,2}[ovt]+ ?)) (?'OUT'[\w\-.]+|['"][\w\-. ]+['"] ))+(?'IN'[\w\-.]+|['"][\w\-. ]+['"])(?'junk'(?:.)*)?
    (?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?'OPT'(?:-{0,2}[vt]+ ?)+)?(?'IN'[\w\-.]+|['"][\w\-. ]+['"])(?'junk'(?:.)*)?|((?'OPT2'(?:-{0,2}[ovt]+ ?)) (?'OUT'[\w\-.]+|['"][\w\-. ]+['"] ))+(?'IN2'[\w\-.]+|['"][\w\-. ]+['"])(?'junk2'(?:.)*)?
  
  (?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?:(?'OPT'(?: ?-{0,2}[ovt]+))(?<=o[vt-])(?: (?'OUT'[\w\-.]+|['"][\w\-. ]+['"] )))*(?'IN'[\w\-.]+|['"][\w\-. ]+['"])(?'junk'(?:.)*)?
  ^(?'HELP'-{0,2}h(?:elp)?)(?:.*)|(?:(?'OPT'(?: ?-{0,2}[ovt]+))(?<=o[vt-])(?: (?'OUT'[\w\-.]+|['"][\w\-. ]+['"] )))*(?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
  ^(?'HELP'-{0,2}help)(?:.*)|(?:(?'OPT' ?-{0,2}[ovht]+)(?<=o[vt])(?: (?'OUT'[\w\-.]+|['"][\w\-. ]+['"] )))*(?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
    ^(?'HELP'-{0,2}help)(?:.*)|(?'OPT'(?:-{0,2}[ovht]+ ?)+)? (?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
    ^(?'HELP'-{0,2}help)(?:.*)|(?'OPT'(?:-{0,2}[ovht]+))?(?: ?(?'IN'[\w\-.]+|['"][\w\-. ]+['"]))?$
    ^(?'HELP'-{0,2}help)(?:.*)|(?'OPT'(?:-{0,2}[vht] ?)+)?(?:-{0,2}(?'O'o) (?'OUT'[\w\-.]+|['"][\w\-. ]+['"] ))?(?: ?(?'IN'[\w\-.]+|['"][\w\-. ]+['"]))?$
    ^(?'HELP'-{0,2}help)(?:.*)|(?'OPT'(?: ?-{0,2}[ovht])+)? ?(?'OUT'[\w\-.]+|['"][\w\-. ]+['"])? ?(?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
    
    ^(?'HELP'-{0,2}help)(?:.*)|(?'OPT'(?: ?-{0,2}[ovht])+)?(?: |^)(?'OUT'[\w\-.]+|['"][\w\-. ]+['"])?(?: |^)(?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
    https://regex101.com/r/PQ9g6g/1
    https://regex101.com/r/PQ9g6g/3/
      ^(?'HELP'-{0,2}help)(?:.*)|(?'OPT'(?: ?-{0,2}[ovht])+((?: |^)(?'OUT'[\w\-.]+|['"][\w\-. ]+['"]))?)?(?: |^)(?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
      ^(?'HELP'-{0,2}help)(?:.*)|(?:(?: |^)(?'OPT'(?: ?-{0,2}[ovht])+)(?:(?: |^)(?'OUT'[\w\-.]+|['"][\w\-. ]+['"]))?)?(?: |^)(?'IN'[\w\-.]+|['"][\w\-. ]+['"])$
'''    

  