import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const fetchPrices = async (startDate = null, endDate = null) => {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;
  
  const response = await api.get('/prices', { params });
  return response.data;
};

export const fetchChangepoints = async () => {
  const response = await api.get('/changepoints');
  return response.data;
};

export const fetchEvents = async (startDate = null, endDate = null, category = null) => {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;
  if (category) params.category = category;
  
  const response = await api.get('/events', { params });
  return response.data;
};

export const fetchCorrelations = async () => {
  const response = await api.get('/correlations');
  return response.data;
};

export const fetchStatistics = async () => {
  const response = await api.get('/statistics');
  return response.data;
};

export const fetchVolatility = async (window = 30) => {
  const response = await api.get('/volatility', { params: { window } });
  return response.data;
};

export default api;
