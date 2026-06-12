import React, { useState, useEffect } from 'react';
import { useLanguage } from '../i18n/useLanguage';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const { t } = useLanguage();
  const [stats, setStats] = useState({
    total_users: 0,
    total_accounts: 0,
    total_transactions: 0,
    total_balance: 0,
    active_users: 0
  });
  const [users, setUsers] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      // Fetch dashboard stats
      const statsResponse = await fetch('http://localhost:5000/api/admin/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Fetch users list
      const usersResponse = await fetch('http://localhost:5000/api/admin/users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (usersResponse.ok) {
        const usersData = await usersResponse.json();
        setUsers(usersData);
      }

      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeactivateUser = async (userId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:5000/api/admin/users/${userId}/deactivate`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        fetchDashboardData();
        alert('User deactivated successfully');
      }
    } catch (err) {
      console.error('Error deactivating user:', err);
      alert('Failed to deactivate user');
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  if (loading) {
    return <div className="admin-loading">{t('common.loading')}</div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>{t('admin.title')}</h1>
        <div className="admin-actions">
          <button className="btn-refresh" onClick={fetchDashboardData}>
            Refresh Data
          </button>
        </div>
      </div>

      {error && <div className="admin-error">{error}</div>}

      <div className="admin-tabs">
        <button
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          {t('admin.dashboard')}
        </button>
        <button
          className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          {t('admin.users')}
        </button>
        <button
          className={`tab-btn ${activeTab === 'accounts' ? 'active' : ''}`}
          onClick={() => setActiveTab('accounts')}
        >
          {t('admin.accounts')}
        </button>
        <button
          className={`tab-btn ${activeTab === 'transactions' ? 'active' : ''}`}
          onClick={() => setActiveTab('transactions')}
        >
          {t('admin.transactions')}
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="admin-overview">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon users-icon">👥</div>
              <div className="stat-content">
                <h3>{t('admin.total_users')}</h3>
                <p className="stat-value">{stats.total_users}</p>
                <p className="stat-subtitle">{stats.active_users} active</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon accounts-icon">💳</div>
              <div className="stat-content">
                <h3>{t('admin.total_accounts')}</h3>
                <p className="stat-value">{stats.total_accounts}</p>
                <p className="stat-subtitle">All accounts</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon transactions-icon">💸</div>
              <div className="stat-content">
                <h3>{t('admin.total_transactions')}</h3>
                <p className="stat-value">{stats.total_transactions}</p>
                <p className="stat-subtitle">Total processed</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon balance-icon">💰</div>
              <div className="stat-content">
                <h3>{t('admin.total_balance')}</h3>
                <p className="stat-value">{formatCurrency(stats.total_balance)}</p>
                <p className="stat-subtitle">Platform total</p>
              </div>
            </div>
          </div>

          <div className="overview-charts">
            <div className="chart-container">
              <h3>System Health</h3>
              <div className="health-indicator">
                <div className="health-status online">● Online</div>
                <div className="health-status">99.9% Uptime</div>
                <div className="health-status">All Systems Operational</div>
              </div>
            </div>

            <div className="chart-container">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                <div className="activity-item">
                  <span className="activity-type">New User Registration</span>
                  <span className="activity-time">2 minutes ago</span>
                </div>
                <div className="activity-item">
                  <span className="activity-type">Large Transaction</span>
                  <span className="activity-time">15 minutes ago</span>
                </div>
                <div className="activity-item">
                  <span className="activity-type">Account Created</span>
                  <span className="activity-time">1 hour ago</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="admin-users">
          <div className="users-table-container">
            <table className="users-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Full Name</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.full_name}</td>
                    <td>
                      <span className={`role-badge role-${user.role}`}>
                        {user.role}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn-action btn-deactivate"
                        onClick={() => handleDeactivateUser(user.id)}
                        disabled={!user.is_active}
                      >
                        Deactivate
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'accounts' && (
        <div className="admin-accounts">
          <div className="placeholder-content">
            <h3>Accounts Management</h3>
            <p>View and manage all user accounts</p>
          </div>
        </div>
      )}

      {activeTab === 'transactions' && (
        <div className="admin-transactions">
          <div className="placeholder-content">
            <h3>Transactions History</h3>
            <p>Monitor all platform transactions</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
