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

user_accesses = [None, "NO_USERS", "ALL_USERS", "PERMITTED_GROUPS"]

ikeys = []
for user_access in user_accesses:
        integration = admin_api.create_integration(
                name=f"ZTIDP-5163 - {user_access}",
                integration_type="websdk",
                user_access=user_access,
                groups_allowed=None if user_access != "PERMITTED_GROUPS" else [gkey1]
        )

        name = integration["name"]
        user_access = integration["user_access"]
        ikey = integration["integration_key"]
        groups_allowed = integration["groups_allowed"]
        ikeys.append(ikey)

        group_names = [group for group in groups_allowed]
        print(f"{name} - {user_access} with groups_allowed of {group_names}")

input('Press enter to delete integrations...')
for ikey in ikeys:
    admin_api.delete_integration(ikey)