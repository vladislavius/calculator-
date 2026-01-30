with open('app/page.tsx', 'r') as f:
    content = f.read()

# Найдём старую функцию generatePDF и заменим на print-версию
old_pdf_start = "const generatePDF = () => {"

new_generate_pdf = '''const generatePDF = () => {
    const totals = calculateTotals();
    const boatPriceForClient = Math.round((selectedBoat.calculated_total || 0) * (1 + boatMarkup / 100));
    const finalTotal = boatPriceForClient + totals.catering + totals.drinks + totals.toys + totals.services + totals.fees + totals.transfer;
    
    // Собираем включённые опции
    const includedOptions = boatOptions
      .filter(opt => opt.status === 'included')
      .map(opt => opt.option_name_ru || opt.option_name || '')
      .filter(Boolean);
    
    // Собираем питание
    const cateringItems = cateringOrders.map(order => {
      const price = Math.round((order.pricePerPerson || 0) * (order.persons || 1) * (1 + boatMarkup / 100));
      return `<tr><td>${order.packageName || order.name}</td><td>${order.persons} чел</td><td>${price.toLocaleString()} THB</td></tr>`;
    }).join('');
    
    // Собираем напитки
    const drinkItems = drinkOrders.map(order => {
      const drink = boatDrinks.find(d => d.id === order.drinkId);
      const price = (customPrices['drink_' + order.drinkId] || order.price || 0) * order.quantity;
      return `<tr><td>${drink?.name_ru || drink?.name_en || 'Напиток'}</td><td>${order.quantity} шт</td><td>${price.toLocaleString()} THB</td></tr>`;
    }).join('');
    
    // Собираем водные развлечения
    const toysItems = selectedToys.map(toy => {
      const hours = selectedHours[toy.id] || 1;
      const basePrice = customPrices['toy_' + toy.id] || toy.pricePerHour || toy.pricePerDay || 0;
      const total = basePrice * hours;
      return `<tr><td>${toy.name}</td><td>${hours} ч</td><td>${total.toLocaleString()} THB</td></tr>`;
    }).join('');
    
    // Собираем услуги
    const serviceItems = selectedServices.map(s => {
      const price = customPrices['service_' + s.id] || s.price || 0;
      return `<tr><td>${s.name}</td><td>1</td><td>${price.toLocaleString()} THB</td></tr>`;
    }).join('');
    
    // Собираем сборы
    const feeItems = selectedFees.map(fee => {
      const price = (customPrices['fee_' + fee.id] || fee.pricePerPerson || 0) * (fee.adults + fee.children);
      return `<tr><td>${fee.name}</td><td>${fee.adults + fee.children} чел</td><td>${price.toLocaleString()} THB</td></tr>`;
    }).join('');
    
    // Трансфер
    const transferHtml = transferPickup.type !== 'none' && transferPickup.price > 0 
      ? `<tr><td>Трансфер ${transferDirection === 'round_trip' ? '(туда-обратно)' : '(в одну сторону)'}</td><td>${transferPickup.pickup || '-'}</td><td>${transferPickup.price.toLocaleString()} THB</td></tr>`
      : '';

    const printContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Расчёт аренды яхты - ${selectedBoat.boat_name}</title>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #333; }
          .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #2563eb; }
          .logo { font-size: 28px; font-weight: bold; color: #2563eb; margin-bottom: 5px; }
          .subtitle { color: #666; font-size: 14px; }
          .date { color: #999; font-size: 12px; margin-top: 10px; }
          .yacht-info { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; }
          .yacht-name { font-size: 24px; font-weight: bold; margin-bottom: 15px; }
          .yacht-details { display: flex; gap: 30px; flex-wrap: wrap; }
          .yacht-detail { }
          .yacht-detail-label { font-size: 12px; opacity: 0.8; }
          .yacht-detail-value { font-size: 16px; font-weight: 600; }
          .section { margin-bottom: 20px; }
          .section-title { font-size: 16px; font-weight: 600; color: #2563eb; margin-bottom: 10px; padding-bottom: 5px; border-bottom: 2px solid #e5e7eb; }
          .included-list { display: flex; flex-wrap: wrap; gap: 8px; }
          .included-item { background: #f0fdf4; color: #166534; padding: 6px 12px; border-radius: 20px; font-size: 13px; }
          table { width: 100%; border-collapse: collapse; margin-top: 10px; }
          th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
          th { background: #f8fafc; font-weight: 600; color: #374151; }
          td:last-child { text-align: right; font-weight: 500; }
          .total-section { background: linear-gradient(135deg, #7c3aed, #6d28d9); color: white; padding: 25px; border-radius: 12px; margin-top: 30px; }
          .total-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.2); }
          .total-row:last-child { border-bottom: none; }
          .total-row.final { font-size: 20px; font-weight: bold; margin-top: 10px; padding-top: 15px; border-top: 2px solid rgba(255,255,255,0.3); }
          .footer { margin-top: 40px; text-align: center; color: #666; font-size: 12px; padding-top: 20px; border-top: 1px solid #e5e7eb; }
          @media print { body { padding: 20px; } }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="logo">🏝️ ОСТРОВ СОКРОВИЩ</div>
          <div class="subtitle">Аренда яхт на Пхукете</div>
          <div class="date">${new Date().toLocaleDateString('ru-RU', { day: '2-digit', month: 'long', year: 'numeric' })}</div>
        </div>
        
        <div class="yacht-info">
          <div class="yacht-name">🚤 ${selectedBoat.boat_name || 'Яхта'}</div>
          <div class="yacht-details">
            <div class="yacht-detail">
              <div class="yacht-detail-label">Маршрут</div>
              <div class="yacht-detail-value">${selectedBoat.route_name || 'По запросу'}</div>
            </div>
            <div class="yacht-detail">
              <div class="yacht-detail-label">Длительность</div>
              <div class="yacht-detail-value">${selectedBoat.duration || '8 часов'}</div>
            </div>
            <div class="yacht-detail">
              <div class="yacht-detail-label">Макс. гостей</div>
              <div class="yacht-detail-value">${selectedBoat.max_guests || '-'} человек</div>
            </div>
            <div class="yacht-detail">
              <div class="yacht-detail-label">Стоимость яхты</div>
              <div class="yacht-detail-value">${boatPriceForClient.toLocaleString()} THB</div>
            </div>
          </div>
        </div>
        
        ${includedOptions.length > 0 ? `
        <div class="section">
          <div class="section-title">✅ ВКЛЮЧЕНО В СТОИМОСТЬ</div>
          <div class="included-list">
            ${includedOptions.map(opt => `<span class="included-item">${opt}</span>`).join('')}
          </div>
        </div>
        ` : ''}
        
        ${cateringItems ? `
        <div class="section">
          <div class="section-title">🍽️ ПИТАНИЕ</div>
          <table>
            <tr><th>Название</th><th>Кол-во</th><th>Сумма</th></tr>
            ${cateringItems}
          </table>
        </div>
        ` : ''}
        
        ${drinkItems ? `
        <div class="section">
          <div class="section-title">🍺 НАПИТКИ</div>
          <table>
            <tr><th>Название</th><th>Кол-во</th><th>Сумма</th></tr>
            ${drinkItems}
          </table>
        </div>
        ` : ''}
        
        ${toysItems ? `
        <div class="section">
          <div class="section-title">🎿 ВОДНЫЕ РАЗВЛЕЧЕНИЯ</div>
          <table>
            <tr><th>Название</th><th>Время</th><th>Сумма</th></tr>
            ${toysItems}
          </table>
        </div>
        ` : ''}
        
        ${serviceItems ? `
        <div class="section">
          <div class="section-title">👨‍🍳 ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ</div>
          <table>
            <tr><th>Услуга</th><th>Кол-во</th><th>Сумма</th></tr>
            ${serviceItems}
          </table>
        </div>
        ` : ''}
        
        ${feeItems ? `
        <div class="section">
          <div class="section-title">🏝️ ПАРКОВЫЕ СБОРЫ</div>
          <table>
            <tr><th>Название</th><th>Гостей</th><th>Сумма</th></tr>
            ${feeItems}
          </table>
        </div>
        ` : ''}
        
        ${transferHtml ? `
        <div class="section">
          <div class="section-title">🚗 ТРАНСФЕР</div>
          <table>
            <tr><th>Тип</th><th>Адрес</th><th>Сумма</th></tr>
            ${transferHtml}
          </table>
        </div>
        ` : ''}
        
        <div class="total-section">
          <div class="total-row">
            <span>Яхта</span>
            <span>${boatPriceForClient.toLocaleString()} THB</span>
          </div>
          ${totals.catering > 0 ? `<div class="total-row"><span>Питание</span><span>+${totals.catering.toLocaleString()} THB</span></div>` : ''}
          ${totals.drinks > 0 ? `<div class="total-row"><span>Напитки</span><span>+${totals.drinks.toLocaleString()} THB</span></div>` : ''}
          ${totals.toys > 0 ? `<div class="total-row"><span>Водные развлечения</span><span>+${totals.toys.toLocaleString()} THB</span></div>` : ''}
          ${totals.services > 0 ? `<div class="total-row"><span>Услуги</span><span>+${totals.services.toLocaleString()} THB</span></div>` : ''}
          ${totals.fees > 0 ? `<div class="total-row"><span>Парковые сборы</span><span>+${totals.fees.toLocaleString()} THB</span></div>` : ''}
          ${totals.transfer > 0 ? `<div class="total-row"><span>Трансфер</span><span>+${totals.transfer.toLocaleString()} THB</span></div>` : ''}
          <div class="total-row final">
            <span>💰 ИТОГО К ОПЛАТЕ</span>
            <span>${finalTotal.toLocaleString()} THB</span>
          </div>
        </div>
        
        <div class="footer">
          <p><strong>🏝️ Остров Сокровищ</strong> — Аренда яхт на Пхукете</p>
          <p>WhatsApp: +66 XX XXX XXXX • Email: info@ostrov-sokrovisch.com</p>
        </div>
      </body>
      </html>
    `;
    
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(printContent);
      printWindow.document.close();
      printWindow.onload = () => {
        printWindow.print();
      };
    }
  };'''

# Находим начало и конец старой функции
start_idx = content.find(old_pdf_start)
if start_idx != -1:
    # Ищем конец функции (следующая const или функция)
    search_from = start_idx + len(old_pdf_start)
    # Находим закрывающую скобку функции
    brace_count = 1
    end_idx = search_from
    while brace_count > 0 and end_idx < len(content):
        if content[end_idx] == '{':
            brace_count += 1
        elif content[end_idx] == '}':
            brace_count -= 1
        end_idx += 1
    
    # Заменяем
    content = content[:start_idx] + new_generate_pdf + content[end_idx:]
    print("✅ Replaced generatePDF with print version")
else:
    print("❌ generatePDF not found")

with open('app/page.tsx', 'w') as f:
    f.write(content)

print("✅ PDF will now open in new window for printing")
