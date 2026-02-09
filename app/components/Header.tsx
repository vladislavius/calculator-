'use client';

import { useCharterStore } from '../store/useCharterStore';
import { useIsMobile } from '../hooks/useIsMobile';

export default function Header() {
  const lang = useCharterStore(s => s.lang);
  const set = useCharterStore(s => s.set);
  const isMobile = useIsMobile();

  return (
    <header style={{ background: 'linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)', color: 'white', padding: isMobile ? '10px 12px' : '20px 24px' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: isMobile ? 'wrap' : 'nowrap', gap: isMobile ? '8px' : '0' }}>
        <div>
          <h1 style={{ fontSize: isMobile ? '16px' : '24px', fontWeight: 'bold', margin: 0 }}>🚤 Phuket Charter Pro</h1>
          {!isMobile && <p style={{ margin: '4px 0 0', opacity: 0.9, fontSize: '14px' }}>Профессиональный калькулятор чартеров</p>}
        </div>
        <div style={{ display: 'flex', gap: isMobile ? '6px' : '12px', alignItems: 'center' }}>
          <a href="/import-all" style={{ padding: isMobile ? '6px 10px' : '8px 16px', backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: '8px', color: 'white', textDecoration: 'none', fontSize: isMobile ? '12px' : '14px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            📦{isMobile ? '' : ' Импорт'}
          </a>
          <a href="/partners" style={{ padding: isMobile ? '6px 10px' : '8px 16px', backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: '8px', color: 'white', textDecoration: 'none', fontSize: isMobile ? '12px' : '14px' }}>
            👥{isMobile ? '' : ' Партнёры'}
          </a>
          <div style={{ display: 'flex', backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '8px', padding: '2px' }}>
            <button onClick={() => set({ lang: 'ru' })} style={{ padding: '6px 10px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontSize: '13px', fontWeight: '600', backgroundColor: lang === 'ru' ? 'white' : 'transparent', color: lang === 'ru' ? '#1e40af' : 'rgba(255,255,255,0.7)' }}>RU</button>
            <button onClick={() => set({ lang: 'en' })} style={{ padding: '6px 10px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontSize: '13px', fontWeight: '600', backgroundColor: lang === 'en' ? 'white' : 'transparent', color: lang === 'en' ? '#1e40af' : 'rgba(255,255,255,0.7)' }}>EN</button>
          </div>
        </div>
      </div>
    </header>
  );
}
