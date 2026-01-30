import re

with open('app/page.tsx', 'r') as f:
    content = f.read()

# Find and replace the FEES tab rendering section
# We need to find where FEES.map is used and replace with routeFees.map

# 1. Replace FEES rendering in the fees tab
old_fees_render = """FEES.map(fee => ("""
new_fees_render = """routeFees.map((fee: any) => ("""
content = content.replace(old_fees_render, new_fees_render)

# 2. Replace fee property access
content = content.replace("fee.nameRu", "fee.name_ru")
content = content.replace("fee.priceAdult", "fee.price_per_person")
content = content.replace("fee.priceChild", "Math.round(fee.price_per_person * 0.5)")

# 3. Replace DRINKS rendering
old_drinks_render = """DRINKS.map(drink => ("""
new_drinks_render = """boatDrinks.map((drink: any) => ("""
content = content.replace(old_drinks_render, new_drinks_render)

# 4. Replace drink property access
content = content.replace("drink.nameRu", "drink.name_ru")
content = content.replace("drink.name}", "drink.name_en}")

# 5. Replace WATER_TOYS rendering
old_toys_render = """WATER_TOYS.map(toy => ("""
new_toys_render = """watersportsCatalog.map((toy: any) => ("""
content = content.replace(old_toys_render, new_toys_render)

# 6. Replace toy property access
content = content.replace("toy.nameRu", "toy.name_ru")
content = content.replace("toy.name}", "toy.name_en}")
content = content.replace("toy.description", "toy.description || ''")

# 7. Replace SPECIAL_SERVICES rendering
old_services_render = """SPECIAL_SERVICES.map(service => ("""
new_services_render = """staffServices.map((service: any) => ("""
content = content.replace(old_services_render, new_services_render)

# 8. Replace service property access
content = content.replace("service.nameRu", "service.name_ru")
content = content.replace("service.name}", "service.name_en}")

# 9. Replace TRANSFER_OPTIONS rendering (if using mock)
old_transfer_render = """TRANSFER_OPTIONS.map(opt => ("""
new_transfer_render = """transferOptionsDB.map((opt: any) => ("""
content = content.replace(old_transfer_render, new_transfer_render)

# 10. Fix toggleFee calls
content = content.replace("toggleFee(fee.id)", "toggleFee(fee)")
content = content.replace("toggleService(service.id)", "toggleService(service)")
content = content.replace("toggleToy(toy.id)", "toggleToy(toy)")

# 11. Fix selectedFees.find
content = content.replace(
    "selectedFees.find(f => f.id === fee.id)",
    "selectedFees.find((f: any) => f.id === fee.id)"
)

# 12. Fix selectedServices.find  
content = content.replace(
    "selectedServices.find(s => s.id === service.id)",
    "selectedServices.find((s: any) => s.id === service.id)"
)

# 13. Fix selectedToys.find
content = content.replace(
    "selectedToys.find(t => t.id === toy.id)",
    "selectedToys.find((t: any) => t.id === toy.id)"
)

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Updated FEES rendering to use routeFees from DB")
print("✅ Updated DRINKS rendering to use boatDrinks from DB")
print("✅ Updated WATER_TOYS rendering to use watersportsCatalog from DB")
print("✅ Updated SPECIAL_SERVICES rendering to use staffServices from DB")
print("✅ Updated TRANSFER_OPTIONS rendering to use transferOptionsDB")
print("✅ Fixed all toggle function calls")
print("✅ Fixed all find function types")
