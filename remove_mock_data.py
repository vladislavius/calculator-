import re

with open('app/page.tsx', 'r') as f:
    content = f.read()

# 1. Remove MOCK DRINKS
content = re.sub(
    r"const DRINKS = \[[\s\S]*?\];\n\n",
    "// DRINKS moved to boat_drinks table in DB\n\n",
    content
)

# 2. Remove MOCK TRANSFER_OPTIONS  
content = re.sub(
    r"const TRANSFER_OPTIONS = \[[\s\S]*?\];\n\n",
    "// TRANSFER_OPTIONS moved to transfer_options table in DB\n\n",
    content
)

# 3. Remove MOCK SPECIAL_SERVICES
content = re.sub(
    r"const SPECIAL_SERVICES = \[[\s\S]*?\];\n\n",
    "// SPECIAL_SERVICES moved to staff_services table in DB\n\n",
    content
)

# 4. Remove MOCK WATER_TOYS
content = re.sub(
    r"const WATER_TOYS = \[[\s\S]*?\];\n\n",
    "// WATER_TOYS moved to watersports_catalog table in DB\n\n",
    content
)

# 5. Remove MOCK FEES
content = re.sub(
    r"const FEES = \[[\s\S]*?\];\n\n",
    "// FEES moved to route_fees table in DB\n\n",
    content
)

# 6. Add new state variables for DB data after existing state
old_state = "const [transferOptionsDB, setTransferOptionsDB] = useState<any[]>([]);"
new_state = """const [transferOptionsDB, setTransferOptionsDB] = useState<any[]>([]);
  
  // DB data
  const [boatDrinks, setBoatDrinks] = useState<any[]>([]);
  const [routeFees, setRouteFees] = useState<any[]>([]);
  const [staffServices, setStaffServices] = useState<any[]>([]);
  const [boatMenu, setBoatMenu] = useState<any[]>([]);"""

content = content.replace(old_state, new_state)

# 7. Update loadPartnersData to load all DB data
old_load = """// Load transfer options
      const { data: toData } = await supabase.from('transfer_options').select('*');
      if (toData) setTransferOptionsDB(toData);
    };
    
    loadPartnersData();
  }, []);"""

new_load = """// Load transfer options
      const { data: toData } = await supabase.from('transfer_options').select('*');
      if (toData) setTransferOptionsDB(toData);
      
      // Load staff services
      const { data: ssData } = await supabase.from('staff_services').select('*');
      if (ssData) setStaffServices(ssData);
    };
    
    loadPartnersData();
  }, []);"""

content = content.replace(old_load, new_load)

# 8. Update openBoatDetails to load boat-specific data (drinks, menu, route fees)
old_open = """const openBoatDetails = async (boat: SearchResult) => {
    setSelectedBoat(boat);
    setLoadingOptions(true);
    resetSelections();

    try {"""

new_open = """const openBoatDetails = async (boat: SearchResult) => {
    setSelectedBoat(boat);
    setLoadingOptions(true);
    resetSelections();

    try {
      // Load boat drinks from partner
      const { data: drinksData } = await supabase
        .from('boat_drinks')
        .select('*')
        .eq('partner_id', boat.partner_id);
      setBoatDrinks(drinksData || []);
      
      // Load route fees for this route
      const { data: routeData } = await supabase
        .from('routes')
        .select('id')
        .ilike('name', '%' + boat.route_name.split(' ')[0] + '%')
        .limit(1)
        .single();
      
      if (routeData) {
        const { data: feesData } = await supabase
          .from('route_fees')
          .select('*')
          .eq('route_id', routeData.id);
        setRouteFees(feesData || []);
        
        // Auto-add mandatory fees
        const mandatoryFees = (feesData || []).filter((f: any) => f.mandatory);
        setSelectedFees(mandatoryFees.map((f: any) => ({
          id: f.id.toString(),
          name: f.name_en,
          nameRu: f.name_ru,
          pricePerPerson: f.price_per_person,
          adults: adults,
          children: children,
          mandatory: true
        })));
      }
      
      // Load boat menu
      const { data: menuData } = await supabase
        .from('boat_menu')
        .select('*')
        .or('partner_id.eq.' + boat.partner_id + ',boat_id.eq.' + boat.boat_id);
      setBoatMenu(menuData || []);
"""

content = content.replace(old_open, new_open)

# 9. Update calculateTotals to use DB fees
old_fees_calc = """// Park fees
    const feesTotal = selectedFees.reduce((sum, f) => {
      const fee = FEES.find(ff => ff.id === f.id);
      return sum + (fee ? (fee.priceAdult * f.adults) + (fee.priceChild * f.children) : 0);
    }, 0);"""

new_fees_calc = """// Park fees (from DB)
    const feesTotal = selectedFees.reduce((sum, f: any) => {
      return sum + ((f.pricePerPerson || 0) * (f.adults + f.children));
    }, 0);"""

content = content.replace(old_fees_calc, new_fees_calc)

# 10. Update toys calculation to use DB
old_toys_calc = """// Water toys
    const toysTotal = selectedToys.reduce((sum, t) => {
      const toy = WATER_TOYS.find(w => w.id === t.id);
      if (!toy) return sum;
      if (toy.unit === 'hour') return sum + (toy.price * t.hours * t.quantity);
      return sum + (toy.price * t.quantity);
    }, 0);"""

new_toys_calc = """// Water toys (from watersports_catalog DB)
    const toysTotal = selectedToys.reduce((sum, t: any) => {
      return sum + ((t.pricePerHour || 0) * (t.hours || 1) + (t.pricePerDay || 0) * (t.days || 0)) * (t.quantity || 1);
    }, 0);"""

content = content.replace(old_toys_calc, new_toys_calc)

# 11. Update services calculation to use DB
old_services_calc = """// Services
    const servicesTotal = selectedServices.reduce((sum, s) => {
      const service = SPECIAL_SERVICES.find(ss => ss.id === s.id);
      return sum + (service ? service.price * s.quantity : 0);
    }, 0);"""

new_services_calc = """// Services (from staff_services DB)
    const servicesTotal = selectedServices.reduce((sum, s: any) => {
      return sum + ((s.price || 0) * (s.quantity || 1));
    }, 0);"""

content = content.replace(old_services_calc, new_services_calc)

# 12. Update drinks calculation to use DB
old_drinks_calc = """// Drinks
    const drinksTotal = drinkOrders.reduce((sum, d) => sum + (d.price * d.quantity), 0) + corkageFee;"""

new_drinks_calc = """// Drinks (from boat_drinks DB)
    const drinksTotal = drinkOrders.reduce((sum, d: any) => sum + ((d.price || 0) * (d.quantity || 1)), 0) + corkageFee;"""

content = content.replace(old_drinks_calc, new_drinks_calc)

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ Removed MOCK data constants")
print("✅ Added DB state variables")  
print("✅ Updated loadPartnersData to load staff_services")
print("✅ Updated openBoatDetails to load boat drinks, route fees, boat menu")
print("✅ Updated calculations to use DB data")
print("")
print("Next: Run second patch to update UI rendering")
