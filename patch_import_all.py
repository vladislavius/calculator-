import re

# Read the file
with open('app/import-all/page.tsx', 'r') as f:
    content = f.read()

# 1. Add deletePartner function after deleteItem function
delete_partner_func = '''
  const deletePartner = async (id: number) => {
    if (!confirm('Удалить партнёра и все его данные?')) return;
    const table = activeType === 'boats' ? 'partners' : activeType === 'catering' ? 'catering_partners' : activeType === 'watersports' ? 'watersports_partners' : 'decoration_partners';
    const itemsTable = activeType === 'boats' ? 'boats' : activeType === 'catering' ? 'catering_menu' : activeType === 'watersports' ? 'watersports_catalog' : 'decoration_catalog';
    // Delete items first
    await supabase.from(itemsTable).delete().eq('partner_id', id);
    // Then delete partner
    await supabase.from(table).delete().eq('id', id);
    showMessage('Партнёр удалён');
    loadAllData();
  };
'''

# Find deleteItem function and add deletePartner after it
content = content.replace(
    "showMessage('Удалено'); loadAllData();\n  };",
    "showMessage('Удалено'); loadAllData();\n  };" + delete_partner_func
)

# 2. Add state for contract view
content = content.replace(
    "const [expandedPartners, setExpandedPartners] = useState<Set<number>>(new Set());",
    '''const [expandedPartners, setExpandedPartners] = useState<Set<number>>(new Set());
  const [selectedContract, setSelectedContract] = useState<any>(null);
  const [contractRoutes, setContractRoutes] = useState<any[]>([]);
  const [contractOptions, setContractOptions] = useState<any[]>([]);'''
)

# 3. Add function to load contract details
load_contract_func = '''
  const loadContractDetails = async (partnerId: number) => {
    // Get boats for this partner
    const { data: partnerBoats } = await supabase.from('boats').select('id, name').eq('partner_id', partnerId);
    if (!partnerBoats || partnerBoats.length === 0) return;
    
    const boatIds = partnerBoats.map(b => b.id);
    
    // Get routes and prices
    const { data: prices } = await supabase
      .from('route_prices')
      .select('*, routes(name), boats(name)')
      .in('boat_id', boatIds);
    
    // Get options
    const { data: options } = await supabase
      .from('boat_options')
      .select('*, options_catalog(name_en, name_ru)')
      .in('boat_id', boatIds);
    
    setContractRoutes(prices || []);
    setContractOptions(options || []);
    setSelectedContract(partnerId);
  };
'''

content = content.replace(
    "const togglePartner = (id: number) => {",
    load_contract_func + "\n  const togglePartner = (id: number) => {"
)

# 4. Update the view section for boats to show contract details
old_boats_view = '''if (activeType === 'boats') return boatPartners.map(p => ({ partner: p, items: boats.filter(b => b.partner_id === p.id) })).filter(g => g.items.length > 0);'''

new_boats_view = '''if (activeType === 'boats') return boatPartners.map(p => ({ partner: p, items: boats.filter(b => b.partner_id === p.id), boatCount: boats.filter(b => b.partner_id === p.id).length })).filter(g => g.items.length > 0);'''

content = content.replace(old_boats_view, new_boats_view)

# 5. Replace the partner header to include delete button and contract view for boats
old_partner_header = '''<div onClick={() => togglePartner(group.partner.id)} style={{display:'flex',justifyContent:'space-between',padding:'12px 16px',backgroundColor:'#f9fafb',cursor:'pointer'}}>
                    <span style={{fontWeight:'600'}}>{activeType==='boats'?'🚢':activeType==='catering'?'🍽️':activeType==='watersports'?'🏄':'✨'} {group.partner.name} ({group.items.length})</span>
                    <span>{expandedPartners.has(group.partner.id)?'▼':'▶'}</span>
                  </div>'''

new_partner_header = '''<div style={{display:'flex',justifyContent:'space-between',padding:'12px 16px',backgroundColor:'#f9fafb'}}>
                    <div onClick={() => { togglePartner(group.partner.id); if(activeType==='boats') loadContractDetails(group.partner.id); }} style={{cursor:'pointer',flex:1,display:'flex',alignItems:'center',gap:'8px'}}>
                      <span style={{fontWeight:'600'}}>{activeType==='boats'?'🚢':activeType==='catering'?'🍽️':activeType==='watersports'?'🏄':'✨'} {group.partner.name}</span>
                      <span style={{color:'#6b7280'}}>({activeType==='boats' ? group.items.length + ' яхт' : group.items.length + ' позиций'})</span>
                      <span>{expandedPartners.has(group.partner.id)?'▼':'▶'}</span>
                    </div>
                    <button onClick={(e) => { e.stopPropagation(); deletePartner(group.partner.id); }} style={{padding:'4px 12px',backgroundColor:'#fee2e2',color:'#dc2626',border:'none',borderRadius:'4px',cursor:'pointer',fontSize:'12px'}}>Удалить</button>
                  </div>'''

content = content.replace(old_partner_header, new_partner_header)

# 6. Replace boat items display with contract details
old_items_display = '''{expandedPartners.has(group.partner.id) && group.items.map(item => (
                    <div key={item.id} style={{display:'flex',justifyContent:'space-between',padding:'10px 16px',borderTop:'1px solid #e5e7eb'}}>
                      <span>{item.name||item.name_en}</span>
                      <div style={{display:'flex',gap:'12px',alignItems:'center'}}>
                        <span>{activeType==='boats'?item.boat_type:activeType==='catering'?item.price_per_person+' THB/чел':activeType==='watersports'?item.price_per_hour+' THB/час':item.price+' THB'}</span>
                        <button onClick={() => deleteItem(activeType==='boats'?'boats':activeType==='catering'?'catering_menu':activeType==='watersports'?'watersports_catalog':'decoration_catalog',item.id)}
                          style={{padding:'4px 8px',backgroundColor:'#fee2e2',color:'#dc2626',border:'none',borderRadius:'4px',cursor:'pointer',fontSize:'12px'}}>Удалить</button>
                      </div>
                    </div>
                  ))}'''

new_items_display = '''{expandedPartners.has(group.partner.id) && (
                    activeType === 'boats' && selectedContract === group.partner.id ? (
                      <div style={{padding:'16px',borderTop:'1px solid #e5e7eb'}}>
                        {/* Boats list */}
                        <div style={{marginBottom:'16px'}}>
                          <h4 style={{fontWeight:'600',marginBottom:'8px',color:'#374151'}}>🚢 Яхты ({group.items.length})</h4>
                          <div style={{display:'flex',flexWrap:'wrap',gap:'8px'}}>
                            {group.items.map(boat => (
                              <span key={boat.id} style={{padding:'4px 12px',backgroundColor:'#e0e7ff',color:'#3730a3',borderRadius:'16px',fontSize:'13px'}}>{boat.name}</span>
                            ))}
                          </div>
                        </div>
                        {/* Routes and Prices */}
                        {contractRoutes.length > 0 && (
                          <div style={{marginBottom:'16px'}}>
                            <h4 style={{fontWeight:'600',marginBottom:'8px',color:'#374151'}}>📍 Маршруты и цены ({contractRoutes.length})</h4>
                            <table style={{width:'100%',borderCollapse:'collapse',fontSize:'13px'}}>
                              <thead>
                                <tr style={{backgroundColor:'#f3f4f6'}}>
                                  <th style={{padding:'8px',textAlign:'left',borderBottom:'1px solid #e5e7eb'}}>Яхта</th>
                                  <th style={{padding:'8px',textAlign:'left',borderBottom:'1px solid #e5e7eb'}}>Маршрут</th>
                                  <th style={{padding:'8px',textAlign:'left',borderBottom:'1px solid #e5e7eb'}}>Сезон</th>
                                  <th style={{padding:'8px',textAlign:'right',borderBottom:'1px solid #e5e7eb'}}>Цена</th>
                                </tr>
                              </thead>
                              <tbody>
                                {contractRoutes.map((price, idx) => (
                                  <tr key={idx} style={{borderBottom:'1px solid #e5e7eb'}}>
                                    <td style={{padding:'8px'}}>{price.boats?.name}</td>
                                    <td style={{padding:'8px'}}>{price.routes?.name}</td>
                                    <td style={{padding:'8px'}}><span style={{padding:'2px 8px',backgroundColor:price.season==='high'?'#fef3c7':price.season==='peak'?'#fee2e2':'#d1fae5',borderRadius:'4px',fontSize:'11px'}}>{price.season}</span></td>
                                    <td style={{padding:'8px',textAlign:'right',fontWeight:'500'}}>{price.base_price?.toLocaleString()} THB</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        )}
                        {/* Options */}
                        {contractOptions.length > 0 && (
                          <div>
                            <h4 style={{fontWeight:'600',marginBottom:'8px',color:'#374151'}}>⚙️ Опции ({contractOptions.length})</h4>
                            <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'8px'}}>
                              {contractOptions.map((opt, idx) => (
                                <div key={idx} style={{padding:'8px',backgroundColor:'#f9fafb',borderRadius:'6px',fontSize:'13px',display:'flex',justifyContent:'space-between'}}>
                                  <span>{opt.options_catalog?.name_en || opt.options_catalog?.name_ru}</span>
                                  <span style={{color:opt.status==='included'?'#059669':'#6b7280'}}>{opt.status==='included'?'✓ Вкл':opt.price+' THB'}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {contractRoutes.length === 0 && contractOptions.length === 0 && (
                          <p style={{color:'#6b7280',fontStyle:'italic'}}>Нет данных о маршрутах и опциях. Импортируйте контракт.</p>
                        )}
                      </div>
                    ) : (
                      group.items.map(item => (
                        <div key={item.id} style={{display:'flex',justifyContent:'space-between',padding:'10px 16px',borderTop:'1px solid #e5e7eb'}}>
                          <span>{item.name||item.name_en}</span>
                          <div style={{display:'flex',gap:'12px',alignItems:'center'}}>
                            <span>{activeType==='catering'?item.price_per_person+' THB/чел':activeType==='watersports'?item.price_per_hour+' THB/час':item.price+' THB'}</span>
                            <button onClick={() => deleteItem(activeType==='catering'?'catering_menu':activeType==='watersports'?'watersports_catalog':'decoration_catalog',item.id)}
                              style={{padding:'4px 8px',backgroundColor:'#fee2e2',color:'#dc2626',border:'none',borderRadius:'4px',cursor:'pointer',fontSize:'12px'}}>Удалить</button>
                          </div>
                        </div>
                      ))
                    )
                  )}'''

content = content.replace(old_items_display, new_items_display)

# Write back
with open('app/import-all/page.tsx', 'w') as f:
    f.write(content)

print("✅ Patched app/import-all/page.tsx")
print("   - Added delete partner button")
print("   - Added contract view for boats (routes, prices, options)")
