from supabase.client import create_client, Client
from typing import List, Dict, Any
from app.config import SUPABASE_URL, SUPABASE_KEY

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def get_cars(self, filters: Dict[str, Any], limit: int = 3, offset: int = 0) -> List[Dict]:
        query = self.client.table('cars').select('*')
        
        if filters.get('category'):
            query = query.eq('category', filters['category'])
            
        specs = filters.get('specs', {})
        if specs.get('driveType'):
            query = query.eq('specs->>driveType', specs['driveType'])
        if specs.get('fuelType'):
            query = query.eq('specs->>fuelType', specs['fuelType'])
            
        query = query.limit(limit).offset(offset)
        
        result = query.execute()
        return result.data