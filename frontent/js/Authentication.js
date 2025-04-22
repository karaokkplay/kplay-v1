import React, { useState, useEffect } from 'react';
import { GoogleLogin } from 'react-google-login';
import { FacebookLogin } from 'react-facebook-login';
import { DiscordLogin } from 'react-discord-login';
import './Authentication.css';

const Authentication = ({ onLogin, onRegister }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Configurações para autenticação com serviços externos
  const googleClientId = 'YOUR_GOOGLE_CLIENT_ID';
  const facebookAppId = 'YOUR_FACEBOOK_APP_ID';
  const discordClientId = 'YOUR_DISCORD_CLIENT_ID';

  // Limpar erros quando o usuário alterna entre login e registro
  useEffect(() => {
    setError('');
  }, [isLogin]);

  // Manipulador para login com email/senha
  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validação básica
      if (!email || !password) {
        throw new Error('Por favor, preencha todos os campos.');
      }

      // Em uma implementação real, você enviaria uma requisição para o backend
      // Simulação de login bem-sucedido após 1 segundo
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Chamar callback de login bem-sucedido
      if (onLogin) {
        onLogin({
          email,
          name: 'Usuário Demo',
          token: 'demo_token_123'
        });
      }
    } catch (err) {
      setError(err.message || 'Erro ao fazer login. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Manipulador para registro com email/senha
  const handleEmailRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validação básica
      if (!email || !password || !confirmPassword || !name) {
        throw new Error('Por favor, preencha todos os campos.');
      }

      if (password !== confirmPassword) {
        throw new Error('As senhas não coincidem.');
      }

      if (password.length < 6) {
        throw new Error('A senha deve ter pelo menos 6 caracteres.');
      }

      // Em uma implementação real, você enviaria uma requisição para o backend
      // Simulação de registro bem-sucedido após 1 segundo
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Chamar callback de registro bem-sucedido
      if (onRegister) {
        onRegister({
          email,
          name,
          token: 'demo_token_123'
        });
      }
    } catch (err) {
      setError(err.message || 'Erro ao registrar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Manipuladores para login com serviços externos
  const handleGoogleSuccess = (response) => {
    if (onLogin) {
      onLogin({
        email: response.profileObj.email,
        name: response.profileObj.name,
        token: response.tokenId,
        provider: 'google'
      });
    }
  };

  const handleGoogleFailure = (error) => {
    setError('Erro ao fazer login com Google. Tente novamente.');
    console.error('Google Login Error:', error);
  };

  const handleFacebookResponse = (response) => {
    if (response.status !== 'unknown') {
      if (onLogin) {
        onLogin({
          email: response.email,
          name: response.name,
          token: response.accessToken,
          provider: 'facebook'
        });
      }
    } else {
      setError('Erro ao fazer login com Facebook. Tente novamente.');
    }
  };

  const handleDiscordResponse = (response) => {
    if (response.code) {
      // Em uma implementação real, você enviaria este código para o backend
      // para trocar por um token de acesso
      if (onLogin) {
        onLogin({
          token: response.code,
          provider: 'discord'
        });
      }
    } else {
      setError('Erro ao fazer login com Discord. Tente novamente.');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>{isLogin ? 'Login' : 'Cadastro'}</h2>
          <div className="auth-toggle">
            <button 
              className={isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(true)}
            >
              Login
            </button>
            <button 
              className={!isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(false)}
            >
              Cadastro
            </button>
          </div>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={isLogin ? handleEmailLogin : handleEmailRegister}>
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="name">Nome</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Seu nome completo"
                required={!isLogin}
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Sua senha"
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmar Senha</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirme sua senha"
                required={!isLogin}
              />
            </div>
          )}

          <button 
            type="submit" 
            className="auth-button"
            disabled={loading}
          >
            {loading ? 'Processando...' : isLogin ? 'Entrar' : 'Cadastrar'}
          </button>
        </form>

        <div className="auth-divider">
          <span>ou</span>
        </div>

        <div className="social-login">
          <GoogleLogin
            clientId={googleClientId}
            buttonText="Continuar com Google"
            onSuccess={handleGoogleSuccess}
            onFailure={handleGoogleFailure}
            cookiePolicy={'single_host_origin'}
            className="google-button"
          />

          <FacebookLogin
            appId={facebookAppId}
            autoLoad={false}
            fields="name,email,picture"
            callback={handleFacebookResponse}
            cssClass="facebook-button"
            textButton="Continuar com Facebook"
          />

          <DiscordLogin
            clientId={discordClientId}
            redirectUri={window.location.origin}
            onSuccess={handleDiscordResponse}
            onFailure={() => setError('Erro ao fazer login com Discord')}
            className="discord-button"
            buttonText="Continuar com Discord"
          />
        </div>

        {isLogin && (
          <div className="auth-footer">
            <a href="#reset-password">Esqueceu sua senha?</a>
          </div>
        )}
      </div>
    </div>
  );
};

export default Authentication;
