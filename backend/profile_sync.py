"""Profile Sync Module for RPG Character Builder

This module handles synchronization of character profiles between
online (cloud) and offline (local) storage with conflict resolution.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class ProfileSync:
    def __init__(self, local_dir='data/profiles', cloud_url=None):
        self.local_dir = local_dir
        self.cloud_url = cloud_url
        self.sync_log = []
        
        # Create local directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
    
    def get_profile_hash(self, profile_data: Dict) -> str:
        """Calculate hash of profile data for change detection"""
        profile_str = json.dumps(profile_data, sort_keys=True)
        return hashlib.sha256(profile_str.encode()).hexdigest()
    
    def load_local_profile(self, profile_id: str) -> Optional[Dict]:
        """Load profile from local storage"""
        file_path = os.path.join(self.local_dir, f"{profile_id}.json")
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    profile = json.load(f)
                    return profile
        except Exception as e:
            self.log_sync(f"Error loading local profile {profile_id}: {str(e)}", 'error')
        
        return None
    
    def save_local_profile(self, profile_id: str, profile_data: Dict) -> bool:
        """Save profile to local storage"""
        file_path = os.path.join(self.local_dir, f"{profile_id}.json")
        
        try:
            # Add sync metadata
            profile_data['last_sync'] = datetime.now().isoformat()
            profile_data['sync_hash'] = self.get_profile_hash(profile_data)
            
            with open(file_path, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            self.log_sync(f"Saved local profile {profile_id}", 'success')
            return True
        except Exception as e:
            self.log_sync(f"Error saving local profile {profile_id}: {str(e)}", 'error')
            return False
    
    def fetch_cloud_profile(self, profile_id: str) -> Optional[Dict]:
        """Fetch profile from cloud storage"""
        if not self.cloud_url:
            return None
        
        try:
            # Simulate cloud API call
            # In production, this would make HTTP request to cloud_url
            cloud_file = os.path.join(self.local_dir, f"cloud_{profile_id}.json")
            
            if os.path.exists(cloud_file):
                with open(cloud_file, 'r') as f:
                    profile = json.load(f)
                    self.log_sync(f"Fetched cloud profile {profile_id}", 'success')
                    return profile
        except Exception as e:
            self.log_sync(f"Error fetching cloud profile {profile_id}: {str(e)}", 'error')
        
        return None
    
    def push_cloud_profile(self, profile_id: str, profile_data: Dict) -> bool:
        """Push profile to cloud storage"""
        if not self.cloud_url:
            return False
        
        try:
            # Simulate cloud API call
            # In production, this would make HTTP request to cloud_url
            cloud_file = os.path.join(self.local_dir, f"cloud_{profile_id}.json")
            
            profile_data['last_cloud_sync'] = datetime.now().isoformat()
            
            with open(cloud_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            self.log_sync(f"Pushed cloud profile {profile_id}", 'success')
            return True
        except Exception as e:
            self.log_sync(f"Error pushing cloud profile {profile_id}: {str(e)}", 'error')
            return False
    
    def resolve_conflict(self, local_profile: Dict, cloud_profile: Dict, 
                        strategy: str = 'newest') -> Dict:
        """Resolve conflicts between local and cloud profiles"""
        if strategy == 'newest':
            # Use the profile with the most recent modification
            local_time = local_profile.get('last_sync', '1970-01-01T00:00:00')
            cloud_time = cloud_profile.get('last_cloud_sync', '1970-01-01T00:00:00')
            
            winner = local_profile if local_time > cloud_time else cloud_profile
            self.log_sync(f"Conflict resolved using newest ({strategy})", 'info')
            return winner
        
        elif strategy == 'local':
            # Always prefer local version
            self.log_sync("Conflict resolved using local version", 'info')
            return local_profile
        
        elif strategy == 'cloud':
            # Always prefer cloud version
            self.log_sync("Conflict resolved using cloud version", 'info')
            return cloud_profile
        
        elif strategy == 'merge':
            # Merge both profiles (prefer cloud for conflicts)
            merged = {**local_profile, **cloud_profile}
            self.log_sync("Conflict resolved using merge strategy", 'info')
            return merged
        
        return local_profile
    
    def sync_profile(self, profile_id: str, strategy: str = 'newest') -> Dict:
        """Synchronize profile between local and cloud storage"""
        local_profile = self.load_local_profile(profile_id)
        cloud_profile = self.fetch_cloud_profile(profile_id)
        
        # Case 1: Only local exists
        if local_profile and not cloud_profile:
            self.push_cloud_profile(profile_id, local_profile)
            return {
                'status': 'synced',
                'action': 'uploaded_to_cloud',
                'profile': local_profile
            }
        
        # Case 2: Only cloud exists
        if cloud_profile and not local_profile:
            self.save_local_profile(profile_id, cloud_profile)
            return {
                'status': 'synced',
                'action': 'downloaded_from_cloud',
                'profile': cloud_profile
            }
        
        # Case 3: Both exist - check for conflicts
        if local_profile and cloud_profile:
            local_hash = self.get_profile_hash(local_profile)
            cloud_hash = self.get_profile_hash(cloud_profile)
            
            if local_hash == cloud_hash:
                return {
                    'status': 'synced',
                    'action': 'already_synced',
                    'profile': local_profile
                }
            else:
                # Conflict detected - resolve it
                resolved = self.resolve_conflict(local_profile, cloud_profile, strategy)
                self.save_local_profile(profile_id, resolved)
                self.push_cloud_profile(profile_id, resolved)
                
                return {
                    'status': 'synced',
                    'action': 'conflict_resolved',
                    'profile': resolved,
                    'strategy': strategy
                }
        
        # Case 4: Neither exists
        return {
            'status': 'error',
            'action': 'profile_not_found',
            'profile': None
        }
    
    def sync_all_profiles(self, strategy: str = 'newest') -> List[Dict]:
        """Sync all local profiles with cloud"""
        results = []
        
        # Get all local profile IDs
        local_files = [f.replace('.json', '') for f in os.listdir(self.local_dir) 
                      if f.endswith('.json') and not f.startswith('cloud_')]
        
        for profile_id in local_files:
            result = self.sync_profile(profile_id, strategy)
            results.append(result)
        
        self.log_sync(f"Synced {len(results)} profiles", 'info')
        return results
    
    def log_sync(self, message: str, level: str = 'info'):
        """Log sync operations"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.sync_log.append(log_entry)
        
        # Keep only last 100 log entries
        if len(self.sync_log) > 100:
            self.sync_log = self.sync_log[-100:]
    
    def get_sync_log(self, limit: int = 20) -> List[Dict]:
        """Get recent sync log entries"""
        return self.sync_log[-limit:]
