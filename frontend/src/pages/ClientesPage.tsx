import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { clienteService } from '../api/clienteService';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { EmptyState } from '../components/common/EmptyState';
import type { Cliente } from '../types/cliente';

export function ClientesPage() {
  const [search, setSearch] = useState('');
  const [showForm, setShowForm] = useState(false);
  const queryClient = useQueryClient();

  const { data: clientes = [], isLoading, error } = useQuery({
    queryKey: ['clientes', search],
    queryFn: () => clienteService.listar({ nome_contains: search || undefined }),
  });

  const deleteMutation = useMutation({
    mutationFn: clienteService.deletar,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clientes'] });
    },
  });

  if (isLoading) return <LoadingSpinner />;

  if (error) {
    return (
      <div className="p-8 text-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 max-w-md mx-auto">
          <p className="text-red-600 font-medium">Erro ao carregar clientes</p>
          <p className="text-red-500 text-sm mt-1">
            Verifique se a API está rodando em http://localhost:8000
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
          <p className="text-gray-600 mt-1">Gerencie todos os seus clientes em um só lugar</p>
        </div>
        <Button onClick={() => setShowForm(true)}>+ Novo Cliente</Button>
      </div>

      {/* Busca */}
      <div className="mb-6">
        <Input
          placeholder="🔍 Buscar por nome ou email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Tabela ou Empty State */}
      {clientes.length === 0 ? (
        <EmptyState
          title="Nenhum cliente encontrado"
          description={search ? "Tente buscar por outro termo" : "Comece cadastrando seu primeiro cliente"}
          action={!search && <Button onClick={() => setShowForm(true)}>Cadastrar Cliente</Button>}
        />
      ) : (
        <>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cliente
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contato
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cadastro
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {clientes.map((cliente: Cliente) => (
                  <tr key={cliente.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      #{cliente.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{cliente.nome}</div>
                      <div className="text-sm text-gray-500">ID: {cliente.id}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{cliente.email}</div>
                      <div className="text-sm text-gray-500">{cliente.telefone || 'Sem telefone'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(cliente.data_cadastro).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-3">
                      <button className="text-blue-600 hover:text-blue-900 transition-colors">
                        Editar
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm(`Tem certeza que deseja excluir "${cliente.nome}"?`)) {
                            deleteMutation.mutate(cliente.id);
                          }
                        }}
                        className="text-red-600 hover:text-red-900 transition-colors"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Estatísticas rápidas */}
          <div className="mt-6 text-sm text-gray-500 text-center">
            Total: {clientes.length} cliente{clientes.length !== 1 ? 's' : ''}
            {search && ` (filtrado por: "${search}")`}
          </div>
        </>
      )}
    </div>
  );
}