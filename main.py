import pygame
import sys
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (25, 25, 112)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
LIME = (50, 205, 50)
PINK = (255, 192, 203)
NAVY = (0, 0, 128)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_RED = (139, 0, 0)
TEAL = (0, 128, 128)

class ItemType(Enum):
    WOOD = 1
    STONE = 2
    FIBER = 3
    MEAT = 4
    BERRIES = 5
    METAL = 6

class DinosaurType(Enum):
    # Original
    TRIKE = 1
    RAPTOR = 2
    REX = 3
    STEGO = 4
    BRONTO = 5
    
    # Additional Dinosaurs
    SABERTOOTH = 6
    TRICERATOPS = 7
    PARASAUROLOPHUS = 8
    GALLIMIMUS = 9
    ANKYLOSAURUS = 10
    BRACHIOSAURUS = 11
    CARNOTAURUS = 12
    DILOPHOSAURUS = 13
    DIMORPHODON = 14
    DODO = 15
    GRIFFIN = 16
    IGUANODON = 17
    MANTIS = 18
    MOSCHOPS = 19
    MOSASAURUS = 20
    OVIRAPTOR = 21
    PACHY = 22
    PHIOMIA = 23
    PHOENIX = 24
    PLESIOSAUR = 25
    PTERANODON = 26
    QUETZALCOATLUS = 27
    REAPER = 28
    SPINOSAURUS = 29
    THERIZINOSAUR = 30
    TITANBOA = 31
    TRILOBITE = 32
    TUSOTEUTHIS = 33
    WYVERN = 34
    ALLOSAURUS = 35
    BASILISK = 36
    COMPY = 37
    CORRUPTED_DINO = 38
    CRYPTID = 39
    GIGA = 40

@dataclass
class Item:
    item_type: ItemType
    quantity: int

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.health = 100
        self.hunger = 100
        self.stamina = 100
        self.speed = 5
        self.inventory: List[Item] = []
        self.max_inventory = 30
        self.current_inventory_weight = 0
        self.level = 1
        self.experience = 0

    def handle_input(self, keys):
        dx, dy = 0, 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        
        # Clamp movement
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x + dx))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y + dy))
        
        # Update stamina
        if dx != 0 or dy != 0:
            self.stamina = max(0, self.stamina - 0.5)
        else:
            self.stamina = min(100, self.stamina + 0.3)
    
    def update(self):
        self.hunger = max(0, self.hunger - 0.05)
        self.health = min(100, self.health + 0.01)  # Slow natural regeneration
        
        if self.hunger < 20:
            self.health = max(0, self.health - 0.2)
    
    def add_item(self, item_type: ItemType, quantity: int = 1):
        for item in self.inventory:
            if item.item_type == item_type:
                item.quantity += quantity
                return
        
        if len(self.inventory) < self.max_inventory:
            self.inventory.append(Item(item_type, quantity))
    
    def draw(self, surface):
        pygame.draw.rect(surface, (100, 149, 237), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, YELLOW, (self.x + self.width // 2, self.y - 5), 5)  # Head
    
    def draw_stats(self, surface, font):
        stats_text = [
            f"Health: {int(self.health)}/100",
            f"Hunger: {int(self.hunger)}/100",
            f"Stamina: {int(self.stamina)}/100",
            f"Level: {self.level}",
            f"XP: {self.experience}"
        ]
        
        for i, text in enumerate(stats_text):
            surf = font.render(text, True, WHITE)
            surface.blit(surf, (10, 10 + i * 25))

class Dinosaur:
    def __init__(self, x: float, y: float, dino_type: DinosaurType):
        self.x = x
        self.y = y
        self.dino_type = dino_type
        self.width = self.get_width()
        self.height = self.get_height()
        self.health = self.get_max_health()
        self.max_health = self.get_max_health()
        self.speed = self.get_speed()
        self.damage = self.get_damage()
        self.aggression = self.get_aggression()
        self.direction = random.uniform(0, 2 * math.pi)
        self.wander_timer = random.randint(60, 300)
        self.target_player = None
        self.attack_cooldown = 0
    
    def get_width(self):
        sizes = {
            DinosaurType.TRIKE: 50,
            DinosaurType.RAPTOR: 40,
            DinosaurType.REX: 80,
            DinosaurType.STEGO: 60,
            DinosaurType.BRONTO: 100,
            DinosaurType.SABERTOOTH: 55,
            DinosaurType.TRICERATOPS: 65,
            DinosaurType.PARASAUROLOPHUS: 45,
            DinosaurType.GALLIMIMUS: 35,
            DinosaurType.ANKYLOSAURUS: 70,
            DinosaurType.BRACHIOSAURUS: 110,
            DinosaurType.CARNOTAURUS: 75,
            DinosaurType.DILOPHOSAURUS: 50,
            DinosaurType.DIMORPHODON: 25,
            DinosaurType.DODO: 15,
            DinosaurType.GRIFFIN: 90,
            DinosaurType.IGUANODON: 55,
            DinosaurType.MANTIS: 30,
            DinosaurType.MOSCHOPS: 60,
            DinosaurType.MOSASAURUS: 120,
            DinosaurType.OVIRAPTOR: 40,
            DinosaurType.PACHY: 35,
            DinosaurType.PHIOMIA: 45,
            DinosaurType.PHOENIX: 85,
            DinosaurType.PLESIOSAUR: 95,
            DinosaurType.PTERANODON: 50,
            DinosaurType.QUETZALCOATLUS: 100,
            DinosaurType.REAPER: 85,
            DinosaurType.SPINOSAURUS: 95,
            DinosaurType.THERIZINOSAUR: 75,
            DinosaurType.TITANBOA: 40,
            DinosaurType.TRILOBITE: 20,
            DinosaurType.TUSOTEUTHIS: 105,
            DinosaurType.WYVERN: 80,
            DinosaurType.ALLOSAURUS: 70,
            DinosaurType.BASILISK: 65,
            DinosaurType.COMPY: 20,
            DinosaurType.CORRUPTED_DINO: 90,
            DinosaurType.CRYPTID: 75,
            DinosaurType.GIGA: 120,
        }
        return sizes.get(self.dino_type, 50)
    
    def get_height(self):
        sizes = {
            DinosaurType.TRIKE: 35,
            DinosaurType.RAPTOR: 30,
            DinosaurType.REX: 50,
            DinosaurType.STEGO: 45,
            DinosaurType.BRONTO: 50,
            DinosaurType.SABERTOOTH: 40,
            DinosaurType.TRICERATOPS: 40,
            DinosaurType.PARASAUROLOPHUS: 38,
            DinosaurType.GALLIMIMUS: 25,
            DinosaurType.ANKYLOSAURUS: 35,
            DinosaurType.BRACHIOSAURUS: 70,
            DinosaurType.CARNOTAURUS: 45,
            DinosaurType.DILOPHOSAURUS: 40,
            DinosaurType.DIMORPHODON: 20,
            DinosaurType.DODO: 12,
            DinosaurType.GRIFFIN: 50,
            DinosaurType.IGUANODON: 42,
            DinosaurType.MANTIS: 28,
            DinosaurType.MOSCHOPS: 45,
            DinosaurType.MOSASAURUS: 70,
            DinosaurType.OVIRAPTOR: 35,
            DinosaurType.PACHY: 28,
            DinosaurType.PHIOMIA: 35,
            DinosaurType.PHOENIX: 55,
            DinosaurType.PLESIOSAUR: 50,
            DinosaurType.PTERANODON: 35,
            DinosaurType.QUETZALCOATLUS: 60,
            DinosaurType.REAPER: 55,
            DinosaurType.SPINOSAURUS: 60,
            DinosaurType.THERIZINOSAUR: 50,
            DinosaurType.TITANBOA: 30,
            DinosaurType.TRILOBITE: 15,
            DinosaurType.TUSOTEUTHIS: 60,
            DinosaurType.WYVERN: 45,
            DinosaurType.ALLOSAURUS: 45,
            DinosaurType.BASILISK: 40,
            DinosaurType.COMPY: 15,
            DinosaurType.CORRUPTED_DINO: 55,
            DinosaurType.CRYPTID: 45,
            DinosaurType.GIGA: 70,
        }
        return sizes.get(self.dino_type, 40)
    
    def get_max_health(self):
        health = {
            DinosaurType.TRIKE: 80,
            DinosaurType.RAPTOR: 50,
            DinosaurType.REX: 150,
            DinosaurType.STEGO: 120,
            DinosaurType.BRONTO: 200,
            DinosaurType.SABERTOOTH: 140,
            DinosaurType.TRICERATOPS: 100,
            DinosaurType.PARASAUROLOPHUS: 75,
            DinosaurType.GALLIMIMUS: 40,
            DinosaurType.ANKYLOSAURUS: 200,
            DinosaurType.BRACHIOSAURUS: 300,
            DinosaurType.CARNOTAURUS: 160,
            DinosaurType.DILOPHOSAURUS: 90,
            DinosaurType.DIMORPHODON: 30,
            DinosaurType.DODO: 20,
            DinosaurType.GRIFFIN: 180,
            DinosaurType.IGUANODON: 85,
            DinosaurType.MANTIS: 60,
            DinosaurType.MOSCHOPS: 110,
            DinosaurType.MOSASAURUS: 250,
            DinosaurType.OVIRAPTOR: 65,
            DinosaurType.PACHY: 60,
            DinosaurType.PHIOMIA: 70,
            DinosaurType.PHOENIX: 220,
            DinosaurType.PLESIOSAUR: 180,
            DinosaurType.PTERANODON: 70,
            DinosaurType.QUETZALCOATLUS: 240,
            DinosaurType.REAPER: 190,
            DinosaurType.SPINOSAURUS: 200,
            DinosaurType.THERIZINOSAUR: 170,
            DinosaurType.TITANBOA: 120,
            DinosaurType.TRILOBITE: 25,
            DinosaurType.TUSOTEUTHIS: 260,
            DinosaurType.WYVERN: 210,
            DinosaurType.ALLOSAURUS: 130,
            DinosaurType.BASILISK: 150,
            DinosaurType.COMPY: 15,
            DinosaurType.CORRUPTED_DINO: 280,
            DinosaurType.CRYPTID: 160,
            DinosaurType.GIGA: 350,
        }
        return health.get(self.dino_type, 100)
    
    def get_speed(self):
        speeds = {
            DinosaurType.TRIKE: 2,
            DinosaurType.RAPTOR: 4,
            DinosaurType.REX: 3,
            DinosaurType.STEGO: 1.5,
            DinosaurType.BRONTO: 1,
            DinosaurType.SABERTOOTH: 3.5,
            DinosaurType.TRICERATOPS: 2.5,
            DinosaurType.PARASAUROLOPHUS: 3,
            DinosaurType.GALLIMIMUS: 4.5,
            DinosaurType.ANKYLOSAURUS: 1.2,
            DinosaurType.BRACHIOSAURUS: 0.8,
            DinosaurType.CARNOTAURUS: 3.2,
            DinosaurType.DILOPHOSAURUS: 2.8,
            DinosaurType.DIMORPHODON: 3,
            DinosaurType.DODO: 1,
            DinosaurType.GRIFFIN: 3.8,
            DinosaurType.IGUANODON: 2.5,
            DinosaurType.MANTIS: 3.5,
            DinosaurType.MOSCHOPS: 2.2,
            DinosaurType.MOSASAURUS: 2.5,
            DinosaurType.OVIRAPTOR: 3.2,
            DinosaurType.PACHY: 2.5,
            DinosaurType.PHIOMIA: 2,
            DinosaurType.PHOENIX: 4,
            DinosaurType.PLESIOSAUR: 2.2,
            DinosaurType.PTERANODON: 3.5,
            DinosaurType.QUETZALCOATLUS: 3.8,
            DinosaurType.REAPER: 3.3,
            DinosaurType.SPINOSAURUS: 2.8,
            DinosaurType.THERIZINOSAUR: 2.5,
            DinosaurType.TITANBOA: 2,
            DinosaurType.TRILOBITE: 1.5,
            DinosaurType.TUSOTEUTHIS: 2,
            DinosaurType.WYVERN: 3.6,
            DinosaurType.ALLOSAURUS: 3,
            DinosaurType.BASILISK: 3.2,
            DinosaurType.COMPY: 2,
            DinosaurType.CORRUPTED_DINO: 2.8,
            DinosaurType.CRYPTID: 2.5,
            DinosaurType.GIGA: 2.2,
        }
        return speeds.get(self.dino_type, 2)
    
    def get_damage(self):
        damages = {
            DinosaurType.TRIKE: 15,
            DinosaurType.RAPTOR: 20,
            DinosaurType.REX: 40,
            DinosaurType.STEGO: 25,
            DinosaurType.BRONTO: 10,
            DinosaurType.SABERTOOTH: 35,
            DinosaurType.TRICERATOPS: 28,
            DinosaurType.PARASAUROLOPHUS: 18,
            DinosaurType.GALLIMIMUS: 12,
            DinosaurType.ANKYLOSAURUS: 20,
            DinosaurType.BRACHIOSAURUS: 8,
            DinosaurType.CARNOTAURUS: 38,
            DinosaurType.DILOPHOSAURUS: 26,
            DinosaurType.DIMORPHODON: 10,
            DinosaurType.DODO: 2,
            DinosaurType.GRIFFIN: 32,
            DinosaurType.IGUANODON: 22,
            DinosaurType.MANTIS: 28,
            DinosaurType.MOSCHOPS: 18,
            DinosaurType.MOSASAURUS: 45,
            DinosaurType.OVIRAPTOR: 16,
            DinosaurType.PACHY: 14,
            DinosaurType.PHIOMIA: 12,
            DinosaurType.PHOENIX: 36,
            DinosaurType.PLESIOSAUR: 33,
            DinosaurType.PTERANODON: 14,
            DinosaurType.QUETZALCOATLUS: 34,
            DinosaurType.REAPER: 42,
            DinosaurType.SPINOSAURUS: 44,
            DinosaurType.THERIZINOSAUR: 40,
            DinosaurType.TITANBOA: 30,
            DinosaurType.TRILOBITE: 5,
            DinosaurType.TUSOTEUTHIS: 48,
            DinosaurType.WYVERN: 38,
            DinosaurType.ALLOSAURUS: 32,
            DinosaurType.BASILISK: 35,
            DinosaurType.COMPY: 3,
            DinosaurType.CORRUPTED_DINO: 50,
            DinosaurType.CRYPTID: 36,
            DinosaurType.GIGA: 55,
        }
        return damages.get(self.dino_type, 15)
    
    def get_aggression(self):
        aggression = {
            DinosaurType.TRIKE: 70,
            DinosaurType.RAPTOR: 85,
            DinosaurType.REX: 95,
            DinosaurType.STEGO: 60,
            DinosaurType.BRONTO: 20,
            DinosaurType.SABERTOOTH: 90,
            DinosaurType.TRICERATOPS: 75,
            DinosaurType.PARASAUROLOPHUS: 30,
            DinosaurType.GALLIMIMUS: 15,
            DinosaurType.ANKYLOSAURUS: 40,
            DinosaurType.BRACHIOSAURUS: 10,
            DinosaurType.CARNOTAURUS: 92,
            DinosaurType.DILOPHOSAURUS: 80,
            DinosaurType.DIMORPHODON: 70,
            DinosaurType.DODO: 5,
            DinosaurType.GRIFFIN: 88,
            DinosaurType.IGUANODON: 35,
            DinosaurType.MANTIS: 75,
            DinosaurType.MOSCHOPS: 50,
            DinosaurType.MOSASAURUS: 98,
            DinosaurType.OVIRAPTOR: 65,
            DinosaurType.PACHY: 55,
            DinosaurType.PHIOMIA: 25,
            DinosaurType.PHOENIX: 85,
            DinosaurType.PLESIOSAUR: 70,
            DinosaurType.PTERANODON: 45,
            DinosaurType.QUETZALCOATLUS: 75,
            DinosaurType.REAPER: 100,
            DinosaurType.SPINOSAURUS: 96,
            DinosaurType.THERIZINOSAUR: 80,
            DinosaurType.TITANBOA: 72,
            DinosaurType.TRILOBITE: 10,
            DinosaurType.TUSOTEUTHIS: 95,
            DinosaurType.WYVERN: 92,
            DinosaurType.ALLOSAURUS: 82,
            DinosaurType.BASILISK: 88,
            DinosaurType.COMPY: 40,
            DinosaurType.CORRUPTED_DINO: 100,
            DinosaurType.CRYPTID: 85,
            DinosaurType.GIGA: 99,
        }
        return aggression.get(self.dino_type, 50)
    
    def get_color(self):
        colors = {
            DinosaurType.TRIKE: (100, 200, 100),
            DinosaurType.RAPTOR: (180, 100, 100),
            DinosaurType.REX: (150, 50, 50),
            DinosaurType.STEGO: (120, 150, 80),
            DinosaurType.BRONTO: (180, 150, 100),
            DinosaurType.SABERTOOTH: (180, 100, 80),
            DinosaurType.TRICERATOPS: (100, 150, 100),
            DinosaurType.PARASAUROLOPHUS: (150, 120, 180),
            DinosaurType.GALLIMIMUS: (200, 150, 100),
            DinosaurType.ANKYLOSAURUS: (80, 100, 120),
            DinosaurType.BRACHIOSAURUS: (150, 120, 80),
            DinosaurType.CARNOTAURUS: (140, 40, 40),
            DinosaurType.DILOPHOSAURUS: (120, 80, 120),
            DinosaurType.DIMORPHODON: (100, 150, 200),
            DinosaurType.DODO: (200, 150, 120),
            DinosaurType.GRIFFIN: (220, 180, 80),
            DinosaurType.IGUANODON: (130, 160, 100),
            DinosaurType.MANTIS: (100, 200, 120),
            DinosaurType.MOSCHOPS: (140, 120, 100),
            DinosaurType.MOSASAURUS: (80, 120, 150),
            DinosaurType.OVIRAPTOR: (180, 140, 80),
            DinosaurType.PACHY: (150, 120, 150),
            DinosaurType.PHIOMIA: (160, 130, 100),
            DinosaurType.PHOENIX: (255, 150, 0),
            DinosaurType.PLESIOSAUR: (80, 150, 200),
            DinosaurType.PTERANODON: (150, 150, 180),
            DinosaurType.QUETZALCOATLUS: (100, 200, 150),
            DinosaurType.REAPER: (100, 50, 150),
            DinosaurType.SPINOSAURUS: (100, 150, 120),
            DinosaurType.THERIZINOSAUR: (180, 150, 80),
            DinosaurType.TITANBOA: (100, 120, 80),
            DinosaurType.TRILOBITE: (150, 100, 100),
            DinosaurType.TUSOTEUTHIS: (150, 120, 180),
            DinosaurType.WYVERN: (200, 100, 200),
            DinosaurType.ALLOSAURUS: (160, 80, 60),
            DinosaurType.BASILISK: (100, 150, 100),
            DinosaurType.COMPY: (100, 100, 100),
            DinosaurType.CORRUPTED_DINO: (150, 50, 200),
            DinosaurType.CRYPTID: (200, 100, 150),
            DinosaurType.GIGA: (100, 50, 50),
        }
        return colors.get(self.dino_type, (100, 100, 100))
    
    def update(self, player: Player, other_dinos: List['Dinosaur']):
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        
        # Calculate distance to player
        dist_to_player = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        
        # Aggressive behavior
        if dist_to_player < 300 and self.aggression > 50:
            self.target_player = player
            # Move towards player
            angle = math.atan2(player.y - self.y, player.x - self.x)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed
            
            # Attack if close
            if dist_to_player < 50 and self.attack_cooldown == 0:
                player.health -= self.damage
                self.attack_cooldown = 60
        else:
            self.target_player = None
            # Wander
            self.wander_timer -= 1
            if self.wander_timer <= 0:
                self.direction = random.uniform(0, 2 * math.pi)
                self.wander_timer = random.randint(60, 300)
            
            self.x += math.cos(self.direction) * self.speed
            self.y += math.sin(self.direction) * self.speed
        
        # Clamp to screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, surface):
        color = self.get_color()
        # Body
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        # Head
        pygame.draw.circle(surface, color, (self.x + self.width - 10, self.y + 5), 8)
        # Tail
        pygame.draw.line(surface, color, (self.x, self.y + self.height // 2), 
                        (self.x - 20, self.y + self.height // 2), 4)
        
        # Special features for certain dinos
        if self.dino_type == DinosaurType.SABERTOOTH:
            # Draw sabertooth fangs
            pygame.draw.line(surface, WHITE, (self.x + self.width - 8, self.y + 8), 
                           (self.x + self.width - 6, self.y + 15), 3)
        elif self.dino_type == DinosaurType.WYVERN:
            # Draw wings
            pygame.draw.line(surface, color, (self.x + 10, self.y), (self.x - 10, self.y + 15), 4)
            pygame.draw.line(surface, color, (self.x + self.width - 10, self.y), (self.x + self.width + 10, self.y + 15), 4)
        elif self.dino_type == DinosaurType.PHOENIX:
            # Draw wings with fire color
            pygame.draw.line(surface, (255, 100, 0), (self.x + 10, self.y), (self.x - 10, self.y + 15), 4)
            pygame.draw.line(surface, (255, 100, 0), (self.x + self.width - 10, self.y), (self.x + self.width + 10, self.y + 15), 4)
        
        # Health bar
        bar_width = self.width
        bar_height = 5
        pygame.draw.rect(surface, RED, (self.x, self.y - 10, bar_width, bar_height))
        health_percent = self.health / self.max_health
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, bar_width * health_percent, bar_height))

class Resource:
    def __init__(self, x: float, y: float, resource_type: ItemType):
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.quantity = self.get_initial_quantity()
        self.width = 20
        self.height = 20
    
    def get_initial_quantity(self):
        quantities = {
            ItemType.WOOD: random.randint(5, 15),
            ItemType.STONE: random.randint(3, 10),
            ItemType.FIBER: random.randint(5, 20),
            ItemType.BERRIES: random.randint(2, 8),
            ItemType.METAL: random.randint(1, 5)
        }
        return quantities.get(self.resource_type, 5)
    
    def get_color(self):
        colors = {
            ItemType.WOOD: BROWN,
            ItemType.STONE: (128, 128, 128),
            ItemType.FIBER: (144, 238, 144),
            ItemType.BERRIES: (186, 85, 211),
            ItemType.METAL: (192, 192, 192)
        }
        return colors.get(self.resource_type, WHITE)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.get_color(), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 1)

class Structure:
    def __init__(self, x: float, y: float, structure_type: str = "thatch"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.structure_type = structure_type
        self.health = 100
        self.max_health = 100
    
    def get_color(self):
        if self.structure_type == "thatch":
            return BROWN
        elif self.structure_type == "wood":
            return (139, 69, 19)
        elif self.structure_type == "stone":
            return (128, 128, 128)
        return BROWN
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.get_color(), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # Health bar
        health_percent = self.health / self.max_health
        pygame.draw.rect(surface, RED, (self.x, self.y - 10, self.width, 5))
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, self.width * health_percent, 5))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ARK: Survival Game - Complete Edition (40 Dinosaurs!)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.running = True
        self.game_over = False
        
        # Game entities
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.dinosaurs: List[Dinosaur] = []
        self.resources: List[Resource] = []
        self.structures: List[Structure] = []
        self.spawn_timer = 0
        self.day_night_cycle = 0
        self.dino_counter = {}
        
        self.initialize_world()
    
    def initialize_world(self):
        """Initialize the game world with resources and dinosaurs"""
        # Spawn initial resources
        for _ in range(15):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            resource_type = random.choice(list(ItemType))
            self.resources.append(Resource(x, y, resource_type))
        
        # Spawn initial dinosaurs - one of each type!
        for dino_type in list(DinosaurType)[:10]:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.dinosaurs.append(Dinosaur(x, y, dino_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_e:
                    self.gather_resources()
                elif event.key == pygame.K_SPACE:
                    self.place_structure()
                elif event.key == pygame.K_f:
                    self.player.health -= 10  # Test damage
    
    def gather_resources(self):
        """Gather resources near the player"""
        for resource in self.resources[:]:
            dist = math.sqrt((self.player.x - resource.x)**2 + (self.player.y - resource.y)**2)
            if dist < 80:
                amount = min(resource.quantity, 5)
                self.player.add_item(resource.resource_type, amount)
                resource.quantity -= amount
                self.player.experience += 10
                
                if resource.quantity <= 0:
                    self.resources.remove(resource)
    
    def place_structure(self):
        """Place a structure near the player"""
        if len([i for i in self.player.inventory if i.item_type == ItemType.WOOD]) >= 5:
            for item in self.player.inventory:
                if item.item_type == ItemType.WOOD:
                    item.quantity -= 5
                    if item.quantity <= 0:
                        self.player.inventory.remove(item)
                    break
            
            x = self.player.x + random.randint(-50, 50)
            y = self.player.y + random.randint(-50, 50)
            self.structures.append(Structure(x, y, "wood"))
    
    def update(self):
        if self.game_over:
            return
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()
        
        # Update dinosaurs
        for dino in self.dinosaurs:
            dino.update(self.player, self.dinosaurs)
        
        # Spawn new dinosaurs
        self.spawn_timer += 1
        if self.spawn_timer > 200:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            dino_type = random.choice(list(DinosaurType))
            self.dinosaurs.append(Dinosaur(x, y, dino_type))
            self.spawn_timer = 0
        
        # Remove dead dinosaurs and spawn resources
        for dino in self.dinosaurs[:]:
            if dino.health <= 0:
                x, y = dino.x, dino.y
                for _ in range(random.randint(3, 8)):
                    self.resources.append(Resource(x + random.randint(-20, 20), 
                                                  y + random.randint(-20, 20), 
                                                  ItemType.MEAT))
                self.dinosaurs.remove(dino)
                self.player.experience += 100
        
        # Day/night cycle
        self.day_night_cycle = (self.day_night_cycle + 1) % 2000
        
        # Check game over
        if self.player.health <= 0:
            self.game_over = True
    
    def draw(self):
        # Background
        brightness = int(100 + 100 * math.sin(self.day_night_cycle / 1000))
        bg_color = (brightness // 2, brightness, brightness // 2)
        self.screen.fill(bg_color)
        
        # Draw resources
        for resource in self.resources:
            resource.draw(self.screen)
        
        # Draw structures
        for structure in self.structures:
            structure.draw(self.screen)
        
        # Draw dinosaurs
        for dino in self.dinosaurs:
            dino.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.player.draw_stats(self.screen, self.font)
        
        # Draw dino counter
        dino_count = len(self.dinosaurs)
        dino_text = self.font.render(f"Dinosaurs: {dino_count}", True, WHITE)
        self.screen.blit(dino_text, (SCREEN_WIDTH - 250, 10))
        
        # Draw dinosaur types on screen
        dino_types_text = self.small_font.render("Types: ", True, WHITE)
        self.screen.blit(dino_types_text, (SCREEN_WIDTH - 250, 40))
        
        dino_names = {}
        for dino in self.dinosaurs:
            dino_names[dino.dino_type.name] = dino_names.get(dino.dino_type.name, 0) + 1
        
        y_offset = 60
        for name, count in list(dino_names.items())[:8]:
            name_text = self.small_font.render(f"{name}: {count}", True, WHITE)
            self.screen.blit(name_text, (SCREEN_WIDTH - 250, y_offset))
            y_offset += 20
        
        # Draw inventory
        inv_text = self.font.render("Inventory (E to gather, SPACE to build):", True, WHITE)
        self.screen.blit(inv_text, (10, SCREEN_HEIGHT - 120))
        
        y_offset = SCREEN_HEIGHT - 90
        for i, item in enumerate(self.player.inventory[:5]):
            item_text = self.font.render(f"{item.item_type.name}: {item.quantity}", True, WHITE)
            self.screen.blit(item_text, (10, y_offset + i * 20))
        
        if len(self.player.inventory) > 5:
            more_text = self.font.render(f"... and {len(self.player.inventory) - 5} more", True, WHITE)
            self.screen.blit(more_text, (10, y_offset + 100))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - YOU DIED", True, RED)
            restart_text = self.font.render("Press ESC to exit", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
