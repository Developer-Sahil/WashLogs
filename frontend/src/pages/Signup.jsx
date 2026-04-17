import React, { useState } from 'react';
import { supabase } from '../lib/supabase';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import { Link, useNavigate } from 'react-router-dom';

export function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);
    
    const { data, error } = await supabase.auth.signUp({ 
      email, 
      password 
    });
    
    if (error) {
      setError(error.message);
    } else {
      setSuccess(true);
      // Wait a moment before redirecting to allow user to see success message
      setTimeout(() => navigate('/'), 2000);
    }
    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', width: '100%' }}>
      <Card style={{ width: '400px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>Create Account</h2>
        <form onSubmit={handleSignup}>
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
          {success && <p style={{ color: '#2b7a2b', marginTop: '1rem', textAlign: 'center' }}>Account created successfully! Redirecting...</p>}
          
          <Button type="submit" variant="primary" style={{ width: '100%', marginTop: '1.5rem' }} disabled={loading}>
            {loading ? 'Signing up...' : 'Sign Up'}
          </Button>
          
          <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Already have an account?</span>{' '}
            <Link to="/login" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 'bold' }}>
              Log in
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
}
