import { apiRequest } from './client';

export const getSecurities = async (auth) => {
  return apiRequest('/securities/', {}, auth);
};

export const buySecurity = async (portfolio_id, ticker, quantity, auth) => {
  return apiRequest('/trades/buy', {
    method: 'POST',
    body: JSON.stringify({ portfolio_id, ticker, quantity }),
  }, auth);
};

export const sellSecurity = async (portfolio_id, ticker, quantity, sale_price, auth) => {
  return apiRequest('/trades/sell', {
    method: 'POST',
    body: JSON.stringify({ portfolio_id, ticker, quantity, sale_price }),
  }, auth);
};
