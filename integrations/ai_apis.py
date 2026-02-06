"""
AI API Manager - Toggle OpenAI/Claude/Gemini for document analysis
Users provide their own API keys
"""

import json
import os
from typing import Dict, Optional


class AIAPIManager:
    """Manage external AI API integrations"""
    
    SUPPORTED_PROVIDERS = {
        'openai': {
            'name': 'OpenAI (GPT)',
            'models': ['gpt-4', 'gpt-3.5-turbo'],
            'default_model': 'gpt-3.5-turbo'
        },
        'anthropic': {
            'name': 'Anthropic (Claude)',
            'models': ['claude-3-sonnet', 'claude-2'],
            'default_model': 'claude-3-sonnet'
        },
        'google': {
            'name': 'Google (Gemini)',
            'models': ['gemini-pro', 'gemini-1.5-pro'],
            'default_model': 'gemini-pro'
        }
    }
    
    def __init__(self, config_file='ai_config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load API configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'enabled': False, 'provider': None, 'api_key': None}
    
    def _save_config(self):
        """Save API configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_api_key(self, provider: str, api_key: str, model: str = None) -> bool:
        """
        Set API key for a provider
        Returns: True if successful
        """
        if provider not in self.SUPPORTED_PROVIDERS:
            return False
        
        self.config['provider'] = provider
        self.config['api_key'] = api_key
        self.config['model'] = model or self.SUPPORTED_PROVIDERS[provider]['default_model']
        self.config['enabled'] = True
        
        self._save_config()
        return True
    
    def remove_api_key(self):
        """Disable AI integration"""
        self.config = {'enabled': False, 'provider': None, 'api_key': None}
        self._save_config()
    
    def is_enabled(self) -> bool:
        """Check if AI integration is enabled"""
        return self.config.get('enabled', False) and self.config.get('api_key') is not None
    
    def analyze_document(self, document_text: str, prompt: str = None) -> Dict:
        """
        Analyze document using configured AI
        Returns: {'success': bool, 'result': str, 'error': str}
        """
        if not self.is_enabled():
            return {'success': False, 'error': 'AI integration not enabled'}
        
        provider = self.config.get('provider')
        api_key = self.config.get('api_key')
        model = self.config.get('model')
        
        default_prompt = prompt or "Extract key information from this document: invoice number, vendor, amount, date."
        
        try:
            if provider == 'openai':
                result = self._call_openai(document_text, default_prompt, api_key, model)
            elif provider == 'anthropic':
                result = self._call_anthropic(document_text, default_prompt, api_key, model)
            elif provider == 'google':
                result = self._call_google(document_text, default_prompt, api_key, model)
            else:
                return {'success': False, 'error': 'Unknown provider'}
            
            return {'success': True, 'result': result, 'provider': provider}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _call_openai(self, text: str, prompt: str, api_key: str, model: str) -> str:
        """Call OpenAI API (requires openai library)"""
        try:
            import openai
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a document analysis assistant."},
                    {"role": "user", "content": f"{prompt}\n\nDocument:\n{text}"}
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "OpenAI library not installed. Install: pip install openai"
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _call_anthropic(self, text: str, prompt: str, api_key: str, model: str) -> str:
        """Call Anthropic API (requires anthropic library)"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model=model,
                max_tokens=500,
                messages=[
                    {"role": "user", "content": f"{prompt}\n\nDocument:\n{text}"}
                ]
            )
            
            return response.content[0].text
            
        except ImportError:
            return "Anthropic library not installed. Install: pip install anthropic"
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def _call_google(self, text: str, prompt: str, api_key: str, model: str) -> str:
        """Call Google Gemini API"""
        try:
            import requests
            
            url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{prompt}\n\nDocument:\n{text}"
                    }]
                }]
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
            
        except ImportError:
            return "requests library not installed"
        except Exception as e:
            raise Exception(f"Google API error: {str(e)}")
    
    def get_providers(self) -> Dict:
        """Get list of supported providers"""
        return self.SUPPORTED_PROVIDERS
    
    def get_current_config(self) -> Dict:
        """Get current configuration (without exposing full API key)"""
        config = self.config.copy()
        if config.get('api_key'):
            # Mask API key
            key = config['api_key']
            config['api_key_masked'] = key[:8] + '...' + key[-4:] if len(key) > 12 else '***'
            del config['api_key']
        return config
    
    def test_connection(self) -> Dict:
        """Test if API connection works"""
        if not self.is_enabled():
            return {'success': False, 'error': 'Not configured'}
        
        test_result = self.analyze_document(
            "Test document: Invoice #123, Amount: $100",
            "Extract the invoice number and amount."
        )
        
        return test_result


class AIUsageTracker:
    """Track AI API usage and costs"""
    
    def __init__(self, log_file='ai_usage.json'):
        self.log_file = log_file
        self.usage_log = self._load_log()
    
    def _load_log(self) -> list:
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_log(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.usage_log, f, indent=2)
    
    def log_usage(self, provider: str, model: str, tokens_used: int = 0):
        """Log API usage"""
        entry = {
            'timestamp': str(pd.Timestamp.now()),
            'provider': provider,
            'model': model,
            'tokens': tokens_used
        }
        
        self.usage_log.append(entry)
        self._save_log()
    
    def get_usage_summary(self) -> Dict:
        """Get usage summary"""
        if not self.usage_log:
            return {'total_calls': 0}
        
        total_calls = len(self.usage_log)
        by_provider = {}
        
        for entry in self.usage_log:
            provider = entry['provider']
            by_provider[provider] = by_provider.get(provider, 0) + 1
        
        return {
            'total_calls': total_calls,
            'by_provider': by_provider
        }
