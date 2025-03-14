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


def create_and_print(name, groups_allowed=None, user_access=None):
    try:
        integration = admin_api.create_integration(
            name=name,
            integration_type="websdk",
            groups_allowed=groups_allowed,
            user_access=user_access
        )

        print("\nCreated integration:")
        pprint.pprint(integration)

    except Exception as e:
        print(e)
        return None

    return integration


def update_and_print(ikey, groups_allowed=None, user_access=None):
    try:
        integration = admin_api.update_integration(
            integration_key=ikey,
            groups_allowed=groups_allowed,
            user_access=user_access
        )

        print("\nUpdated integration:")
        pprint.pprint(integration)

    except Exception as e:
        print(e)
        return None

    return integration


def print_integrations_collection(integrations):
    for integration in integrations:
        print(integration["name"] + " (" + integration["integration_key"] + "): " +  integration["user_access"])
        if integration["groups_allowed"]:
            print("\tgroups_allowed: " + ", ".join(integration["groups_allowed"]))

NO_USERS = "NO_USERS"
PERMITTED_GROUPS = "PERMITTED_GROUPS"
ALL_USERS = "ALL_USERS"

print("\n**Create**")
default = create_and_print("ZTIDP-5163")
no_users = create_and_print("ZTIDP-5163 NO_USERS", [], NO_USERS)
permitted_groups_array = create_and_print("ZTIDP-5163 PERMITTED_GROUPS (array)", [gkey1, gkey2], PERMITTED_GROUPS)
permitted_groups_string = create_and_print("ZTIDP-5163 PERMITTED_GROUPS (string)", f"{gkey1},{gkey2}", PERMITTED_GROUPS)
all_users = create_and_print("ZTIDP-5163 ALL_USERS", [], ALL_USERS)

print("\n==Error Cases==")

print("--NO_USERS with groups_allowed--")
create_and_print("ZTIDP-5163 invalid", gkey1, NO_USERS)

print("\n--ALL_USERS with groups_allowed--")
create_and_print("ZTIDP-5163 invalid", [gkey1,gkey2], ALL_USERS)

print("\n--PERMITTED_GROUPS with no groups_allowed--")
create_and_print("ZTIDP-5163 invalid", None, PERMITTED_GROUPS)

print("\n--invalid groups_allowed--")
create_and_print("ZTIDP-5163 invalid", 1, PERMITTED_GROUPS)

print("\n--invalid groups_allowed (deny)--")
create_and_print("ZTIDP-5163 invalid", groups_allowed="deny", user_access=PERMITTED_GROUPS)

print("\n--invalid user_access--")
create_and_print("ZTIDP-5163 invalid", groups_allowed=None, user_access="eggs, bacon and toast")

print("\n--no user_access provided, groups_allowed is provided--")
create_and_print("ZTIDP-5163 invalid", groups_allowed=[gkey2])

default_ikey = default["integration_key"]
no_users_ikey = no_users["integration_key"]
permitted_groups_array_ikey = permitted_groups_array["integration_key"] # TODO why didn't this work?
permitted_groups_string_ikey = permitted_groups_string["integration_key"]
all_users_ikey = all_users["integration_key"]

all_ikeys = ", ".join([default_ikey, no_users_ikey, permitted_groups_array_ikey, permitted_groups_string_ikey, all_users_ikey])
all_user_accesses = ", ".join([default["user_access"], no_users["user_access"], permitted_groups_array["user_access"], permitted_groups_string["user_access"], all_users["user_access"]])
all_groups_allowed = ", ".join([
    str(default["groups_allowed"]),
    str(no_users["groups_allowed"]),
    str(permitted_groups_array["groups_allowed"]),
    str(permitted_groups_string["groups_allowed"]),
    str(all_users["groups_allowed"]),
])

print(f"\n\nCreated ikeys: {all_ikeys}")
print(f"\nWith user_access: {all_user_accesses}")
print(f"\nWith groups_allowed: {all_groups_allowed}")

print("\n**Get integrations collection**\n")
limit = 5
offset = 9
print(f"Fetching all integrations, limited to {limit} offset by {offset}\n")
integrations = admin_api.get_integrations(limit=limit, offset=offset)
print(integrations)
print("\nWhich contains these integrations:")
print_integrations_collection(integrations)

print("\n**Get integrations collection generator**\n")
integrations = admin_api.get_integrations_generator()
print_integrations_collection(integrations)

print("\n**Update**\n")
print("--Update to ALL_USERS--")
update_and_print(default_ikey, user_access=ALL_USERS)

print("\n--Update to NO_USERS--")
update_and_print(default_ikey, user_access=NO_USERS, groups_allowed=[])

print("\n--Update to PERMITTED_GROUPS (string)--")
update_and_print(default_ikey, user_access=PERMITTED_GROUPS, groups_allowed=f"{gkey1},{gkey2}")

print("\n--Update to NO_USERS (groups_allowed as string)--")
update_and_print(default_ikey, user_access=NO_USERS, groups_allowed="")

print("\n--Update to ALL_USERS (groups_allowed as array)--")
update_and_print(default_ikey, user_access=ALL_USERS, groups_allowed=[])

print("\n--Update to PERMITTED_GROUPS (array)--")
update_and_print(default_ikey, user_access=PERMITTED_GROUPS, groups_allowed=[gkey1, gkey2])

print("\n --PERMITTED_GROUPS only update groups_allowed--")
update_and_print(default_ikey, groups_allowed=[gkey1])

print("\n--Update integration, but not groups_allowed or user_access--")
updated = admin_api.update_integration(default_ikey, name="ZTIDP-5163 Updated 2")
pprint.pprint(updated)

print ("\n==Error Cases==")

print("--NO_USERS (already set) + groups_allowed--")
admin_api.update_integration(default_ikey, groups_allowed="", user_access=NO_USERS)
update_and_print(default_ikey, [gkey1, gkey2])

print("\n--ALL_USERS (already set) + groups_allowed--")
admin_api.update_integration(default_ikey, groups_allowed=[], user_access=ALL_USERS)
update_and_print(default_ikey, [gkey1, gkey2])

print("\n--PERMITTED_GROUPS (already set) + no groups_allowed--")
admin_api.update_integration(default_ikey, user_access=PERMITTED_GROUPS, groups_allowed=[gkey2])
update_and_print(default_ikey, [])

print("\n--NO_USERS (explicitly set) + groups_allowed--")
update_and_print(default_ikey, groups_allowed=[gkey1, gkey2], user_access=NO_USERS)

print("\n--ALL_USERS (explicitly set) + groups_allowed--")
update_and_print(default_ikey, groups_allowed=[gkey1], user_access=ALL_USERS)

# Set the integration back to NO_USERS to test trying to change it to PERMITTED_GROUPS
admin_api.update_integration(default_ikey, user_access=NO_USERS, groups_allowed="")

print("\n--PERMITTED_GROUPS (explicitly set) + empty groups_allowed--")
update_and_print(default_ikey, groups_allowed=[], user_access=PERMITTED_GROUPS)

print("\n--PERMITTED_GROUPS (explicitly set) + no groups_allowed--")
update_and_print(default_ikey, user_access=PERMITTED_GROUPS)

# Set the integration back to PERMITTED_GROUPS to check validation of groups_allowed
admin_api.update_integration(default_ikey, user_access=PERMITTED_GROUPS, groups_allowed=[gkey1,gkey2])

print("\n--Invalid groups_allowed - wrong type--")
update_and_print(default_ikey, groups_allowed=1)

print("\n--Invalid groups_allowed - invalid gkey (array)--")
update_and_print(default_ikey, groups_allowed=["Dang, I am absolutely not valid :(", gkey1])

print("\n--Invalid groups_allowed - invalid gkey (string)--")
update_and_print(default_ikey, groups_allowed="Dang, I am absolutely not valid :(")

fakeGkey = "DGC4Q2A7ZYBQBFOQFFFF"

print("\n--Invalid groups_allowed - valid gkey does not exist (array)--")
update_and_print(default_ikey, groups_allowed=[gkey1, fakeGkey])

print("\n--Invalid groups_allowed - valid gkey does not exist (string)--")
update_and_print(default_ikey, groups_allowed=f"{fakeGkey},{gkey2}")

print("\n**Get single integration**\n")
print(f"Fetching integration with ikey: {default_ikey}\n")
integration = admin_api.get_integration(default_ikey)
print(integration)

print("\n**Delete**")
admin_api.delete_integration(default_ikey)
admin_api.delete_integration(no_users_ikey)
admin_api.delete_integration(permitted_groups_array_ikey)
admin_api.delete_integration(permitted_groups_string_ikey)
admin_api.delete_integration(all_users_ikey)

input("Press enter to delete integrations...")
print("Deleted integrations successfully")
