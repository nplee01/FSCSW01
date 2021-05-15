#!/usr/bin/env python
import secrets
import os, sys, argparse, re
from pathlib import Path
# Generate .env from an input env template

# Instantiate command line args parser
par = argparse.ArgumentParser(prog="gen_env", description="Generate .env file for an input template while replacing secrets")
# Input env file template, eg prod.env
par.add_argument('InFile', metavar='infile', type=str, 
        help="Input template env file to be processed")
par.add_argument('-o', '--output', dest='outfile', type=str, help="Optionally output to this file else .env")

args = par.parse_args()

infile = args.InFile

if not os.path.isfile(infile):
    print(f"File {infile} does not exist")
    sys.exit(2)

# We output file in the same directory as input file
WORK_DIR = Path(infile).resolve().parent
# Secret to be replaced
pwd = secrets.token_urlsafe()[:10]
sec = secrets.token_urlsafe()
fixpwd = secrets.token_urlsafe()[:10]
pgpwd = secrets.token_urlsafe()[:10]
# These replace patterns must match what is in template file.
pg1 = re.compile('ReplaceWorkDirectory')
pg2 = re.compile('ReplaceDBPassword')
pg3 = re.compile('ReplaceSecretKey')
pg4 = re.compile('ReplaceFixPassword')

# Output file default is .env if not supplied
outfile = args.outfile or '.env'

with open(WORK_DIR / outfile, 'w') as outf:
    with open(infile) as inf:
        outf.write(f"# Env vars generated with random secrets from {infile}")
        for line in inf:
            if pg1.search(line):
                outf.write(pg1.sub(str(WORK_DIR), line))
            elif pg2.search(line):
                outf.write(pg2.sub(pwd, line))
            elif pg3.search(line):
                outf.write(pg3.sub(sec, line))
            elif pg4.search(line):
                outf.write(pg4.sub(fixpwd, line))
            elif line.startswith('#'):
                pass
            else:
                outf.write(line)
