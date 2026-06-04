import json

with open("residents.json", "r") as f:
    residents = json.load(f)

for resident in residents:
    print("Name:", resident["name"])
    print("Age:", resident["age"])
    print("Risk:", resident["risk_level"])
    print()