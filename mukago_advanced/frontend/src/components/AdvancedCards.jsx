import React from 'react';
import '../styles/AdvancedCards.css';

/**
 * Premium Feature Card Component
 * Used for displaying feature highlights with icons and descriptions
 */
export const FeatureCard = ({ icon, title, description, color = 'gold' }) => {
  return (
    <div className={`feature-card feature-card-${color}`}>
      <div className="feature-card-icon">
        {icon}
      </div>
      <div className="feature-card-content">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
      <div className="feature-card-accent"></div>
    </div>
  );
};

/**
 * Premium Stat Card Component
 * Used for displaying key metrics and statistics
 */
export const StatCard = ({ label, value, change, icon, trend = 'up' }) => {
  return (
    <div className="stat-card-premium">
      <div className="stat-card-header">
        <span className="stat-icon">{icon}</span>
        <span className={`stat-trend trend-${trend}`}>
          {trend === 'up' ? '↑' : '↓'} {change}%
        </span>
      </div>
      <div className="stat-card-body">
        <p className="stat-label">{label}</p>
        <h2 className="stat-value">{value}</h2>
      </div>
      <div className="stat-card-bar">
        <div className="stat-bar-fill"></div>
      </div>
    </div>
  );
};

/**
 * Premium Account Card Component
 * Used for displaying bank account information
 */
export const AccountCard = ({ accountNumber, accountType, balance, currency = 'USD' }) => {
  return (
    <div className="account-card">
      <div className="account-card-header">
        <div className="account-logo">MCB</div>
        <div className="account-chip"></div>
      </div>
      <div className="account-card-body">
        <p className="account-type">{accountType}</p>
        <p className="account-number">{accountNumber}</p>
      </div>
      <div className="account-card-footer">
        <div>
          <p className="balance-label">Balance</p>
          <p className="balance-value">{currency} {balance.toLocaleString()}</p>
        </div>
        <div className="account-card-brand">VISA Infinite</div>
      </div>
    </div>
  );
};

/**
 * Premium Transaction Card Component
 * Used for displaying transaction history
 */
export const TransactionCard = ({ type, description, amount, date, status = 'completed' }) => {
  const getIcon = (transactionType) => {
    const icons = {
      transfer: '💸',
      deposit: '📥',
      withdrawal: '📤',
      investment: '📈',
      payment: '💳'
    };
    return icons[transactionType] || '💰';
  };

  return (
    <div className="transaction-card">
      <div className="transaction-icon">{getIcon(type)}</div>
      <div className="transaction-content">
        <h4>{description}</h4>
        <p className="transaction-date">{date}</p>
      </div>
      <div className="transaction-amount">
        <p className={`amount amount-${type}`}>{amount}</p>
        <span className={`status-badge status-${status}`}>{status}</span>
      </div>
    </div>
  );
};

/**
 * Premium Investment Card Component
 * Used for displaying investment portfolio items
 */
export const InvestmentCard = ({ symbol, name, shares, value, change, chartColor = '#d4af37' }) => {
  return (
    <div className="investment-card">
      <div className="investment-header">
        <div>
          <h4>{symbol}</h4>
          <p>{name}</p>
        </div>
        <span className={`change-badge ${change >= 0 ? 'positive' : 'negative'}`}>
          {change >= 0 ? '+' : ''}{change}%
        </span>
      </div>
      <div className="investment-body">
        <div className="investment-shares">
          <p>Shares</p>
          <h3>{shares}</h3>
        </div>
        <div className="investment-chart">
          <svg viewBox="0 0 100 40" style={{ color: chartColor }}>
            <polyline
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              points="0,30 10,25 20,20 30,15 40,10 50,5 60,15 70,10 80,20 90,15 100,10"
            />
          </svg>
        </div>
      </div>
      <div className="investment-footer">
        <p>Total Value</p>
        <h2>{value}</h2>
      </div>
    </div>
  );
};

/**
 * Premium Module Card Component
 * Used for displaying platform modules
 */
export const ModuleCard = ({ number, title, description, icon, color }) => {
  return (
    <div className={`module-card module-card-${color}`}>
      <div className="module-number">{number}</div>
      <div className="module-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="module-accent"></div>
    </div>
  );
};

/**
 * Premium Alert Card Component
 * Used for displaying alerts and notifications
 */
export const AlertCard = ({ type = 'info', title, message, action }) => {
  return (
    <div className={`alert-card alert-${type}`}>
      <div className="alert-icon">
        {type === 'success' && '✓'}
        {type === 'error' && '✕'}
        {type === 'warning' && '⚠'}
        {type === 'info' && 'ℹ'}
      </div>
      <div className="alert-content">
        <h4>{title}</h4>
        <p>{message}</p>
      </div>
      {action && (
        <button className="alert-action">{action}</button>
      )}
    </div>
  );
};

/**
 * Premium Portfolio Allocation Card Component
 * Used for displaying capital allocation breakdown
 */
export const AllocationCard = ({ title, items }) => {
  const total = items.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="allocation-card">
      <h3>{title}</h3>
      <div className="allocation-items">
        {items.map((item, index) => (
          <div key={index} className="allocation-item">
            <div className="allocation-label">
              <span className={`allocation-dot allocation-dot-${item.color}`}></span>
              <span>{item.label}</span>
            </div>
            <div className="allocation-bar">
              <div
                className={`allocation-fill allocation-fill-${item.color}`}
                style={{ width: `${(item.value / total) * 100}%` }}
              ></div>
            </div>
            <span className="allocation-value">{item.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * Premium User Profile Card Component
 * Used for displaying user information
 */
export const UserProfileCard = ({ name, email, role, avatar, status = 'online' }) => {
  return (
    <div className="user-profile-card">
      <div className="user-avatar">
        {avatar ? (
          <img src={avatar} alt={name} />
        ) : (
          <div className="avatar-placeholder">{name.charAt(0)}</div>
        )}
        <span className={`status-indicator status-${status}`}></span>
      </div>
      <div className="user-info">
        <h3>{name}</h3>
        <p className="user-email">{email}</p>
        <span className="user-role">{role}</span>
      </div>
    </div>
  );
};

/**
 * Premium Loading Card Component
 * Used for loading states
 */
export const LoadingCard = () => {
  return (
    <div className="loading-card">
      <div className="loading-skeleton">
        <div className="skeleton-header"></div>
        <div className="skeleton-line"></div>
        <div className="skeleton-line"></div>
      </div>
    </div>
  );
};
