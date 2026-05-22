interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  loading?: boolean;
  children: React.ReactNode;
}

export function Button({ 
  children, 
  variant = 'primary', 
  loading = false, 
  className = '', 
  disabled,
  ...props 
}: ButtonProps) {
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  };

  return (
    <button
      className={`px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 ${variants[variant]} ${className}`}
      disabled={loading || disabled}
      {...props}
    >
      {loading ? 'Carregando...' : children}
    </button>
  );
}