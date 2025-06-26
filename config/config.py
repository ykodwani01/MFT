import yaml 
from dotenv import load_dotenv
import os

class Config:
    def __init__(self, config_path=None):
        load_dotenv()
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "service.yaml")
        self.config_path = config_path
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key not found. Please set ALPHA_VANTAGE_API_KEY in your environment variables.")
        
        self.load_config()
        
    def load_config(self):
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def get_stocks(self):
        return self.config.get('stocks', [])
    