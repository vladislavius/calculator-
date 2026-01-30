import re

with open('app/page.tsx', 'r') as f:
    content = f.read()

# Fix line 1065 - non_alcoholic drinks
content = content.replace(
    "{DRINKS.filter(d => d.category === 'non_alcoholic').map(drink => (",
    "{boatDrinks.filter((d: any) => d.category === 'non_alcoholic').map((drink: any) => ("
)

# Fix line 1083 - alcohol drinks  
content = content.replace(
    "{DRINKS.filter(d => d.category === 'alcohol').map(drink => (",
    "{boatDrinks.filter((d: any) => d.category !== 'non_alcoholic' && !d.included).map((drink: any) => ("
)

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Fixed DRINKS -> boatDrinks")
