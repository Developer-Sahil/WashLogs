import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { Card } from '../components/ui/Card';
import { Activity, DollarSign, Package } from 'lucide-react';

export function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/dashboard');
        // Backend returns {"total_orders": X, "total_revenue": Y, ...} under "data" wrapper?
        // API.md says data wrapper: {"data": {...}}
        setStats(response.data.data || response.data);
      } catch (err) {
        console.error("Failed to load dashboard stats", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  return (
    <div>
      <h1 style={{ marginBottom: '2rem' }}>Dashboard Overview</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div className="concave" style={{ padding: '1rem', borderRadius: '50%', color: 'var(--primary-color)' }}>
              <Package size={24} />
            </div>
            <div>
              <p>Total Orders</p>
              <h3>{stats?.total_orders || 0}</h3>
            </div>
          </div>
        </Card>
        
        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div className="concave" style={{ padding: '1rem', borderRadius: '50%', color: 'var(--primary-color)' }}>
              <DollarSign size={24} />
            </div>
            <div>
              <p>Total Revenue</p>
              <h3>${(stats?.total_revenue || 0).toFixed(2)}</h3>
            </div>
          </div>
        </Card>

        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div className="concave" style={{ padding: '1rem', borderRadius: '50%', color: 'var(--primary-color)' }}>
              <Activity size={24} />
            </div>
            <div>
              <p>Active Orders</p>
              <h3>{stats?.recent_orders?.length || 0}</h3>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
