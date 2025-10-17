import pytest
from backend.models.character import Character

def test_character_creation():
    """Test basic character creation"""
    char = Character(
        name="Test Warrior",
        class_type="warrior",
        level=1
    )
    assert char.name == "Test Warrior"
    assert char.class_type == "warrior"
    assert char.level == 1

def test_character_stats():
    """Test character stat allocation"""
    char = Character(
        name="Test Character",
        class_type="warrior"
    )
    char.set_stat("STR", 16)
    char.set_stat("DEX", 12)
    
    assert char.get_stat("STR") == 16
    assert char.get_stat("DEX") == 12

def test_character_skill_learning():
    """Test skill learning functionality"""
    char = Character(
        name="Test Mage",
        class_type="mage"
    )
    char.learn_skill("fireball")
    
    assert "fireball" in char.skills
    assert char.can_use_skill("fireball")
