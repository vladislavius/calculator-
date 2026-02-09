'use client';

import { useCharterStore } from '../store/useCharterStore';
import { calculateTotals } from '../lib/calculateTotals';

interface SummarySectionProps {
  generatePDF: () => void;
  generateWhatsApp: () => void;
}

export default function SummarySection({ generatePDF, generateWhatsApp }: SummarySectionProps) {
  const s = useCharterStore();
  const selectedBoat = s.selectedBoat!;
  const totals = calculateTotals({
    selectedBoat: s.selectedBoat, selectedExtras: s.selectedExtras,
    cateringOrders: s.cateringOrders, drinkOrders: s.drinkOrders,
    selectedToys: s.selectedToys, selectedServices: s.selectedServices,
    selectedFees: s.selectedFees, selectedPartnerWatersports: s.selectedPartnerWatersports,
    transferPickup: s.transferPickup, transferDropoff: s.transferDropoff,
    transferPrice: s.transferPrice, transferMarkup: s.transferMarkup,
    landingEnabled: s.landingEnabled, landingFee: s.landingFee,
    defaultParkFeeEnabled: s.defaultParkFeeEnabled, defaultParkFee: s.defaultParkFee,
    defaultParkFeeAdults: s.defaultParkFeeAdults, defaultParkFeeChildren: s.defaultParkFeeChildren,
    corkageFee: s.corkageFee, extraAdults: s.extraAdults, children3to11: s.children3to11,
    childrenUnder3: s.childrenUnder3, adults: s.adults,
    customAdultPrice: s.customAdultPrice, customChildPrice: s.customChildPrice,
    boatMarkup: s.boatMarkup, fixedMarkup: s.fixedMarkup,
    markupMode: s.markupMode, markupPercent: s.markupPercent, customPrices: s.customPrices,
  });

  const baseLine = (label: string, value: number) => (
    value > 0 ? (
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.2)' }}>
        <span>{label}</span>
        <span style={{ fontWeight: '600' }}>+{value.toLocaleString()} THB</span>
      </div>
    ) : null
  );

  const guestSurcharge = (s.extraAdults + s.children3to11) > 0
    ? (s.extraAdults * (s.customPrices["extra_adult"] || selectedBoat?.extra_pax_price || 0)) +
      (s.children3to11 * (s.customPrices["child_3_11"] || Math.round((selectedBoat?.extra_pax_price || 0) * 0.5)))
    : 0;

  return (
    <div id="summary" style={{ padding: '24px', background: 'linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)', borderRadius: '16px', color: 'white' }}>
      <h3 style={{ margin: '0 0 20px', fontSize: '20px', fontWeight: '700' }}>📊 ИТОГО</h3>
      
      <div style={{ marginBottom: '20px', padding: '16px', backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: '12px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <span style={{ fontWeight: '600' }}>Наша наценка</span>
          <div style={{ display: 'flex', gap: '4px', backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '8px', padding: '2px' }}>
            <button onClick={() => s.set({ markupMode: 'percent' })} style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontSize: '13px', fontWeight: '600', backgroundColor: s.markupMode === 'percent' ? 'white' : 'transparent', color: s.markupMode === 'percent' ? '#1e40af' : 'rgba(255,255,255,0.7)' }}>%</button>
            <button onClick={() => s.set({ markupMode: 'fixed' })} style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontSize: '13px', fontWeight: '600', backgroundColor: s.markupMode === 'fixed' ? 'white' : 'transparent', color: s.markupMode === 'fixed' ? '#1e40af' : 'rgba(255,255,255,0.7)' }}>THB</button>
          </div>
        </div>
        {s.markupMode === 'percent' ? (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
              <input type="number" min="0" max="500" value={s.boatMarkup} onChange={(e) => s.set({ boatMarkup: Number(e.target.value) || 0 })} style={{ width: '100px', padding: '8px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.3)', backgroundColor: 'rgba(255,255,255,0.1)', color: 'white', fontSize: '20px', fontWeight: 'bold', textAlign: 'center' }} />
              <span style={{ fontSize: '20px', fontWeight: 'bold' }}>%</span>
              <span style={{ fontSize: '13px', opacity: 0.7 }}>= +{Math.round((selectedBoat?.calculated_total || 0) * s.boatMarkup / 100).toLocaleString()} THB</span>
            </div>
            <input type="range" min="0" max="200" value={s.boatMarkup} onChange={(e) => s.set({ boatMarkup: Number(e.target.value) })} style={{ width: '100%', height: '6px', cursor: 'pointer' }} />
          </>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <input type="number" min="0" step="1000" value={s.fixedMarkup} onChange={(e) => s.set({ fixedMarkup: Number(e.target.value) || 0 })} style={{ width: '160px', padding: '8px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.3)', backgroundColor: 'rgba(255,255,255,0.1)', color: 'white', fontSize: '20px', fontWeight: 'bold', textAlign: 'center' }} />
            <span style={{ fontSize: '16px', fontWeight: 'bold' }}>THB</span>
            <span style={{ fontSize: '13px', opacity: 0.7 }}>= {((selectedBoat?.calculated_total || 0) > 0 ? (s.fixedMarkup / (selectedBoat?.calculated_total || 1) * 100).toFixed(1) : 0)}%</span>
          </div>
        )}
      </div>

      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.2)' }}>
          <span>Яхта (базовая цена)</span>
          <span style={{ fontWeight: '600' }}>{(selectedBoat.calculated_total || 0).toLocaleString()} THB</span>
        </div>

        {guestSurcharge > 0 && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.2)' }}>
            <span>Доп. гости ({s.extraAdults} взр + {s.children3to11} дет)</span>
            <span style={{ fontWeight: '600' }}>+{guestSurcharge.toLocaleString()} THB</span>
          </div>
        )}

        {baseLine('Парковые сборы', totals.fees)}
        {baseLine('Питание', totals.catering)}
        {baseLine('Напитки', totals.drinks)}
        {baseLine('Водные развлечения', totals.toys)}
        {baseLine('Водные услуги', totals.partnerWatersports || 0)}
        {baseLine('Персонал', totals.services)}
        {baseLine('Трансфер', totals.transfer)}
        {baseLine('Дополнительные опции', totals.extras)}

        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.2)', color: '#fcd34d' }}>
          <span>Наценка {s.markupMode === 'fixed' ? '(' + s.fixedMarkup.toLocaleString() + ' THB)' : '(' + s.boatMarkup + '%)'}</span>
          <span style={{ fontWeight: '600' }}>+{s.markupMode === 'fixed' ? s.fixedMarkup.toLocaleString() : Math.round((selectedBoat.calculated_total || 0) * s.boatMarkup / 100).toLocaleString()} THB</span>
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '16px 0 0', fontSize: '24px', fontWeight: 'bold' }}>
          <span>💰 ЦЕНА ДЛЯ КЛИЕНТА</span>
          <span>{(totals.totalClient || 0).toLocaleString()} THB</span>
        </div>
      </div>

      <div style={{ marginTop: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '600', color: 'white' }}>📝 Заметки / Примечания:</label>
        <textarea
          value={s.customNotes}
          onChange={(e) => s.set({ customNotes: e.target.value })}
          placeholder="Например: Обед в ресторане - кэш-ваучер 500 THB/чел для спидбота..."
          style={{ width: '100%', padding: '12px', borderRadius: '8px', border: 'none', fontSize: '14px', minHeight: '80px', resize: 'vertical', backgroundColor: 'rgba(255,255,255,0.95)' }}
        />
      </div>

      <div style={{ marginTop: '20px', display: 'flex', gap: '12px' }}>
        <button onClick={generatePDF} style={{ flex: 1, padding: '16px', backgroundColor: 'white', color: '#1e40af', border: 'none', borderRadius: '10px', fontWeight: '700', cursor: 'pointer', fontSize: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          📄 Создать PDF
        </button>
        <button onClick={generateWhatsApp} style={{ flex: 1, padding: '16px', backgroundColor: '#25D366', color: 'white', border: 'none', borderRadius: '10px', fontWeight: '700', cursor: 'pointer', fontSize: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          💬 Отправить в WhatsApp
        </button>
      </div>
    </div>
  );
}
