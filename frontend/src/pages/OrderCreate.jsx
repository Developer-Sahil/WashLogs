import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { PlusCircle, Trash2 } from 'lucide-react';

export function OrderCreate() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    customer_name: '',
    phone_number: '',
    items: [{ garment_type: 'Shirt', quantity: 1, price_per_item: 10.0 }]
  });

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { garment_type: 'Shirt', quantity: 1, price_per_item: 10.0 }]
    }));
  };

  const removeItem = (index) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const handleItemChange = (index, field, value) => {
    setFormData(prev => {
      const newItems = [...prev.items];
      newItems[index][field] = value;
      return { ...prev, items: newItems };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/orders', formData);
      navigate('/orders');
    } catch (err) {
      console.error("Failed to create order", err);
      alert("Failed to create order. Please check the inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', width: '100%' }}>
      <h1 style={{ marginBottom: '2rem' }}>New Order</h1>
      
      <form onSubmit={handleSubmit}>
        <Card style={{ marginBottom: '2rem' }}>
          <h3>Customer Details</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <Input 
              label="Customer Name" 
              value={formData.customer_name} 
              onChange={e => setFormData({...formData, customer_name: e.target.value})} 
              required 
            />
            <Input 
              label="Phone Number" 
              value={formData.phone_number} 
              onChange={e => setFormData({...formData, phone_number: e.target.value})} 
              required 
            />
          </div>
        </Card>

        <Card style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>Garments</h3>
            <Button type="button" onClick={addItem} variant="secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>
              <PlusCircle size={16} /> Add Item
            </Button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            {formData.items.map((item, index) => (
              <div key={index} className="concave" style={{ padding: '1rem', display: 'flex', gap: '1rem', alignItems: 'flex-end' }}>
                <div style={{ flex: 2 }}>
                  <label className="ui-label">Garment Type</label>
                  <select 
                    className="ui-input concave" 
                    value={item.garment_type} 
                    onChange={e => handleItemChange(index, 'garment_type', e.target.value)}
                    style={{ marginTop: '0.5rem' }}
                  >
                    {['Shirt', 'Pants', 'Saree', 'Dress', 'Skirt', 'Jacket', 'Coat', 'Sweater', 'Blouse', 'Other'].map(opt => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                </div>
                <div style={{ flex: 1 }}>
                  <Input 
                    label="QTY" 
                    type="number" 
                    min="1" 
                    value={item.quantity} 
                    onChange={e => handleItemChange(index, 'quantity', parseInt(e.target.value) || 1)} 
                    style={{ marginBottom: 0 }}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <Input 
                    label="Price ($)" 
                    type="number" 
                    step="0.01" 
                    min="0" 
                    value={item.price_per_item} 
                    onChange={e => handleItemChange(index, 'price_per_item', parseFloat(e.target.value) || 0)} 
                    style={{ marginBottom: 0 }}
                  />
                </div>
                {formData.items.length > 1 && (
                  <Button type="button" onClick={() => removeItem(index)} variant="danger" style={{ padding: '0.75rem', marginBottom: '0.1rem' }}>
                    <Trash2 size={18} />
                  </Button>
                )}
              </div>
            ))}
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
            <h3 style={{ textShadow: 'none' }}>
              Total: ${formData.items.reduce((acc, curr) => acc + (curr.quantity * curr.price_per_item), 0).toFixed(2)}
            </h3>
          </div>
        </Card>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button type="submit" variant="primary" disabled={loading}>
            {loading ? 'Creating...' : 'Submit Order'}
          </Button>
        </div>
      </form>
    </div>
  );
}
