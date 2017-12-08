#!/bin/bash

set -euo pipefail

now() {
  date +%FT%T%z
}

run_test() {
  python3 run.py
}

assert_stable() {
  for _ in {1..5}; do
    run_test | tr '\n' '##'
    echo
  done \
  | uniq \
  | tee >(sed 's/#\(.\)/\n\1/g;s/#//' >&2) \
  | [[ `wc -l` == 1 ]]
}

run_suite() {
  assert_stable
}

test_runner() {
  find -type d -name 'day[0-9]*' \
  | sort -rV \
  | while read dir; do
    echo >&2 "[[Dir $dir]]"
    {
      pushd "$dir"
      echo >&2 "[Start $(now)]"
      run_suite "$dir"
      echo >&2 "[Ended $(now)]"
      popd > /dev/null
    }
    echo >&2
  done
}

test_runner
