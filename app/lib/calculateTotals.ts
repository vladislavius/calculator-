import { SearchResult, SelectedExtra } from './types';

interface CalcParams {
  selectedBoat: SearchResult | null;
  selectedExtras: SelectedExtra[];
  cateringOrders: any[];
  drinkOrders: any[];
  selectedToys: any[];
  selectedServices: any[];
  selectedFees: any[];
  selectedPartnerWatersports: any[];
  transferPickup: any;
  transferDropoff: any;
  transferPrice: number;
  transferMarkup: number;
  landingEnabled: boolean;
  landingFee: number;
  defaultParkFeeEnabled: boolean;
  defaultParkFee: number;
  defaultParkFeeAdults: number;
  defaultParkFeeChildren: number;
  corkageFee: number;
  extraAdults: number;
  children3to11: number;
  childrenUnder3: number;
  adults: number;
  customAdultPrice: number | null;
  customChildPrice: number | null;
  boatMarkup: number;
  fixedMarkup: number;
  markupMode: "percent" | "fixed";
  markupPercent: number;
  customPrices: Record<string, number>;
}

export interface CalcResult {
  agent: number;
  client: number;
  childrenDiscount: number;
  extras: number;
  catering: number;
  drinks: number;
  toys: number;
  services: number;
  transfer: number;
  fees: number;
  partnerWatersports: number;
  markup: number;
  totalAgent: number;
  totalClient: number;
}

export function calculateTotals(p: CalcParams): CalcResult {
  if (!p.selectedBoat) {
    return { agent: 0, client: 0, childrenDiscount: 0, extras: 0, catering: 0, drinks: 0, toys: 0, services: 0, transfer: 0, fees: 0, partnerWatersports: 0, markup: 0, totalAgent: 0, totalClient: 0 };
  }

  const baseAgent = Number(p.selectedBoat.calculated_agent_total) || Number(p.selectedBoat.base_price) || 0;
  const baseClient = Number(p.selectedBoat.calculated_total) || Number(p.selectedBoat.base_price) || 0;

  const extrasTotal = p.selectedExtras.reduce((sum, e) => sum + (e.price * e.quantity), 0);
  const cateringTotal = p.cateringOrders.reduce((sum, c) => sum + (c.pricePerPerson * c.persons), 0);
  const drinksTotal = p.drinkOrders.reduce((sum, d: any) => sum + ((d.price || 0) * (d.quantity || 1)), 0) + p.corkageFee;
  const toysTotal = p.selectedToys.reduce((sum, t: any) => sum + ((t.pricePerHour || 0) * (t.hours || 1) + (t.pricePerDay || 0) * (t.days || 0)) * (t.quantity || 1), 0);
  const servicesTotal = p.selectedServices.reduce((sum, s: any) => sum + ((s.price || 0) * (s.quantity || 1)), 0);

  let transferTotal = p.transferPickup.price + p.transferDropoff.price;
  if (p.transferPrice > 0) {
    transferTotal += Math.round(p.transferPrice * (1 + p.transferMarkup / 100));
  }

  const partnerWatersportsTotal = p.selectedPartnerWatersports.reduce((sum, w) => {
    const pricePerHour = Number(w.pricePerHour) || 0;
    const pricePerDay = Number(w.pricePerDay) || 0;
    const hours = Number(w.hours) || 0;
    const days = Number(w.days) || 0;
    return sum + (pricePerHour * hours) + (pricePerDay * days);
  }, 0);

  const feesTotal = p.selectedFees.reduce((sum, f: any) => sum + ((f.pricePerPerson || 0) * (f.adults + f.children)), 0)
    + (p.landingEnabled ? p.landingFee : 0)
    + (p.defaultParkFeeEnabled ? p.defaultParkFee * (p.defaultParkFeeAdults + p.defaultParkFeeChildren) : 0);

  const allExtras = extrasTotal + cateringTotal + drinksTotal + toysTotal + servicesTotal + transferTotal + feesTotal + partnerWatersportsTotal;

  const adultPriceToUse = p.customAdultPrice !== null ? p.customAdultPrice : (p.selectedBoat?.extra_pax_price || 0);
  const childPriceToUse = p.customChildPrice !== null ? p.customChildPrice : (p.selectedBoat?.child_price_3_11 || Math.round((p.selectedBoat?.extra_pax_price || 0) * 0.5));
  const extraAdultsSurcharge = p.extraAdults * adultPriceToUse;
  const children3to11Surcharge = p.children3to11 * childPriceToUse;
  const extraGuestsSurcharge = extraAdultsSurcharge + children3to11Surcharge;

  const boatPriceWithMarkup = p.markupMode === "fixed" ? baseClient + p.fixedMarkup : Math.round(baseClient * (1 + p.boatMarkup / 100));
  const totalBeforeMarkup = boatPriceWithMarkup + extraGuestsSurcharge + allExtras;
  const markupAmount = p.markupPercent > 0 ? Math.round(totalBeforeMarkup * p.markupPercent / 100) : 0;

  return {
    agent: baseAgent,
    client: baseClient,
    childrenDiscount: 0,
    extras: extrasTotal,
    catering: cateringTotal,
    drinks: drinksTotal,
    toys: toysTotal,
    services: servicesTotal,
    transfer: transferTotal,
    fees: feesTotal,
    partnerWatersports: partnerWatersportsTotal,
    markup: markupAmount,
    totalAgent: baseAgent + allExtras,
    totalClient: totalBeforeMarkup + markupAmount
  };
}
