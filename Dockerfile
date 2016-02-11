FROM phusion/baseimage

RUN apt-get update \
  && apt-get install -y \
    ansible \
    curl \
    fabric \
    git-core \
    make \
    mysql-server \
    nodejs \
    npm \
    python-apt \
    python-dev \
    python-imaging \
    python-mysqldb \
    python-pip \
    python-pycurl \
    python-virtualenv \
    ruby \
    sqlite3 \
    unzip \
    vim \
    wget \
    zip \
  && ln -s /usr/bin/nodejs /usr/bin/node

COPY ./provision/docker/01_start_mysql.sh /etc/my_init.d/

RUN /etc/init.d/mysql start \
  && mysql -uroot -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root'); \
                      SET PASSWORD FOR 'root'@'127.0.0.1' = PASSWORD('root')" \
  && /etc/init.d/mysql stop \
  && cd /var/lib \
  && mv mysql mysql-hd \
  && ln -s mysql-hd mysql \
  && chmod +x /etc/my_init.d/01_start_mysql.sh

COPY . /vagrant

WORKDIR /vagrant

RUN useradd -G sudo -m vagrant \
 && echo "vagrant ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && mkdir /vagrant-dev \
 && chown -R vagrant:vagrant /vagrant /vagrant-dev \
 && rm /usr/sbin/policy-rc.d

RUN su vagrant -c "ansible-playbook -i provision/docker/inventory provision/site.yml"
