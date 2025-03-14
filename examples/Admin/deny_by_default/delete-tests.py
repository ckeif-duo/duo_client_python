#!/usr/bin/python
import pprint
import sys

import duo_client

argv_iter = iter(sys.argv[1:])

admin_api = duo_client.Admin(
        "DIADMINIKEYCLOUDSSO0",
        "qeqiNyKxbeTqGr3oCHWeMAej9qnJEYPbRQdaay6Q",
        "api-deadbeef.duo.test",
        "DISABLE" # disable certificate verification
)

integrations = admin_api.get_integrations()

for integration in integrations:
    if integration["name"].startswith("ZTIDP-5163"):
        print(f"Deleting integration {integration['name']} ({integration['integration_key']})")
        admin_api.delete_integration(integration["integration_key"])
