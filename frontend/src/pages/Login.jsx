import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setError(error.message);
    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', width: '100%' }}>
      <Card style={{ width: '400px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>WashLogs Login</h2>
        <form onSubmit={handleLogin}>
          <Input 
            label="Email" 
            type="email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
            required 
          />
          <Input 
            label="Password" 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            required 
          />
          {error && <p style={{ color: 'var(--error)', marginTop: '1rem', textAlign: 'center' }}>{error}</p>}
          <Button type="submit" variant="primary" style={{ width: '100%', marginTop: '1.5rem' }} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </Button>
          
          <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Don't have an account?</span>{' '}
            <Link to="/signup" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 'bold' }}>
              Sign up
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
}
