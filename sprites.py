import random  
import pygame


SCREEN_RECT = pygame.Rect(0, 0, 640, 360)
FRAME_PER_SEC = 60
CREATE_WAVE_EVENT = pygame.USEREVENT + 1
CREATE_I_EVENT = pygame.USEREVENT + 2
CREATE_OVER_EVENT = pygame.USEREVENT + 3
GOLD = (255, 215, 0)
class GameSprite(pygame.sprite.Sprite):
    
    def __init__(self, image_name, speed=2):
        
        super().__init__()

        # Define the sprite's attributes
        self.image = pygame.image.load(image_name)  # Load the sprite image
        self.rect = self.image.get_rect()  # Get the image's rectangular area
        self.speed = speed  # Set the movement speed

    def update(self):
        # Move the sprite horizontally (leftward)
        self.rect.x -= self.speed


class Background(GameSprite):
    """Background sprite for the game."""
    def __init__(self, image_path, is_alt=False):
        # Call the parent class initializer
        super().__init__(image_path)
        # If it's an alternate image, set its initial position to the right
        if is_alt:
            self.rect.x = self.rect.width
        else:
            self.rect.x = 0

    def update(self):
        # Call the parent class's update method
        super().update()
        # If the background moves off-screen, reset its position to the right
        if self.rect.x <= -SCREEN_RECT.width:
            self.rect.x = self.rect.width


class Man(GameSprite):
    """Sprite for the monkey character."""

    def __init__(self):
        super().__init__("./images/man.png", 0)

        # Set the initial position of the monkey
        self.rect.centerx = SCREEN_RECT.centerx - 70
        self.rect.bottom = SCREEN_RECT.height - 20
        # Set the distance between the monkey and the ground
        self.bottom_to_ground = SCREEN_RECT.height - 20

    def update(self):
        self.rect.y += self.speed

        # Ensure the monkey stays within the screen boundaries
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > self.bottom_to_ground:
            self.rect.bottom = self.bottom_to_ground


class Wave(GameSprite):
    """Wave sprite."""

    def __init__(self):
        super().__init__("./images/wave.png")

        # Set a random speed for the wave
        self.speed = random.randint(2, 4)

        # Set the wave's initial position on the right side of the screen
        self.rect.x = SCREEN_RECT.width
        self.rect.bottom = SCREEN_RECT.height

    def update(self):
        # Call the parent class's update method
        super().update()

        # If the wave moves off-screen, remove it from all sprite groups
        if self.rect.right <= 0:
            self.kill()

    def __del__(self):
        print(f"Wave destroyed at {self.rect}")  # Print a message when the wave is deleted


class Score(pygame.sprite.Sprite):
    """Score sprite for displaying the player's score."""

    def __init__(self):
        
        super().__init__()
        self.score = 0
        self.font_type = pygame.font.match_font('Microsoft YaHei')
        self.font = pygame.font.Font(self.font_type, 20)
        self.image = self.font.render(f"Score: {self.score}", True, GOLD)
        self.rect = self.image.get_rect()

    def update(self):
        # Update the score display
        self.image = self.font.render(f"Score: {self.score}", True, GOLD)
        self.rect = self.image.get_rect()


class Countdown(pygame.sprite.Sprite):
    """Countdown timer sprite."""

    def __init__(self, start_time):
        # Call the parent class initializer
        super().__init__()

        # Set the initial countdown time
        self.start_time = start_time
        # Set up font for displaying the countdown
        self.font_type = pygame.font.match_font('Microsoft YaHei')
        self.font = pygame.font.Font(self.font_type, 50)
        self.image = self.font.render(str(self.start_time), True, GOLD)
        self.rect = self.image.get_rect()
        self.rect.right = SCREEN_RECT.width  # Align the timer to the right
        self.rect.y = 0  # Set the vertical position

    def update(self):
        # Update the countdown display
        self.image = self.font.render(str(self.start_time), True, GOLD)
        self.rect = self.image.get_rect()
        self.rect.right = SCREEN_RECT.width
        self.rect.y = 0


class Menu(pygame.sprite.Sprite):
    """Menu sprite for the game."""

    def __init__(self):
        # Call the parent class initializer
        super().__init__()
        self.display = False  # Set the menu visibility to hidden initially
        # Set up font for the menu text
        self.font_type = pygame.font.match_font('Microsoft YaHei')
        self.font = pygame.font.Font(self.font_type, 30)
        self.image = self.font.render("", True, GOLD)
        self.rect = self.image.get_rect()

    def update(self):
        if self.display:
            # Update the menu text to "Restart"
            self.image = self.font.render("Restart", True, GOLD)
            self.rect = self.image.get_rect()
            self.rect.centerx = SCREEN_RECT.centerx  # Center horizontally
            self.rect.centery = SCREEN_RECT.centery + 50  


class Mouse(pygame.sprite.Sprite):
    """Mouse cursor sprite."""

    def __init__(self):
        super().__init__()
        self.display = False  
        self.image = pygame.Surface((5, 5))
        self.rect = self.image.get_rect()  

    def update(self):
        super().update()
