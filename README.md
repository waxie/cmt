# Cluster Management Tool
Cluster Management Tool (CMT) is originally created at SARA Computing and
Networking Services, which is based in Amsterdam and now known as SURFsara.

The main reason behind CMT's existence is that we needed a tool that's capable
of generating configuration-files for certain software running on our clusters.

CMT uses a database to store all information about your networks, hardware and
interfaces. With templates you can generate different types of configuration files.

For example DHCP, DNS, Torque, etc. CMT uses the Django framework.

## Requirements
 * Python 2.7 or higher
 * Python virtualenv
 
All dependencies for CMT can be found in the [requirements.txt] file. 

## Usage

Work in progress

### Download the client

You can download the client via a browser or simply with curl or wget:
```
curl --user <username> https://<hostname>/client/download
wget --user=<username> --ask-password --auth-no-challenge https://<hostname>/client/download
```

## Contact

For bugs, requests or suggestions, please mail to cmt-dev@surfsara.nl