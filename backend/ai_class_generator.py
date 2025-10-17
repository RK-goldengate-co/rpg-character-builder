"""AI Class Generator Module for RPG Character Builder

This module uses AI to generate character classes, skills, and abilities
based on player preferences and game balance algorithms.
"""

import random
import json

class AIClassGenerator:
    def __init__(self):
        self.base_stats = {
            'warrior': {'STR': 16, 'DEX': 12, 'INT': 8, 'WIS': 10, 'CON': 14, 'CHA': 10},
            'mage': {'STR': 8, 'DEX': 10, 'INT': 16, 'WIS': 14, 'CON': 10, 'CHA': 12},
            'rogue': {'STR': 10, 'DEX': 16, 'INT': 12, 'WIS': 10, 'CON': 10, 'CHA': 12},
            'cleric': {'STR': 12, 'DEX': 10, 'INT': 10, 'WIS': 16, 'CON': 12, 'CHA': 14}
        }
        
    def generate_class(self, preferences):
        """Generate a custom class based on player preferences"""
        playstyle = preferences.get('playstyle', 'balanced')
        theme = preferences.get('theme', 'fantasy')
        
        class_data = {
            'name': self._generate_name(playstyle, theme),
            'stats': self._generate_stats(playstyle),
            'skills': self._generate_skills(playstyle),
            'description': self._generate_description(playstyle, theme)
        }
        
        return class_data
    
    def _generate_name(self, playstyle, theme):
        """Generate a unique class name"""
        prefixes = {
            'aggressive': ['Battle', 'War', 'Death'],
            'defensive': ['Guardian', 'Sentinel', 'Protector'],
            'magical': ['Arcane', 'Mystic', 'Elemental'],
            'balanced': ['Adventurer', 'Explorer', 'Hero']
        }
        
        suffixes = {
            'fantasy': ['Knight', 'Mage', 'Ranger'],
            'scifi': ['Operative', 'Commander', 'Specialist'],
            'modern': ['Agent', 'Fighter', 'Expert']
        }
        
        prefix = random.choice(prefixes.get(playstyle, prefixes['balanced']))
        suffix = random.choice(suffixes.get(theme, suffixes['fantasy']))
        
        return f"{prefix} {suffix}"
    
    def _generate_stats(self, playstyle):
        """Generate stat distribution based on playstyle"""
        base = self.base_stats.get('warrior', {})
        
        if playstyle == 'aggressive':
            return {'STR': 18, 'DEX': 14, 'INT': 8, 'WIS': 8, 'CON': 12, 'CHA': 10}
        elif playstyle == 'defensive':
            return {'STR': 14, 'DEX': 10, 'INT': 10, 'WIS': 12, 'CON': 18, 'CHA': 10}
        elif playstyle == 'magical':
            return {'STR': 8, 'DEX': 12, 'INT': 18, 'WIS': 14, 'CON': 10, 'CHA': 12}
        else:
            return {'STR': 12, 'DEX': 12, 'INT': 12, 'WIS': 12, 'CON': 12, 'CHA': 12}
    
    def _generate_skills(self, playstyle):
        """Generate appropriate skill set"""
        skill_pools = {
            'aggressive': ['Power Strike', 'Berserk', 'Critical Hit'],
            'defensive': ['Shield Wall', 'Fortify', 'Last Stand'],
            'magical': ['Fireball', 'Ice Shard', 'Lightning Bolt'],
            'balanced': ['Quick Attack', 'Dodge', 'Focus']
        }
        
        return skill_pools.get(playstyle, skill_pools['balanced'])
    
    def _generate_description(self, playstyle, theme):
        """Generate class description"""
        return f"A {playstyle} {theme} class with unique abilities and balanced stats."
    
    def export_class(self, class_data, filename):
        """Export generated class to JSON file"""
        with open(filename, 'w') as f:
            json.dump(class_data, f, indent=2)
        return True
