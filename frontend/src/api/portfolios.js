import { apiRequest } from './client';

export const getMyPortfolios = async (auth) => {
  return apiRequest('/portfolios/me', {}, auth);
};

export const getPortfolioDetails = async (id, auth) => {
  return apiRequest(`/portfolios/${id}`, {}, auth);
};

export const getPortfolioHoldings = async (id, auth) => {
  return apiRequest(`/portfolios/${id}/holdings`, {}, auth);
};

export const getPortfolioTransactions = async (id, auth) => {
  return apiRequest(`/portfolios/${id}/transactions`, {}, auth);
};

export const createPortfolio = async (data, auth) => {
  return apiRequest('/portfolios/', {
    method: 'POST',
    body: JSON.stringify(data),
  }, auth);
};

export const deletePortfolio = async (id, auth) => {
  return apiRequest(`/portfolios/${id}`, {
    method: 'DELETE',
  }, auth);
};
