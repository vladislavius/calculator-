with open('app/page.tsx', 'r') as f:
    content = f.read()

# ===== FIX WATER TOYS TAB =====
# Fix price display for toys - use price_per_hour or price_per_day
content = content.replace(
    "toy.price === 0 ? '✓ Free' : `${toy.price.toLocaleString()} THB/${toy.unit}`",
    "(toy.price_per_hour || 0) === 0 && (toy.price_per_day || 0) === 0 ? '✓ Включено' : `${(toy.price_per_hour || toy.price_per_day || 0).toLocaleString()} THB/${toy.price_per_hour ? 'час' : 'день'}`"
)

# Fix toy unit check
content = content.replace(
    "toy.unit === 'hour'",
    "(toy.price_per_hour && toy.price_per_hour > 0)"
)
content = content.replace(
    "toy.unit !== 'hour' && toy.unit !== 'included'",
    "(toy.price_per_day && toy.price_per_day > 0)"
)

# ===== FIX SERVICES TAB =====
# Fix service price display
content = content.replace(
    "{service.price.toLocaleString()} THB",
    "{(service.price || 0).toLocaleString()} THB"
)
# Fix service unit display
content = content.replace(
    "{service.name_ru} / {service.unit}",
    "{service.name_ru || ''} / {service.price_per || 'день'}"
)

# ===== FIX FEES TAB - need to see that section first =====

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Fixed WATER TOYS tab - price display")
print("✅ Fixed SERVICES tab - price and unit display")
