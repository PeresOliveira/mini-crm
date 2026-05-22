// src/App.tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { ClientesPage } from './pages/ClientesPage';

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex space-x-8">
              <Link to="/" className="flex items-center text-gray-900 font-medium">
                <span className="text-xl"></span>
                <span className="ml-2 font-semibold">Mini CRM</span>
              </Link>
              <Link 
                to="/clientes" 
                className="flex items-center text-gray-600 hover:text-gray-900 border-b-2 border-transparent hover:border-blue-500 transition-colors"
              >
                Clientes
              </Link>
            </div>
            <div className="flex items-center text-sm text-gray-500">
              <span>v1.0.0</span>
            </div>
          </div>
        </div>
      </nav>

      {/* Conteúdo principal */}
      <main className="max-w-7xl mx-auto">
        {children}
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<ClientesPage />} />
          <Route path="/clientes" element={<ClientesPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;