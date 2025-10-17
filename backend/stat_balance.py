"""Stat Balance Module for RPG Character Builder

This module provides algorithms to balance character statistics,
ensure fair gameplay, and optimize stat distributions.
"""

import math
from typing import Dict, List, Tuple

class StatBalancer:
    def __init__(self):
        self.total_points = 70
        self.min_stat = 3
        self.max_stat = 18
        self.stat_names = ['STR', 'DEX', 'INT', 'WIS', 'CON', 'CHA']
        
        # Balance weights for different roles
        self.role_weights = {
            'warrior': {'STR': 2.0, 'DEX': 1.2, 'INT': 0.8, 'WIS': 1.0, 'CON': 1.8, 'CHA': 1.0},
            'mage': {'STR': 0.8, 'DEX': 1.0, 'INT': 2.0, 'WIS': 1.5, 'CON': 1.0, 'CHA': 1.2},
            'rogue': {'STR': 1.0, 'DEX': 2.0, 'INT': 1.2, 'WIS': 1.0, 'CON': 1.0, 'CHA': 1.2},
            'cleric': {'STR': 1.2, 'DEX': 1.0, 'INT': 1.0, 'WIS': 2.0, 'CON': 1.2, 'CHA': 1.5}
        }
    
    def validate_stats(self, stats: Dict[str, int]) -> Tuple[bool, str]:
        """Validate if stat distribution is legal"""
        # Check all stats are present
        for stat_name in self.stat_names:
            if stat_name not in stats:
                return False, f"Missing stat: {stat_name}"
        
        # Check stat ranges
        for stat_name, value in stats.items():
            if value < self.min_stat or value > self.max_stat:
                return False, f"{stat_name} must be between {self.min_stat} and {self.max_stat}"
        
        # Check total points
        total = sum(stats.values())
        if total != self.total_points:
            return False, f"Total points must be {self.total_points}, got {total}"
        
        return True, "Valid stats"
    
    def calculate_power_level(self, stats: Dict[str, int], role: str = None) -> float:
        """Calculate overall power level of stat distribution"""
        if role and role in self.role_weights:
            weights = self.role_weights[role]
            power = sum(stats[stat] * weights[stat] for stat in self.stat_names)
        else:
            power = sum(stats.values())
        
        return round(power, 2)
    
    def suggest_stats(self, role: str, playstyle: str = 'balanced') -> Dict[str, int]:
        """Suggest optimal stat distribution for a role"""
        if role not in self.role_weights:
            role = 'warrior'
        
        weights = self.role_weights[role]
        total_weight = sum(weights.values())
        
        # Calculate base allocation
        stats = {}
        points_left = self.total_points
        
        for stat_name in self.stat_names:
            proportion = weights[stat_name] / total_weight
            allocated = int(self.total_points * proportion)
            
            # Apply playstyle modifier
            if playstyle == 'aggressive':
                if stat_name in ['STR', 'DEX']:
                    allocated += 2
                elif stat_name in ['INT', 'WIS']:
                    allocated -= 1
            elif playstyle == 'defensive':
                if stat_name == 'CON':
                    allocated += 3
                elif stat_name in ['STR', 'DEX']:
                    allocated -= 1
            
            # Ensure within bounds
            allocated = max(self.min_stat, min(self.max_stat, allocated))
            stats[stat_name] = allocated
            points_left -= allocated
        
        # Distribute remaining points
        while points_left > 0:
            for stat_name in sorted(self.stat_names, key=lambda s: weights[s], reverse=True):
                if stats[stat_name] < self.max_stat and points_left > 0:
                    stats[stat_name] += 1
                    points_left -= 1
                    if points_left <= 0:
                        break
        
        # Remove excess points if over
        while points_left < 0:
            for stat_name in sorted(self.stat_names, key=lambda s: weights[s]):
                if stats[stat_name] > self.min_stat and points_left < 0:
                    stats[stat_name] -= 1
                    points_left += 1
                    if points_left >= 0:
                        break
        
        return stats
    
    def optimize_stats(self, current_stats: Dict[str, int], role: str) -> Dict[str, int]:
        """Optimize existing stat distribution for better balance"""
        suggested = self.suggest_stats(role)
        
        # Calculate difference
        optimized = current_stats.copy()
        total_current = sum(current_stats.values())
        
        if total_current == self.total_points:
            # Stats are already valid, make minor adjustments
            for stat_name in self.stat_names:
                diff = suggested[stat_name] - current_stats[stat_name]
                adjustment = int(diff * 0.3)  # 30% adjustment towards optimal
                new_value = current_stats[stat_name] + adjustment
                optimized[stat_name] = max(self.min_stat, min(self.max_stat, new_value))
            
            # Rebalance to exact total
            total = sum(optimized.values())
            if total != self.total_points:
                diff = self.total_points - total
                # Adjust the most flexible stat
                for stat_name in self.stat_names:
                    if diff > 0 and optimized[stat_name] < self.max_stat:
                        optimized[stat_name] += diff
                        break
                    elif diff < 0 and optimized[stat_name] > self.min_stat:
                        optimized[stat_name] += diff
                        break
        
        return optimized
    
    def compare_builds(self, stats1: Dict[str, int], stats2: Dict[str, int], role: str) -> Dict:
        """Compare two stat distributions"""
        power1 = self.calculate_power_level(stats1, role)
        power2 = self.calculate_power_level(stats2, role)
        
        return {
            'build1_power': power1,
            'build2_power': power2,
            'difference': round(abs(power1 - power2), 2),
            'winner': 'build1' if power1 > power2 else 'build2' if power2 > power1 else 'tie',
            'advantage_percent': round(abs(power1 - power2) / max(power1, power2) * 100, 2)
        }
