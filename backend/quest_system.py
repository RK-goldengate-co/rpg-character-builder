"""Quest System Module for RPG Character Builder

This module provides a comprehensive quest management system including
quest tracking, objectives, rewards, and progression.
"""

class Quest:
    def __init__(self, quest_id, name, description, objectives, rewards):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.status = 'not_started'
        self.progress = {}
    
    def start_quest(self):
        """Initialize quest and mark as active"""
        self.status = 'active'
        return True
    
    def update_objective(self, objective_id, value):
        """Update progress on a specific objective"""
        self.progress[objective_id] = value
        return self.check_completion()
    
    def check_completion(self):
        """Check if all objectives are completed"""
        for obj in self.objectives:
            if self.progress.get(obj['id'], 0) < obj['required']:
                return False
        self.status = 'completed'
        return True

class QuestManager:
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
    
    def add_quest(self, quest):
        """Add a new quest to the active list"""
        quest.start_quest()
        self.active_quests.append(quest)
    
    def complete_quest(self, quest_id):
        """Mark quest as completed and move to completed list"""
        for quest in self.active_quests:
            if quest.quest_id == quest_id:
                self.completed_quests.append(quest)
                self.active_quests.remove(quest)
                return quest.rewards
        return None
