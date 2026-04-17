import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export function OrdersList() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await api.get('/orders');
      setOrders(response.data.data || response.data);
    } catch (err) {
      console.error("Failed to load orders", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const updateStatus = async (id, newStatus) => {
    try {
      await api.patch(`/orders/${id}/status`, { status: newStatus });
      fetchOrders(); // refresh
    } catch (err) {
      console.error("Failed to update status", err);
    }
  };

  const deleteOrder = async (id) => {
    if(!confirm("Are you sure you want to delete this order?")) return;
    try {
      await api.delete(`/orders/${id}`);
      fetchOrders();
    } catch (err) {
      console.error("Failed to delete order", err);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Orders Ledger</h1>
        <Button onClick={fetchOrders} variant="secondary">Refresh</Button>
      </div>

      <Card style={{ padding: 0, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--shadow-dark)', backgroundColor: 'rgba(0,0,0,0.05)' }}>
              <th style={{ padding: '1rem' }}>ID</th>
              <th style={{ padding: '1rem' }}>Customer</th>
              <th style={{ padding: '1rem' }}>Status</th>
              <th style={{ padding: '1rem' }}>Total</th>
              <th style={{ padding: '1rem' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="5" style={{ padding: '2rem', textAlign: 'center' }}>Loading...</td></tr>
            ) : orders.length === 0 ? (
              <tr><td colSpan="5" style={{ padding: '2rem', textAlign: 'center' }}>No orders found.</td></tr>
            ) : (
              orders.map(order => (
                <tr key={order.id} style={{ borderBottom: '1px solid var(--shadow-dark)' }}>
                  <td style={{ padding: '1rem', fontFamily: 'monospace', fontSize: '0.85rem' }}>{order.id.split('-')[0]}</td>
                  <td style={{ padding: '1rem' }}>
                    <strong>{order.customer_name}</strong><br/>
                    <small>{order.phone_number}</small>
                  </td>
                  <td style={{ padding: '1rem' }}>
                    <span className="concave" style={{ padding: '0.25rem 0.75rem', borderRadius: '12px', fontSize: '0.85rem', fontWeight: 600 }}>
                      {order.status}
                    </span>
                  </td>
                  <td style={{ padding: '1rem', fontWeight: 600 }}>${order.total_amount.toFixed(2)}</td>
                  <td style={{ padding: '1rem', display: 'flex', gap: '0.5rem' }}>
                    {order.status === 'RECEIVED' && (
                       <Button onClick={() => updateStatus(order.id, 'PROCESSING')} variant="primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>Process</Button>
                    )}
                    {order.status === 'PROCESSING' && (
                       <Button onClick={() => updateStatus(order.id, 'READY')} variant="secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>Ready</Button>
                    )}
                    {order.status === 'READY' && (
                       <Button onClick={() => updateStatus(order.id, 'DELIVERED')} variant="primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>Deliver</Button>
                    )}
                    <Button onClick={() => deleteOrder(order.id)} variant="danger" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>Del</Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
