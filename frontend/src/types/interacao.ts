export type TipoInteracao = 'ligacao' | 'email' | 'reuniao' | 'whatsapp' | 'proposta';

export interface Interacao {
  id: number;
  cliente_id: number;
  tipo: TipoInteracao;
  descricao: string | null;
  data: string;
}

export interface InteracaoCreate {
  cliente_id: number;
  tipo: TipoInteracao;
  descricao?: string | null;
}