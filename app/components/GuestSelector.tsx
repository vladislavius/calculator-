"use client";

import { useCharterStore } from '../store/useCharterStore';
import { useIsMobile } from '../hooks/useIsMobile';

export default function GuestSelector() {
  const s = useCharterStore();
  const selectedBoat = s.selectedBoat;
  const isMobile = useIsMobile();
  if (!selectedBoat) return null;

  const surcharge = (s.extraAdults * (s.customAdultPrice !== null ? s.customAdultPrice : (selectedBoat.extra_pax_price || 0))) +
    (s.children3to11 * (s.customChildPrice !== null ? s.customChildPrice : (selectedBoat.child_price_3_11 || Math.round((selectedBoat.extra_pax_price || 0) * 0.5))));

  const btn: React.CSSProperties = { width: '28px', height: '28px', border: 'none', borderRadius: '6px', backgroundColor: 'rgba(0,0,0,0.2)', cursor: 'pointer', fontSize: '16px', color: 'white' };

  return (
    <div style={{ marginTop: isMobile ? '8px' : '16px', padding: isMobile ? '10px' : '16px', backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: '12px' }}>
      <p style={{ margin: '0 0 8px', fontWeight: '600', fontSize: isMobile ? '13px' : '15px' }}>👥 Гости на борту</p>

      <div style={{ marginBottom: '8px', padding: isMobile ? '6px' : '10px', backgroundColor: 'rgba(255,255,255,0.3)', borderRadius: '8px', fontSize: isMobile ? '11px' : '13px', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
        <span>Базовая: <strong>{selectedBoat.base_pax || 8}</strong></span>
        <span>•</span>
        <span>Макс: <strong>{selectedBoat.max_guests}</strong></span>
        {selectedBoat.cabin_count > 0 && <><span>•</span><span>🛏️ <strong>{selectedBoat.cabin_count}</strong></span></>}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr 1fr' : 'repeat(3, 1fr)', gap: isMobile ? '6px' : '12px' }}>
        <div style={{ padding: isMobile ? '8px' : '12px', backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: '8px' }}>
          <label style={{ fontSize: isMobile ? '10px' : '12px', opacity: 0.8, display: 'block', marginBottom: '4px' }}>👨 Доп. взрослые</label>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '6px' }}>
            <button onClick={() => s.set({ extraAdults: Math.max(0, s.extraAdults - 1) })} style={btn}>−</button>
            <span style={{ minWidth: '24px', textAlign: 'center', fontWeight: '700', fontSize: isMobile ? '15px' : '18px' }}>{s.extraAdults}</span>
            <button onClick={() => s.set({ extraAdults: s.extraAdults + 1 })} style={btn}>+</button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
            <input type="number" value={s.customAdultPrice !== null ? s.customAdultPrice : (selectedBoat.extra_pax_price || 0)} onChange={(e) => s.set({ customAdultPrice: Number(e.target.value) || 0 })} style={{ width: isMobile ? '50px' : '65px', padding: '3px', border: '1px solid rgba(255,255,255,0.5)', borderRadius: '4px', fontSize: '11px', textAlign: 'right', backgroundColor: 'rgba(255,255,255,0.8)' }} />
            <span style={{ fontSize: '10px', opacity: 0.8 }}>THB</span>
          </div>
        </div>

        <div style={{ padding: isMobile ? '8px' : '12px', backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: '8px' }}>
          <label style={{ fontSize: isMobile ? '10px' : '12px', opacity: 0.8, display: 'block', marginBottom: '4px' }}>👧 Дети 3-11</label>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '6px' }}>
            <button onClick={() => s.set({ children3to11: Math.max(0, s.children3to11 - 1) })} style={btn}>−</button>
            <span style={{ minWidth: '24px', textAlign: 'center', fontWeight: '700', fontSize: isMobile ? '15px' : '18px' }}>{s.children3to11}</span>
            <button onClick={() => s.set({ children3to11: s.children3to11 + 1 })} style={btn}>+</button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
            <input type="number" value={s.customChildPrice !== null ? s.customChildPrice : (selectedBoat.child_price_3_11 || Math.round((selectedBoat.extra_pax_price || 0) * 0.5))} onChange={(e) => s.set({ customChildPrice: Number(e.target.value) || 0 })} style={{ width: isMobile ? '50px' : '65px', padding: '3px', border: '1px solid rgba(255,255,255,0.5)', borderRadius: '4px', fontSize: '11px', textAlign: 'right', backgroundColor: 'rgba(255,255,255,0.8)' }} />
            <span style={{ fontSize: '10px', opacity: 0.8 }}>THB</span>
          </div>
        </div>

        <div style={{ padding: isMobile ? '8px' : '12px', backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: '8px', gridColumn: isMobile ? 'span 2' : 'auto' }}>
          <label style={{ fontSize: isMobile ? '10px' : '12px', opacity: 0.8, display: 'block', marginBottom: '4px' }}>👶 До 3 лет <span style={{ color: '#4ade80' }}>(free)</span></label>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <button onClick={() => s.set({ childrenUnder3: Math.max(0, s.childrenUnder3 - 1) })} style={btn}>−</button>
            <span style={{ minWidth: '24px', textAlign: 'center', fontWeight: '700', fontSize: isMobile ? '15px' : '18px' }}>{s.childrenUnder3}</span>
            <button onClick={() => s.set({ childrenUnder3: s.childrenUnder3 + 1 })} style={btn}>+</button>
          </div>
        </div>
      </div>

      <div style={{ marginTop: '8px', padding: isMobile ? '6px' : '10px', backgroundColor: 'rgba(0,0,0,0.1)', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '4px' }}>
        <span style={{ fontSize: isMobile ? '12px' : '14px' }}>Всего: <strong>{(selectedBoat.base_pax || 8) + s.extraAdults + s.children3to11 + s.childrenUnder3}</strong> из {selectedBoat.max_guests}</span>
        {surcharge > 0 && <span style={{ fontWeight: '700', fontSize: isMobile ? '13px' : '16px', color: '#fbbf24' }}>+{surcharge.toLocaleString()} THB</span>}
      </div>
    </div>
  );
}
