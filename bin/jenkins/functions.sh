
set -o nounset
set -o errexit

setup () {
  if [ -z "${1:-}" ]; then
    echo "Missing mandatory project parameter"
    exit 1
  else
    PROJECT="${1}"
  fi

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
		ansible-playbook -i provision/docker/inventory provision/site.yml
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

