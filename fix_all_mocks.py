with open('app/page.tsx', 'r') as f:
    content = f.read()

# Fix WATER_TOYS -> watersportsCatalog (line 1101)
content = content.replace(
    '{WATER_TOYS.map(toy => {',
    '{watersportsCatalog.map((toy: any) => {'
)

# Fix SPECIAL_SERVICES -> staffServices (line 1161)
content = content.replace(
    '{SPECIAL_SERVICES.map(service => {',
    '{staffServices.map((service: any) => {'
)

# Fix TRANSFER_OPTIONS -> transferOptionsDB (lines 1268, 1271, 1291, 1294)
content = content.replace(
    'TRANSFER_OPTIONS.find(t => t.type === e.target.value)',
    'transferOptionsDB.find((t: any) => t.type === e.target.value)'
)
content = content.replace(
    '{TRANSFER_OPTIONS.map(t => (',
    '{transferOptionsDB.map((t: any) => ('
)

# Fix FEES -> routeFees (line 1328)
content = content.replace(
    '{FEES.map(fee => {',
    '{routeFees.map((fee: any) => {'
)

# Fix property names for toys
content = content.replace('toy.name}', '(toy.name_en || toy.name)}')
content = content.replace('toy.pricePerHour', '(toy.price_per_hour || 0)')
content = content.replace('toy.pricePerDay', '(toy.price_per_day || 0)')

# Fix property names for services
content = content.replace('service.name}', '(service.name_en || service.name)}')
content = content.replace('service.price}', '(service.price || 0)}')

# Fix property names for fees
content = content.replace('fee.name}', '(fee.name_en || fee.name)}')
content = content.replace('fee.priceAdult', '(fee.price_per_person || 0)')
content = content.replace('fee.priceChild', 'Math.round((fee.price_per_person || 0) * 0.5)')

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Fixed WATER_TOYS -> watersportsCatalog")
print("✅ Fixed SPECIAL_SERVICES -> staffServices")
print("✅ Fixed TRANSFER_OPTIONS -> transferOptionsDB")
print("✅ Fixed FEES -> routeFees")
print("✅ Fixed property names (name_en, price_per_hour, etc.)")
