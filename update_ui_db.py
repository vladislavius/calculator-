import re

with open('app/page.tsx', 'r') as f:
    content = f.read()

# 1. Fix addDrink function to work with DB drinks
old_add_drink = """const addDrink = (drink: typeof DRINKS[0]) => {
    const exists = drinkOrders.find(d => d.drinkId === drink.id);
    if (exists) {
      setDrinkOrders(drinkOrders.map(d => 
        d.drinkId === drink.id ? { ...d, quantity: d.quantity + 1 } : d
      ));
    } else {
      setDrinkOrders([...drinkOrders, {
        drinkId: drink.id,
        name: drink.name,
        price: drink.price,
        quantity: 1,
        unit: drink.unit
      }]);
    }
  };"""

new_add_drink = """const addDrink = (drink: any) => {
    const exists = drinkOrders.find(d => d.drinkId === drink.id);
    if (exists) {
      setDrinkOrders(drinkOrders.map(d => 
        d.drinkId === drink.id ? { ...d, quantity: d.quantity + 1 } : d
      ));
    } else {
      setDrinkOrders([...drinkOrders, {
        drinkId: drink.id,
        name: drink.name_en || drink.name,
        nameRu: drink.name_ru || drink.name,
        price: drink.price || 0,
        quantity: 1,
        unit: drink.unit || 'piece',
        included: drink.included || false
      }]);
    }
  };"""

content = content.replace(old_add_drink, new_add_drink)

# 2. Fix toggleService to work with DB services
old_toggle_service = """const toggleService = (serviceId: string) => {
    const exists = selectedServices.find(s => s.id === serviceId);
    if (exists) {
      setSelectedServices(selectedServices.filter(s => s.id !== serviceId));
    } else {
      setSelectedServices([...selectedServices, { id: serviceId, quantity: 1 }]);
    }
  };"""

new_toggle_service = """const toggleService = (service: any) => {
    const exists = selectedServices.find((s: any) => s.id === service.id);
    if (exists) {
      setSelectedServices(selectedServices.filter((s: any) => s.id !== service.id));
    } else {
      setSelectedServices([...selectedServices, { 
        id: service.id, 
        name: service.name_en || service.name,
        nameRu: service.name_ru,
        price: service.price || 0,
        pricePer: service.price_per || 'day',
        quantity: 1 
      }]);
    }
  };"""

content = content.replace(old_toggle_service, new_toggle_service)

# 3. Fix toggleToy to work with DB watersports
old_toggle_toy = """const toggleToy = (toyId: string) => {
    const exists = selectedToys.find(t => t.id === toyId);
    if (exists) {
      setSelectedToys(selectedToys.filter(t => t.id !== toyId));
    } else {
      setSelectedToys([...selectedToys, { id: toyId, quantity: 1, hours: 1 }]);
    }
  };"""

new_toggle_toy = """const toggleToy = (toy: any) => {
    const exists = selectedToys.find((t: any) => t.id === toy.id);
    if (exists) {
      setSelectedToys(selectedToys.filter((t: any) => t.id !== toy.id));
    } else {
      setSelectedToys([...selectedToys, { 
        id: toy.id, 
        name: toy.name_en || toy.name,
        nameRu: toy.name_ru,
        pricePerHour: toy.price_per_hour || 0,
        pricePerDay: toy.price_per_day || 0,
        quantity: 1, 
        hours: 1,
        days: 0
      }]);
    }
  };"""

content = content.replace(old_toggle_toy, new_toggle_toy)

# 4. Fix toggleFee to work with DB fees
old_toggle_fee = """const toggleFee = (feeId: string) => {
    const exists = selectedFees.find(f => f.id === feeId);
    if (exists) {
      setSelectedFees(selectedFees.filter(f => f.id !== feeId));
    } else {
      setSelectedFees([...selectedFees, { id: feeId, adults: adults, children: children }]);
    }
  };"""

new_toggle_fee = """const toggleFee = (fee: any) => {
    const exists = selectedFees.find((f: any) => f.id === fee.id);
    if (exists) {
      setSelectedFees(selectedFees.filter((f: any) => f.id !== fee.id));
    } else {
      setSelectedFees([...selectedFees, { 
        id: fee.id, 
        name: fee.name_en,
        nameRu: fee.name_ru,
        pricePerPerson: fee.price_per_person || 0,
        adults: adults, 
        children: children,
        mandatory: fee.mandatory || false
      }]);
    }
  };"""

content = content.replace(old_toggle_fee, new_toggle_fee)

# 5. Add function to add menu item
add_menu_func = """
  // Add menu item from boat_menu
  const addMenuItem = (item: any) => {
    if (item.included) return; // Don't add included items
    setCateringOrders([...cateringOrders, {
      packageId: 'menu_' + item.id,
      packageName: item.name_en + ' (с яхты)',
      pricePerPerson: item.price || 0,
      persons: adults,
      minPersons: 1,
      notes: item.description || ''
    }]);
  };

"""

# Insert after removeCatering function
content = content.replace(
    "const removeCatering = (index: number) => {\n    setCateringOrders(cateringOrders.filter((_, i) => i !== index));\n  };",
    "const removeCatering = (index: number) => {\n    setCateringOrders(cateringOrders.filter((_, i) => i !== index));\n  };" + add_menu_func
)

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Updated addDrink to work with DB")
print("✅ Updated toggleService to work with DB")
print("✅ Updated toggleToy to work with DB")
print("✅ Updated toggleFee to work with DB")
print("✅ Added addMenuItem function")
