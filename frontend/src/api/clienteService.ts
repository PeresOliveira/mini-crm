import { apiClient } from './client';
import type { Cliente, ClienteCreate, ClienteUpdate } from '../types/cliente';

export const clienteService = {
  async listar(params?: {
    skip?: number;
    limit?: number;
    nome_contains?: string;
    email_contains?: string;
  }): Promise<Cliente[]> {
    const response = await apiClient.get('/clientes/', { params });
    return response.data;
  },

  async buscarPorId(id: number): Promise<Cliente> {
    const response = await apiClient.get(`/clientes/${id}`);
    return response.data;
  },

  async criar(data: ClienteCreate): Promise<Cliente> {
    const response = await apiClient.post('/clientes/', data);
    return response.data;
  },

  async atualizar(id: number, data: ClienteUpdate): Promise<Cliente> {
    const response = await apiClient.put(`/clientes/${id}`, data);
    return response.data;
  },

  async deletar(id: number): Promise<void> {
    await apiClient.delete(`/clientes/${id}`);
  },
};