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
    up --force-recreate -d
  
  if [[ $UID -eq 0 ]]; then
    # This fixes permissions with bindfs only on jenkins.
    chown 1000:1000 -R .
  elif [[ $UID -eq 1000 ]]; then
    docker exec -i ${PROJECT}_dev_1 sh -c "
    bindfs /vagrant_bind /vagrant --map=$UID/1000 -o nonempty
    "
  fi
  
  echo "Provisioning ${PROJECT}_dev_1"
  docker exec -i ${PROJECT}_dev_1 su vagrant -c "
    source /vagrant/bin/init_vagrant_env
    ansible-playbook -i provision/docker/inventory provision/site.yml
    build_compass
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

  docker exec -i ${PROJECT}_dev_1 sh -c "chown $UID -R /vagrant"
  docker exec -i ${PROJECT}_selenium_1 sh -c "chown $UID -R /selenium"

  docker-compose -p ${PROJECT} stop
}
