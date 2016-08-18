#!/usr/bin/env python

### export PYTHONPATH=<pwd_client_dir>
import cmt_client

client = Client()

json = client.request('read', 'equipment', ['rack=Z3A-H08', 'first_slot=17'], None)
print json

