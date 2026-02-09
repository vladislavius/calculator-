"use client";

import { useCharterStore } from '../store/useCharterStore';
import { calculateTotals } from '../lib/calculateTotals';
import { useIsMobile } from '../hooks/useIsMobile';

export default function ModalHeader({ closeModal }: { closeModal: () => void }) {
  const s = useCharterStore();
  const selectedBoat = s.selectedBoat;
  const isMobile = useIsMobile();
  if (!selectedBoat) return null;

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

  const navLinks = [
    { href: '#included', icon: '✅', label: 'Включено' },
    { href: '#food', icon: '🍽️', label: 'Еда' },
    { href: '#drinks', icon: '🍺', label: 'Напитки' },
    { href: '#toys', icon: '🏄', label: 'Игрушки' },
    { href: '#services', icon: '🎉', label: 'Услуги' },
    { href: '#transfer', icon: '🚗', label: 'Трансфер' },
    { href: '#fees', icon: '🎫', label: 'Сборы' },
    { href: '#summary', icon: '📋', label: 'Итого' },
  ];

  return (
    <>
      <div style={{
        padding: isMobile ? '8px 10px' : '20px 24px',
        borderBottom: '1px solid #e5e7eb',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        backgroundColor: '#f8fafc',
        position: 'sticky', top: 0, zIndex: 10,
      }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h2 style={{ margin: 0, fontSize: isMobile ? '15px' : '22px', fontWeight: 'bold', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {selectedBoat.boat_name}
          </h2>
          <p style={{ margin: '2px 0 0', color: '#6b7280', fontSize: isMobile ? '11px' : '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {selectedBoat.partner_name} • {selectedBoat.route_name}
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: isMobile ? '8px' : '16px', flexShrink: 0 }}>
          <div style={{ textAlign: 'right' }}>
            <p style={{ margin: 0, fontSize: isMobile ? '10px' : '12px', color: '#6b7280' }}>Итого</p>
            <p style={{ margin: 0, fontSize: isMobile ? '15px' : '24px', fontWeight: 'bold', color: '#059669' }}>
              {(totals.totalClient || 0).toLocaleString()}
            </p>
          </div>
          <button onClick={closeModal} style={{ padding: isMobile ? '6px 10px' : '8px 16px', backgroundColor: '#f3f4f6', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: isMobile ? '16px' : '20px' }}>✕</button>
        </div>
      </div>

      <div style={{
        padding: isMobile ? '6px 8px' : '12px 24px',
        borderBottom: '1px solid #e5e7eb',
        backgroundColor: '#fafafa',
        display: 'flex', gap: isMobile ? '2px' : '8px',
        flexWrap: 'nowrap',
        overflowX: 'auto',
        WebkitOverflowScrolling: 'touch',
        position: 'sticky', top: isMobile ? '48px' : 'auto', zIndex: 10,
      }}>
        {navLinks.map(link => (
          <a key={link.href} href={link.href} style={{
            fontSize: isMobile ? '11px' : '13px',
            color: '#2563eb', textDecoration: 'none',
            whiteSpace: 'nowrap',
            padding: isMobile ? '4px 6px' : '4px 8px',
            backgroundColor: isMobile ? '#e0e7ff' : 'transparent',
            borderRadius: '6px', flexShrink: 0,
          }}>
            {link.icon}{isMobile ? '' : ' ' + link.label}
          </a>
        ))}
      </div>
    </>
  );
}
