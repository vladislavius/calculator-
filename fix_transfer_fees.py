with open('app/page.tsx', 'r') as f:
    content = f.read()

# ===== FIX TRANSFER TAB =====
# Fix nameRu -> name_ru for transfer options
content = content.replace(
    "{t.nameRu} {t.price > 0 ? `(${t.price} THB)` : ''}",
    "{t.name_ru || t.name} {(t.price || 0) > 0 ? `(${t.price} THB)` : ''}"
)

# Fix price access for transfer
content = content.replace(
    "price: opt?.price || 0",
    "price: opt?.price || 0"
)

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Fixed TRANSFER tab - name_ru field")
