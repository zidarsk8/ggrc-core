# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

set -o nounset
set -o errexit

project_name () {
  # Get propper project name
  # args:
  #  -p: if set the project name will be the name of the repo parent folder.
  #  -d: default project name, if parent folder is not set or valid.
  # returns: project name containing only alphanumeric characters

  # parse the command line options
  while [[ "$#" -gt 0 ]]
  do
    OPT_NAME="$1"

    case $OPT_NAME in
      -p|--parent)
        RESULT=$( cd "$(dirname "$0")/../.." ; echo ${PWD##*/}  )
      ;;
      -d|--default)
        DEFAULT="$2"
        shift  # extra shift for the current options's value
      ;;
      *)  # an unknown option found
      ;;
    esac
    shift  # drop the just-processed option/argument
  done
  if [[ -n "${RESULT:-}" ]]; then
    echo "${RESULT:-}" | sed 's/[^A-Za-z0-9]//g'
  else
    echo "${DEFAULT:-}" | sed 's/[^A-Za-z0-9]//g'
  fi
}

setup () {
  if [ -z "${1:-}" ]; then
    echo "Missing mandatory project parameter"
    exit 1
  else
    PROJECT="${1}"
  fi

  git submodule update --init

  docker-compose --file docker-compose-testing.yml \
    --project-name ${PROJECT} \
    build

  docker-compose --file docker-compose-testing.yml \
    --project-name ${PROJECT} \
    up --force-recreate -d

  if [[ $UID -eq 0 ]]; then
    # Allow users inside the containers to access files.
    chown 1000 -R .
  elif [[ $UID -ne 1000 ]]; then
    echo "These tests must be run with UID 1000 or 0. Your UID is $UID"
    exit 1
  fi

  echo "Provisioning ${PROJECT}_dev_1"
  docker exec -i ${PROJECT}_dev_1 su vagrant -c "
    source /vagrant/bin/init_vagrant_env
    make bower_components > /dev/null
    ln -s /vagrant-dev/node_modules /vagrant/node_modules
    build_css
    build_assets
  "
}

teardown () {
  if [ -z "${1:-}" ]; then
    echo "Missing mandatory project parameter"
    exit 1
  else
    PROJECT="${1}"
  fi

  docker-compose -p ${PROJECT} stop
}

print_line () {
echo "
###############################################################################
"
}

integration_tests () {
  PROJECT=$1
  print_line

  echo "Running ${PROJECT}"
  docker exec -i ${PROJECT}_dev_1 su vagrant -c "
    source /vagrant/bin/init_vagrant_env
    /vagrant/bin/run_integration
  " && rc=$? || rc=$?

  print_line
  return $rc
}


selenium_tests () {
  PROJECT=$1
  print_line

  echo "Running Test server"
  docker exec -id ${PROJECT}_dev_1 /vagrant/bin/launch_ggrc_test

  echo "Running Selenium tests"
  docker exec -i ${PROJECT}_selenium_1 sh -c "
    python /selenium/src/run_selenium.py --junitxml=/selenium/logs/selenium.xml
  " && rc=$? || rc=$?

  mv ./test/selenium/logs/selenium.xml ./test/selenium.xml || true

  print_line
  return $rc
}


unittests_tests () {
  PROJECT=$1
  print_line
  
  echo "Running python unit tests"
  docker exec -i ${PROJECT}_dev_1 su vagrant -c "
    source /vagrant/bin/init_vagrant_env
    /vagrant/bin/run_unit
  " && unit_rc=$? || unit_rc=$?
  
  [[ unit_rc -eq 0 ]] && echo "PASS" || echo "FAIL"
  
  print_line

  echo "Running karma tests"
  
  docker exec -id ${PROJECT}_selenium_1 python /selenium/bin/chrome_karma.py
  
  docker exec -i ${PROJECT}_dev_1 su vagrant -c "
    source /vagrant/bin/init_vagrant_env
    /vagrant/node_modules/karma/bin/karma start \\
      /vagrant/karma.conf.js --single-run --reporters dots,junit
  " && karma_rc=$? || karma_rc=$?
  
  [[ karma_rc -eq 0 ]] && echo "PASS" || echo "FAIL"
  
  print_line
  return $((unit_rc * unit_rc + karma_rc * karma_rc))
}
