FROM centos:6

RUN yum -y install epel-release centos-release-SCL; yum clean all
RUN yum -y groupinstall "Development Tools"; yum clean all
RUN yum -y install git mysql python27-python-devel python27-MySQL-python libjpeg-turbo\
                   libjpeg-turbo-devel zlib zlib-devel; yum clean all
RUN curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
RUN scl enable python27 "python /tmp/get-pip.py"

copy requirements/ /src/requirements

RUN scl enable python27 "pip install Pillow==2.6.1"
RUN scl enable python27 "pip install -r /src/requirements/docker.txt"

copy cfgov /src/app
