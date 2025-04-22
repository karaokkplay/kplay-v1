import React, { useState, useEffect } from 'react';
import './Payment.css';

const Payment = ({ onPaymentComplete, onCancel, planSelected = 'monthly' }) => {
  const [paymentMethod, setPaymentMethod] = useState('credit_card');
  const [cardNumber, setCardNumber] = useState('');
  const [cardName, setCardName] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [cvv, setCvv] = useState('');
  const [plan, setPlan] = useState(planSelected);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Planos de assinatura
  const plans = {
    monthly: {
      name: 'Mensal',
      price: 'R$ 9,90',
      description: 'Acesso a todas as funcionalidades por 1 mês',
      features: [
        'Extração ilimitada de acordes',
        'Visualização no teclado virtual',
        'Sincronização de letras',
        'Sem anúncios'
      ]
    },
    quarterly: {
      name: 'Trimestral',
      price: 'R$ 24,90',
      description: 'Acesso a todas as funcionalidades por 3 meses',
      features: [
        'Tudo do plano mensal',
        'Economia de 16%',
        'Suporte prioritário',
        'Download de arquivos MIDI processados'
      ]
    },
    yearly: {
      name: 'Anual',
      price: 'R$ 89,90',
      description: 'Acesso a todas as funcionalidades por 12 meses',
      features: [
        'Tudo do plano trimestral',
        'Economia de 25%',
        'Acesso antecipado a novos recursos',
        'Biblioteca de progressões harmônicas expandida'
      ]
    }
  };

  // Formatar número do cartão
  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = matches && matches[0] || '';
    const parts = [];
    
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    
    if (parts.length) {
      return parts.join(' ');
    } else {
      return value;
    }
  };

  // Formatar data de expiração
  const formatExpiryDate = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    
    if (v.length >= 2) {
      return `${v.substring(0, 2)}/${v.substring(2, 4)}`;
    }
    
    return value;
  };

  // Manipuladores de eventos para campos do cartão
  const handleCardNumberChange = (e) => {
    const formattedValue = formatCardNumber(e.target.value);
    setCardNumber(formattedValue);
  };

  const handleExpiryDateChange = (e) => {
    const formattedValue = formatExpiryDate(e.target.value);
    setExpiryDate(formattedValue);
  };

  const handleCvvChange = (e) => {
    const value = e.target.value.replace(/\D/g, '');
    if (value.length <= 4) {
      setCvv(value);
    }
  };

  // Validar formulário
  const validateForm = () => {
    if (paymentMethod === 'credit_card') {
      if (!cardNumber || cardNumber.replace(/\s/g, '').length < 16) {
        setError('Número de cartão inválido');
        return false;
      }
      
      if (!cardName) {
        setError('Nome no cartão é obrigatório');
        return false;
      }
      
      if (!expiryDate || expiryDate.length < 5) {
        setError('Data de expiração inválida');
        return false;
      }
      
      if (!cvv || cvv.length < 3) {
        setError('CVV inválido');
        return false;
      }
    }
    
    setError('');
    return true;
  };

  // Processar pagamento
  const processPayment = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      // Simulação de processamento de pagamento
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simulação de sucesso
      setSuccess(true);
      
      // Notificar componente pai após 2 segundos
      setTimeout(() => {
        if (onPaymentComplete) {
          onPaymentComplete({
            method: paymentMethod,
            plan,
            date: new Date().toISOString(),
            transactionId: 'txn_' + Math.random().toString(36).substr(2, 9)
          });
        }
      }, 2000);
      
    } catch (err) {
      setError('Erro ao processar pagamento. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="payment-container">
      <div className="payment-card">
        <div className="payment-header">
          <h2>Assinatura K-Play</h2>
          <p>Escolha seu plano e forma de pagamento</p>
        </div>
        
        {error && <div className="payment-error">{error}</div>}
        
        {success ? (
          <div className="payment-success">
            <div className="success-icon">✓</div>
            <h3>Pagamento Confirmado!</h3>
            <p>Sua assinatura foi ativada com sucesso.</p>
            <p>Você receberá um e-mail com os detalhes da sua compra.</p>
          </div>
        ) : (
          <form onSubmit={processPayment}>
            <div className="plan-selection">
              <h3>Escolha seu plano</h3>
              <div className="plan-options">
                {Object.keys(plans).map((planKey) => (
                  <div 
                    key={planKey}
                    className={`plan-option ${plan === planKey ? 'selected' : ''}`}
                    onClick={() => setPlan(planKey)}
                  >
                    <div className="plan-name">{plans[planKey].name}</div>
                    <div className="plan-price">{plans[planKey].price}</div>
                    <div className="plan-description">{plans[planKey].description}</div>
                    {plan === planKey && (
                      <div className="plan-features">
                        <ul>
                          {plans[planKey].features.map((feature, index) => (
                            <li key={index}>{feature}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
            
            <div className="payment-method">
              <h3>Forma de pagamento</h3>
              <div className="payment-options">
                <div 
                  className={`payment-option ${paymentMethod === 'credit_card' ? 'selected' : ''}`}
                  onClick={() => setPaymentMethod('credit_card')}
                >
                  <i className="fas fa-credit-card"></i>
                  <span>Cartão de Crédito</span>
                </div>
                <div 
                  className={`payment-option ${paymentMethod === 'pix' ? 'selected' : ''}`}
                  onClick={() => setPaymentMethod('pix')}
                >
                  <i className="fas fa-qrcode"></i>
                  <span>PIX</span>
                </div>
              </div>
            </div>
            
            {paymentMethod === 'credit_card' && (
              <div className="credit-card-form">
                <div className="form-group">
                  <label htmlFor="cardNumber">Número do Cartão</label>
                  <input
                    type="text"
                    id="cardNumber"
                    value={cardNumber}
                    onChange={handleCardNumberChange}
                    placeholder="0000 0000 0000 0000"
                    maxLength="19"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="cardName">Nome no Cartão</label>
                  <input
                    type="text"
                    id="cardName"
                    value={cardName}
                    onChange={(e) => setCardName(e.target.value)}
                    placeholder="NOME COMO ESTÁ NO CARTÃO"
                    required
                  />
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="expiryDate">Validade</label>
                    <input
                      type="text"
                      id="expiryDate"
                      value={expiryDate}
                      onChange={handleExpiryDateChange}
                      placeholder="MM/AA"
                      maxLength="5"
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="cvv">CVV</label>
                    <input
                      type="text"
                      id="cvv"
                      value={cvv}
                      onChange={handleCvvChange}
                      placeholder="123"
                      maxLength="4"
                      required
                    />
                  </div>
                </div>
              </div>
            )}
            
            {paymentMethod === 'pix' && (
              <div className="pix-payment">
                <div className="pix-info">
                  <p>Ao confirmar, você receberá um QR Code PIX para pagamento.</p>
                  <p>Após o pagamento, sua assinatura será ativada automaticamente.</p>
                </div>
                <div className="pix-image">
                  <div className="pix-placeholder">
                    <i className="fas fa-qrcode"></i>
                    <span>QR Code PIX</span>
                  </div>
                </div>
              </div>
            )}
            
            <div className="payment-actions">
              <button 
                type="button" 
                className="cancel-button"
                onClick={onCancel}
                disabled={loading}
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                className="confirm-button"
                disabled={loading}
              >
                {loading ? 'Processando...' : 'Confirmar Pagamento'}
              </button>
            </div>
          </form>
        )}
        
        <div className="payment-footer">
          <p>Pagamento seguro <i className="fas fa-lock"></i></p>
          <p>Seus dados são protegidos e criptografados</p>
        </div>
      </div>
    </div>
  );
};

export default Payment;
