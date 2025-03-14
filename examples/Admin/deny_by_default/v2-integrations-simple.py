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

gkey1 = "DGSZJD877B6PI3WNX37J"
gkey2 = "DGK7C34SP8C71HVQR16O"


# user_accesses = [None, "NO_USERS", "ALL_USERS", "PERMITTED_GROUPS"]
groups_alloweds = [None, "deny", "", gkey1]

test_cases = {
      "Default": None,
      "NO_USERS": "deny",
      "ALL_USERS": "",
      "PERMITTED_GROUPS": gkey1
}

ikeys = []
for name, groups_allowed in test_cases.items():
        integration = admin_api.create_integration(
                name=f"ZTIDP-5163 - {name}",
                integration_type="websdk",
                groups_allowed=groups_allowed
        )

        name = integration["name"]
        ikey = integration["integration_key"]
        groups_allowed = integration["groups_allowed"]
        ikeys.append(ikey)

        group_names = [group for group in groups_allowed]
        print(f"{name} - groups_allowed is {groups_allowed}")

input('Press enter to delete integrations...')
for ikey in ikeys:
    admin_api.delete_integration(ikey)