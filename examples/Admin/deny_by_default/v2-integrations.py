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
fakeGkey = "DGC4Q2A7ZYBQBFOQFFFF"

def create_and_print(name, groups_allowed=None):
    try:
        integration = admin_api.create_integration(
            name=name,
            integration_type="websdk",
            groups_allowed=groups_allowed,
        )

        print("\nCreated integration:")
        pprint.pprint(integration)

    except Exception as e:
        print(e)
        return None

    return integration


def update_and_print(ikey, groups_allowed=None):
    try:
        integration = admin_api.update_integration(
            integration_key=ikey,
            groups_allowed=groups_allowed,
        )

        print("\nUpdated integration:")
        pprint.pprint(integration)

    except Exception as e:
        print(e)
        return None

    return integration


def print_integrations_collection(integrations):
    for integration in integrations:
        print(integration["name"] + " (" + integration["integration_key"] + "): " + (integration["user_access"] if "user_access" in integration else "<No user_access>"))
        if integration["groups_allowed"]:
            print("\tgroups_allowed: " + ", ".join(integration["groups_allowed"]))

NO_USERS = "NO_USERS"
PERMITTED_GROUPS = "PERMITTED_GROUPS"
ALL_USERS = "ALL_USERS"

print("\n**Create**")
default = create_and_print("ZTIDP-5163 Default (NO_USERS)")
no_users = create_and_print("ZTIDP-5163 NO_USERS", groups_allowed="deny")
permitted_groups = create_and_print("ZTIDP-5163 PERMITTED_GROUPS", groups_allowed=f"{gkey1},{gkey2}")
all_users = create_and_print("ZTIDP-5163 ALL_USERS", groups_allowed="")

print("\n==Error Cases==")

print("\n--groups_allowed as array--")
create_and_print("ZTIDP-5163", groups_allowed=[gkey1, gkey2])

print("\n--invalid groups_allowed--")
create_and_print("ZTIDP-5163", groups_allowed=1)

print("\n--non-existant group--")
create_and_print("ZTIDP-5163", groups_allowed=f"{gkey1},{fakeGkey}")

default_ikey = default["integration_key"]
no_users_ikey = no_users["integration_key"]
permitted_groups_string_ikey = permitted_groups["integration_key"]
all_users_ikey = all_users["integration_key"]

all_ikeys = ", ".join([default_ikey, no_users_ikey, permitted_groups_string_ikey, all_users_ikey])
all_groups_allowed = ", ".join([
    str(default["groups_allowed"]),
    str(no_users["groups_allowed"]),
    str(permitted_groups["groups_allowed"]),
    str(all_users["groups_allowed"]),
])

print(f"\n\nCreated ikeys: {all_ikeys}")
print(f"\nWith groups_allowed: {all_groups_allowed}")

print("\n**Get integrations collection**\n")
limit = 10
offset = 4
print(f"Fetching all integrations, limited to {limit} offset by {offset}\n")
integrations = admin_api.get_integrations(limit=limit, offset=offset)
pprint.pprint(integrations)
print("\nWhich contains these integrations:")
print_integrations_collection(integrations)

print("\n**Get integrations collection generator**\n")
integrations = admin_api.get_integrations_generator()
print_integrations_collection(integrations)

print("\n**Update**\n")
print("--Update to ALL_USERS--")
update_and_print(default_ikey, groups_allowed="")

print("\n--Update to NO_USERS--")
update_and_print(default_ikey, groups_allowed="deny")

print("\n--Update to PERMITTED_GROUPS--")
update_and_print(default_ikey, groups_allowed=f"{gkey1},{gkey2}")

print("\n--Update integration, but not groups_allowed--")
updated = admin_api.update_integration(default_ikey, name="ZTIDP-5163s Updated 2")
pprint.pprint(updated)

print ("\n==Error Cases==")

print("\n--groups_allowed as array--")
create_and_print(default_ikey, groups_allowed=[gkey1, gkey2])

print("\n--Invalid groups_allowed - wrong type--")
update_and_print(default_ikey, groups_allowed=1)

print("\n--Invalid groups_allowed - invalid gkey--")
update_and_print(default_ikey, groups_allowed="Dang, I am absolutely not valid :(")

print("\n--Invalid groups_allowed - valid gkey does not exist--")
update_and_print(default_ikey, groups_allowed=f"{fakeGkey},{gkey2}")

print("\n**Get single integration**\n")
print(f"Fetching integration with ikey: {default_ikey}\n")
integration = admin_api.get_integration(default_ikey)
pprint.pprint(integration)

print("\n**Delete**")
admin_api.delete_integration(default_ikey)
admin_api.delete_integration(no_users_ikey)
admin_api.delete_integration(permitted_groups_string_ikey)
admin_api.delete_integration(all_users_ikey)

print("Deleted integrations successfully")