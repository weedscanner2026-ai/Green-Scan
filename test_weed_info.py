import json

# Test if weed_info.json is valid and has correct structure
with open('weed_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("WEED_INFO.JSON VALIDATION")
print("=" * 60)

weeds = data.get('weeds', {})
print(f"\nTotal weeds in file: {len(weeds)}")
print("\nWeed names (keys):")
for name in weeds.keys():
    print(f"  - {name}")

print("\n" + "=" * 60)
print("CHECKING EACH WEED ENTRY")
print("=" * 60)

for weed_name, weed_data in weeds.items():
    print(f"\n{weed_name}:")
    print(f"  Scientific Name: {weed_data.get('scientific_name', 'MISSING')}")
    desc = weed_data.get('description', 'MISSING')
    print(f"  Description: {desc[:50]}..." if len(desc) > 50 else f"  Description: {desc}")
    print(f"  Control Methods: {weed_data.get('control_methods', 'MISSING')[:50]}...")

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)
