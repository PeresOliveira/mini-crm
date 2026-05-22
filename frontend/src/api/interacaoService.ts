import { apiClient } from './client';
import type { Interacao, InteracaoCreate } from '../types/interacao';

export const interacaoService = {
  async listarPorCliente(
    clienteId: number,
    params?: { skip?: number; limit?: number; tipo?: string }
  ): Promise<Interacao[]> {
    const response = await apiClient.get(`/interacoes/cliente/${clienteId}`, { params });
    return response.data;
  },

  async criar(data: InteracaoCreate): Promise<Interacao> {
    const response = await apiClient.post('/interacoes/', data);
    return response.data;
  },

  async deletar(id: number): Promise<void> {
    await apiClient.delete(`/interacoes/${id}`);
  },

  async estatisticas(clienteId: number): Promise<any> {
    const response = await apiClient.get(`/interacoes/cliente/${clienteId}/estatisticas`);
    return response.data;
  },
};