'use client';

import { SearchResult } from '../lib/types';
import { cardStyle } from '../lib/styles';
import { useIsMobile } from '../hooks/useIsMobile';

interface BoatCardProps {
  boat: SearchResult;
  showAgentPrice: boolean;
  markupPercent: number;
  onSelect: (boat: SearchResult) => void;
}

const seasonLabel = (s: string) => {
  const map: Record<string, string> = { 'peak': '🔥 Пик', 'high': '☀️ Высокий', 'low': '🌧️ Низкий', 'all': '📅 Все сезоны' };
  return map[s] || s;
};

export default function BoatCard({ boat, showAgentPrice, markupPercent, onSelect }: BoatCardProps) {
  const isMobile = useIsMobile();

  return (
    <div
      style={{ ...cardStyle, cursor: 'pointer', transition: 'transform 0.2s', border: '2px solid transparent', padding: isMobile ? '12px' : '20px' }}
      onClick={() => onSelect(boat)}
      onMouseOver={(e) => (e.currentTarget.style.borderColor = '#2563eb')}
      onMouseOut={(e) => (e.currentTarget.style.borderColor = 'transparent')}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h3 style={{ margin: 0, fontSize: isMobile ? '15px' : '18px', fontWeight: '600', color: '#111' }}>{boat.boat_name}</h3>
          <p style={{ margin: '2px 0 0', fontSize: isMobile ? '11px' : '13px', color: '#6b7280' }}>{boat.partner_name}</p>
        </div>
        <span style={{ padding: '3px 8px', backgroundColor: '#e0e7ff', color: '#4338ca', borderRadius: '20px', fontSize: isMobile ? '10px' : '12px', fontWeight: '500', height: 'fit-content', whiteSpace: 'nowrap' }}>
          {boat.boat_type}
        </span>
      </div>
      <div style={{ display: 'flex', gap: isMobile ? '8px' : '16px', fontSize: isMobile ? '11px' : '13px', color: '#6b7280', marginBottom: '8px', flexWrap: 'wrap' }}>
        <span>📏 {boat.length_ft}ft</span>
        <span>👥 {boat.max_guests}</span>
        {boat.cabin_count > 0 && <span>🛏️ {boat.cabin_count}</span>}
      </div>
      <div style={{ padding: isMobile ? '8px' : '12px', backgroundColor: '#f8fafc', borderRadius: '8px', marginBottom: '8px' }}>
        <p style={{ margin: 0, fontSize: isMobile ? '12px' : '14px', color: '#374151' }}>🗺️ {boat.route_name}</p>
        {boat.season && <p style={{ margin: '2px 0 0', fontSize: isMobile ? '10px' : '12px', color: '#8b5cf6' }}>{seasonLabel(boat.season || "")}</p>}
        {boat.fuel_surcharge > 0 && <p style={{ margin: '2px 0 0', fontSize: isMobile ? '10px' : '12px', color: '#f59e0b' }}>⛽ +{boat.fuel_surcharge.toLocaleString()}</p>}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {showAgentPrice ? (
          <div>
            <p style={{ margin: 0, fontSize: isMobile ? '10px' : '12px', color: '#6b7280' }}>Agent: <span style={{ fontWeight: '600' }}>{(boat.calculated_agent_total || boat.base_price).toLocaleString()}</span></p>
            <p style={{ margin: '2px 0 0', fontSize: isMobile ? '14px' : '16px', fontWeight: 'bold', color: '#059669' }}>{Math.round((boat.calculated_total || 0) * (1 + markupPercent / 100)).toLocaleString()} THB</p>
            <p style={{ margin: '1px 0 0', fontSize: isMobile ? '10px' : '12px', color: '#7c3aed' }}>Profit: {(Math.round((boat.calculated_total || 0) * (1 + markupPercent / 100)) - (boat.calculated_agent_total || boat.base_price)).toLocaleString()}</p>
          </div>
        ) : (
          <p style={{ margin: 0, fontSize: isMobile ? '16px' : '20px', fontWeight: 'bold', color: '#2563eb' }}>{Math.round((boat.calculated_total || 0) * (1 + markupPercent / 100)).toLocaleString()} THB</p>
        )}
        <button style={{ padding: isMobile ? '8px 12px' : '8px 16px', backgroundColor: '#2563eb', color: 'white', border: 'none', borderRadius: '6px', fontSize: isMobile ? '12px' : '14px', cursor: 'pointer' }}>
          Выбрать →
        </button>
      </div>
    </div>
  );
}
