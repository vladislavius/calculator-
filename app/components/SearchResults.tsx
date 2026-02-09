'use client';

import { useCharterStore } from '../store/useCharterStore';
import { SearchResult } from '../lib/types';
import BoatCard from './BoatCard';
import { useIsMobile } from '../hooks/useIsMobile';

interface SearchResultsProps {
  onSelectBoat: (boat: SearchResult) => void;
}

export default function SearchResults({ onSelectBoat }: SearchResultsProps) {
  const results = useCharterStore(s => s.results);
  const loading = useCharterStore(s => s.loading);
  const searchDate = useCharterStore(s => s.searchDate);
  const showAgentPrice = useCharterStore(s => s.showAgentPrice);
  const markupPercent = useCharterStore(s => s.markupPercent);
  const isMobile = useIsMobile();

  if (results.length > 0) {
    return (
      <div>
        <h2 style={{ margin: '0 0 12px', fontSize: isMobile ? '15px' : '18px', color: '#1e293b' }}>
          Найдено: {results.length} на {searchDate}
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fill, minmax(350px, 1fr))', gap: isMobile ? '8px' : '16px' }}>
          {results.map((boat, i) => (
            <BoatCard key={i} boat={boat} showAgentPrice={showAgentPrice} markupPercent={markupPercent} onSelect={onSelectBoat} />
          ))}
        </div>
      </div>
    );
  }
  if (!loading) {
    return <p style={{ textAlign: 'center', color: '#64748b', padding: '40px' }}>Выберите параметры и нажмите "Найти лодки"</p>;
  }
  return null;
}
