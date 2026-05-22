import type { Interacao } from './interacao';

export interface Cliente {
  id: number;
  nome: string;
  email: string;
  telefone: string | null;
  data_cadastro: string;
  interacoes?: Interacao[];
}

export interface ClienteCreate {
  nome: string;
  email: string;
  telefone?: string | null;
}

export interface ClienteUpdate {
  nome?: string;
  email?: string;
  telefone?: string | null;
}