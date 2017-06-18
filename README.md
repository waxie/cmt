# Cluster Management Tool
Cluster Management Tool (CMT) is originally created at SARA Computing and
Networking Services, which is based in Amsterdam and now known as SURFsara.

The main reason behind CMT's existence is that we needed a tool that's capable
of generating configuration-files for certain software running on our clusters.

CMT uses a database to store all information about your networks, hardware and
interfaces. With templates you can generate different types of configuration files.

For example DHCP, DNS, Torque, etc. CMT uses the Django framework.

The documentation is currently a bit limited to this README for know. We are working on better
docmentation

## Requirements
 * Python 2.7 (working on Python 3 support)
 * Python virtualenv
 
All dependencies for CMT can be found in the [requirements.txt](requirements.txt) file. If you don't want to use
the LDAP authentication backend, then you can remove django-auth-ldap from the requirements.txt
file.

Please note that CMT has been testen on Linux only.

## Installation of the CMT Server

After creating a virtualenv you can install the requirements of CMT with the following command:
```
pip install -r requirements.txt
```

Then you will need to create a configuration file which is used by CMT. CMT will look 
at location `/etc/cmt/cmt.conf`. For an example configuration see `files/cmt.conf` .

For easy use you can create a file `.virtual_env_path` in the root dir of CMT django site. In this
file you will need to specify the full path to your virtualenv you have created for CMT. For example
when you created a virtualenv called `cmt-2.5.0` the path is `/home/<username>/.virtualenv/cmt-2.5.0`.

Finally you will need to bootstrap CMT with `./manage.py migrate` and finally you can start CMT with
`./manage.py runserver`.

## Usage of the CMT Client

Before you can use the client, you will need to download it first. You can do this from the web
interface or with `curl` or `wget`. The client has only 1 requirement, Python 2.7. We are working
Python 3 support. In the next release 2.6.0 Python 3 wil be fully supported.

Examples:
```
curl --user <username> https://<hostname>/client/download
wget --user=<username> --ask-password --auth-no-challenge https://<hostname>/client/download
```

The client does not need any configuration, it will be configured for you when you download the 
client. The client supports the following modes:
 - read, Fetch and object from CMT
 - create, Create an object in CMT
 - update, Update an object from CMT
 - parse, Parse a template from CMT
 
You can read, create, update, parse the following objects:
 - address
 - cluster
 - company
 - connection
 - country
 - equipment
 - hardwaremodel
 - interface
 - interfacetype
 - network
 - rack
 - role
 - room
 - telephonenumber
 - warrantycontract
 - warrantytype

The client uses the arguments --get and --set to determine what kind of fields are specified.  
For each mode you can use the --help which of the arguments are supported by which mode.

### Cli Usage

Create example:
```
python cmt_client.py create cluster --set name="CMT Cluster"
Username: <username>
Password: 
[CREATE] Result:
{
    "created_on": "2017-06-17T19:57:12.875774",
    "machinenames": null,
    "name": "CMT Cluster",
    "note": "",
    "response": "201 - CREATED",
    "tags": "",
    "updated_on": "2017-06-17T19:57:12.875822",
    "url": "http://localhost.localdomain:8000/api/v2/cluster/55"
}
```

Read example:
```
python cmt_client.py read cluster --get name="CMT Cluster"
[READ] Result:
{
    "count": 1,
    "next": null,
    "previous": null,
    "response": "200 - OK",
    "results": [
        {
            "created_on": "2017-06-17T19:57:12.875774",
            "machinenames": null,
            "name": "CMT Cluster",
            "note": "",
            "tags": "",
            "updated_on": "2017-06-17T19:57:12.875822",
            "url": "http://localhost.localdomain:8000/api/v2/cluster/55"
        }
    ]
}
```

Update example:
```
python cmt_client.py update cluster --get name="CMT Cluster" --set machinenames="{machinenames}"
Username: <username>
Password: 
[UPDATE] Result:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "created_on": "2017-06-17T19:57:12.875774",
            "machinenames": "{machinenames}",
            "name": "CMT Cluster",
            "note": "",
            "response": "200 - OK",
            "tags": "",
            "updated_on": "2017-06-17T19:59:54.621700",
            "url": "http://localhost.localdomain:8000/api/v2/cluster/55"
        }
    ]
}
```

Delete example:
```
python cmt_client.py delete cluster --get name="CMT Cluster"
Username: <username>
Password: 
[DELETE] Result:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "created_on": "2017-06-17T19:57:12.875774",
            "machinenames": "{machinenames}",
            "name": "CMT Cluster",
            "note": "",
            "tags": "",
            "updated_on": "2017-06-17T19:59:54.621700",
            "url": "http://localhost.localdomain:8000/api/v2/cluster/55"
        }
    ]
}
```

### Module usage

Read example:
```python
import cmt_client

client = cmt_client.Client()
json = client.request('read', 'cluster', ['name="CMT Cluster"'], None)

print json
```

## Known issues

 * Currently field roles is not marked as required in the API when creating a new Equipment, but 
   it is required in the database model. So you will need to remember to specify it.
 * Currently is is not possible to add multiple roles to an Equipment via the API.
 * CMT client is not Python 3 ready

## Contact

For bugs, requests or suggestions, please mail to cmt-dev@surfsara.nl

## See also

History and old documentation can be found here: (https://oss.trac.surfsara.nl/cmt)