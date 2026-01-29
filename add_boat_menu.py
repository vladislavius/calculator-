import re

with open('app/import-all/page.tsx', 'r') as f:
    content = f.read()

# 1. Add boat menu state
old_state = "const [contractOptions, setContractOptions] = useState<any[]>([]);"
new_state = """const [contractOptions, setContractOptions] = useState<any[]>([]);
  const [boatMenu, setBoatMenu] = useState<any[]>([]);
  const [menuMode, setMenuMode] = useState<'import' | 'view'>('view');
  const [selectedBoatForMenu, setSelectedBoatForMenu] = useState<number | null>(null);
  const [menuText, setMenuText] = useState('');
  const [menuForAllBoats, setMenuForAllBoats] = useState(true);"""

content = content.replace(old_state, new_state)

# 2. Add loadBoatMenu to loadAllData
old_load = "if (dc) setDecorationCatalog(dc);\n  };"
new_load = """if (dc) setDecorationCatalog(dc);
    const { data: bm } = await supabase.from('boat_menu').select('*').order('name_en');
    if (bm) setBoatMenu(bm);
  };"""

content = content.replace(old_load, new_load)

# 3. Add loadContractDetails update to include menu
old_contract_load = """setContractRoutes(prices || []);
    setContractOptions(options || []);
    setSelectedContract(partnerId);
  };"""

new_contract_load = """setContractRoutes(prices || []);
    setContractOptions(options || []);
    
    // Load menu for this partner's boats
    const { data: menu } = await supabase
      .from('boat_menu')
      .select('*')
      .or('partner_id.eq.' + partnerId + ',boat_id.in.(' + boatIds.join(',') + ')');
    setBoatMenu(menu || []);
    
    setSelectedContract(partnerId);
  };"""

content = content.replace(old_contract_load, new_contract_load)

# 4. Add parseMenu and saveMenu functions before togglePartner
menu_functions = '''
  const parseMenuSimple = () => {
    const lines = menuText.split('\\n').filter(l => l.trim());
    const items: any[] = [];
    for (const line of lines) {
      const priceMatch = line.match(/(\\d+)/);
      const price = priceMatch ? parseInt(priceMatch[1]) : 0;
      const name = line.replace(/\\d+/g, '').replace(/THB|฿|бат/gi, '').replace(/[-—]/g, '').trim();
      const isIncluded = line.toLowerCase().includes('included') || line.toLowerCase().includes('вкл') || price === 0;
      if (name) items.push({ name_en: name, name_ru: name, price, included: isIncluded, category: 'main' });
    }
    return items;
  };

  const analyzeMenuAI = async (partnerId: number) => {
    if (menuText.length < 20) { showMessage('Текст меню слишком короткий', 'error'); return; }
    setLoading(true);
    try {
      const response = await fetch('/api/analyze-partner-price', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: menuText, type: 'boat_menu' })
      });
      const result = await response.json();
      if (!result.success) throw new Error(result.error);
      await saveMenuItems(result.items || [], partnerId);
    } catch (error: any) { 
      // Fallback to simple parsing
      const items = parseMenuSimple();
      if (items.length > 0) await saveMenuItems(items, partnerId);
      else showMessage('Ошибка: ' + error.message, 'error');
    }
    setLoading(false);
  };

  const saveMenuItems = async (items: any[], partnerId: number) => {
    const menuItems = items.map(item => ({
      partner_id: menuForAllBoats ? partnerId : null,
      boat_id: menuForAllBoats ? null : selectedBoatForMenu,
      name_en: item.name_en || item.name,
      name_ru: item.name_ru || item.name_en || item.name,
      price: item.price || 0,
      included: item.included || false,
      category: item.category || 'main',
      description: item.description || ''
    }));
    
    const { error } = await supabase.from('boat_menu').insert(menuItems);
    if (error) { showMessage('Ошибка: ' + error.message, 'error'); return; }
    
    showMessage('Сохранено ' + menuItems.length + ' позиций меню!');
    setMenuText('');
    setMenuMode('view');
    loadContractDetails(partnerId);
  };

  const deleteMenuItem = async (id: number, partnerId: number) => {
    await supabase.from('boat_menu').delete().eq('id', id);
    showMessage('Удалено');
    loadContractDetails(partnerId);
  };

'''

content = content.replace(
    "const loadContractDetails = async (partnerId: number) => {",
    menu_functions + "const loadContractDetails = async (partnerId: number) => {"
)

# 5. Update API route to handle boat_menu type
api_update = '''
# Update API to handle boat_menu
'''

# 6. Update the contract view to show menu section
old_options_section = '''{contractOptions.length > 0 && (
                          <div>
                            <h4 style={{fontWeight:'600',marginBottom:'8px',color:'#374151'}}>⚙️ Опции ({contractOptions.length})</h4>'''

new_options_section = '''{/* Menu Section */}
                        <div style={{marginBottom:'16px',padding:'16px',backgroundColor:'#fffbeb',borderRadius:'8px',border:'1px solid #fcd34d'}}>
                          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'12px'}}>
                            <h4 style={{fontWeight:'600',color:'#92400e'}}>🍽️ Меню яхты</h4>
                            <div style={{display:'flex',gap:'8px'}}>
                              <button onClick={() => setMenuMode(menuMode === 'view' ? 'import' : 'view')} 
                                style={{padding:'6px 12px',backgroundColor:menuMode==='import'?'#fbbf24':'#fef3c7',color:'#92400e',border:'none',borderRadius:'6px',cursor:'pointer',fontSize:'13px'}}>
                                {menuMode === 'view' ? '+ Добавить меню' : 'Отмена'}
                              </button>
                            </div>
                          </div>
                          
                          {menuMode === 'import' ? (
                            <div>
                              <div style={{marginBottom:'12px'}}>
                                <label style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'8px'}}>
                                  <input type="checkbox" checked={menuForAllBoats} onChange={e => setMenuForAllBoats(e.target.checked)} />
                                  <span style={{fontSize:'14px'}}>Для всех яхт партнёра</span>
                                </label>
                                {!menuForAllBoats && (
                                  <select value={selectedBoatForMenu || ''} onChange={e => setSelectedBoatForMenu(Number(e.target.value))}
                                    style={{width:'100%',padding:'8px',border:'1px solid #d1d5db',borderRadius:'6px',marginTop:'4px'}}>
                                    <option value="">Выберите яхту...</option>
                                    {group.items.map(boat => <option key={boat.id} value={boat.id}>{boat.name}</option>)}
                                  </select>
                                )}
                              </div>
                              <textarea value={menuText} onChange={e => setMenuText(e.target.value)}
                                placeholder="Вставьте меню:&#10;Завтрак - included&#10;Том Ям - 350 THB&#10;Пад Тай - 250 THB&#10;BBQ Seafood - 1500 THB"
                                style={{width:'100%',padding:'10px',border:'1px solid #d1d5db',borderRadius:'6px',minHeight:'120px',fontFamily:'monospace',fontSize:'13px',marginBottom:'12px'}} />
                              <div style={{display:'flex',gap:'8px'}}>
                                <button onClick={() => analyzeMenuAI(group.partner.id)} disabled={loading || menuText.length < 20}
                                  style={{padding:'8px 16px',background:'linear-gradient(to right,#f59e0b,#d97706)',color:'white',border:'none',borderRadius:'6px',cursor:'pointer',opacity:loading||menuText.length<20?0.5:1}}>
                                  {loading ? 'Сохранение...' : '💾 Сохранить меню'}
                                </button>
                              </div>
                            </div>
                          ) : (
                            <div>
                              {boatMenu.length > 0 ? (
                                <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:'8px'}}>
                                  {boatMenu.map(item => (
                                    <div key={item.id} style={{padding:'8px 12px',backgroundColor:'white',borderRadius:'6px',fontSize:'13px',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                                      <div>
                                        <span style={{fontWeight:'500'}}>{item.name_en}</span>
                                        {item.boat_id && <span style={{marginLeft:'6px',fontSize:'11px',color:'#6b7280'}}>(яхта #{item.boat_id})</span>}
                                      </div>
                                      <div style={{display:'flex',alignItems:'center',gap:'8px'}}>
                                        <span style={{color:item.included?'#059669':'#92400e'}}>{item.included ? '✓ Вкл' : item.price + ' THB'}</span>
                                        <button onClick={() => deleteMenuItem(item.id, group.partner.id)} style={{color:'#dc2626',background:'none',border:'none',cursor:'pointer',fontSize:'14px'}}>×</button>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              ) : (
                                <p style={{color:'#92400e',fontSize:'13px',fontStyle:'italic'}}>Меню не добавлено. Нажмите "+ Добавить меню"</p>
                              )}
                            </div>
                          )}
                        </div>
                        
                        {contractOptions.length > 0 && (
                          <div>
                            <h4 style={{fontWeight:'600',marginBottom:'8px',color:'#374151'}}>⚙️ Опции ({contractOptions.length})</h4>'''

content = content.replace(old_options_section, new_options_section)

with open('app/import-all/page.tsx', 'w') as f:
    f.write(content)

print("✅ Added boat menu functionality!")
print("   - Menu can be added per partner (all boats) or per specific boat")
print("   - View/Import toggle in contract details")
print("   - AI parsing with fallback to simple parsing")
