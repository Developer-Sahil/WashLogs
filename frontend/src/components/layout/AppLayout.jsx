import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/Button';
import { LogOut, LayoutDashboard, ListOrdered, PlusCircle } from 'lucide-react';
import '../ui/ui.css';

export function AppLayout() {
  const { signOut } = useAuth();

  return (
    <div style={{ display: 'flex', width: '100%', minHeight: '100vh', backgroundColor: 'var(--bg-color)' }}>
      {/* Sidebar */}
      <aside className="convex" style={{ width: '250px', padding: '1.5rem', margin: '1rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        <div>
          <h2 style={{ color: 'var(--primary-color-dark)', marginBottom: '0.2rem' }}>WashLogs</h2>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Management System</p>
        </div>
        
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
          <NavLink 
            to="/" 
            className={({isActive}) => `ui-button ${isActive ? 'ui-button-primary convex' : 'ui-button-secondary concave'}`}
            end
          >
            <LayoutDashboard size={18} /> Dashboard
          </NavLink>
          <NavLink 
            to="/orders" 
            className={({isActive}) => `ui-button ${isActive ? 'ui-button-primary convex' : 'ui-button-secondary concave'}`}
            end
          >
            <ListOrdered size={18} /> Orders
          </NavLink>
          <NavLink 
            to="/orders/new" 
            className={({isActive}) => `ui-button ${isActive ? 'ui-button-primary convex' : 'ui-button-secondary concave'}`}
          >
            <PlusCircle size={18} /> New Order
          </NavLink>
        </nav>

        <Button variant="danger" onClick={signOut} style={{ marginTop: 'auto' }}>
          <LogOut size={18} /> Logout
        </Button>
      </aside>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: '2rem', display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
        <Outlet />
      </main>
    </div>
  );
}
