#!/usr/bin/env python3

import argparse
import requests
import re

def fetch_and_store(tap, formula):
  org, repo = tap.split("/", 2)
  url = f"https://raw.githubusercontent.com/{org}/homebrew-{repo}/master/Formula/{formula}.rb"
  print(f"Fetching... {url}")
  res = requests.get(url)
  depends_on_regex = r"""depends_on\s["']([^"']+)["']"""
  dependencies = []
  with open(f"Formula/{formula}.rb", "w") as outfile:
      for line in res.iter_lines():
          line = line.decode("utf-8")
          match = re.search(depends_on_regex, line)
          if not match:
              outfile.write(line)
          else:
              dependency = match.group(1)
              dependencies.append(dependency)
              outfile.write(line.replace(dependency, f"ParticleHealth/taps/{dependency}"))
          outfile.write('\n')

  for dependency in dependencies:
      fetch_and_store(tap, dependency)

def main(tap, formula):
  fetch_and_store(tap, formula)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Download formula and save them to this tap.')
  parser.add_argument('--tap', type=str, help='Tap to fetch the formula from', default='homebrew/core')
  parser.add_argument('formula', type=str, help='Tap to fetch the formula from', default='homebrew/core')
  args = parser.parse_args()
  main(args.tap, args.formula)
