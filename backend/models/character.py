from datetime import datetime
from typing import Dict, List, Optional

class Character:
    """RPG Character Model"""
    
    def __init__(self, name: str, class_type: str, level: int = 1):
        self.name = name
        self.class_type = class_type
        self.level = level
        self.stats = {
            'STR': 10,
            'DEX': 10,
            'INT': 10,
            'WIS': 10,
            'CON': 10,
            'CHA': 10
        }
        self.skills = []
        self.equipment = {}
        self.appearance = {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def set_stat(self, stat_name: str, value: int):
        """Set character stat value"""
        if stat_name in self.stats:
            self.stats[stat_name] = value
            self.updated_at = datetime.utcnow()
    
    def get_stat(self, stat_name: str) -> int:
        """Get character stat value"""
        return self.stats.get(stat_name, 0)
    
    def learn_skill(self, skill_id: str):
        """Add skill to character"""
        if skill_id not in self.skills:
            self.skills.append(skill_id)
            self.updated_at = datetime.utcnow()
    
    def can_use_skill(self, skill_id: str) -> bool:
        """Check if character has learned skill"""
        return skill_id in self.skills
    
    def to_dict(self) -> Dict:
        """Export character to dictionary"""
        return {
            'name': self.name,
            'class': self.class_type,
            'level': self.level,
            'stats': self.stats,
            'skills': self.skills,
            'equipment': self.equipment,
            'appearance': self.appearance,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
