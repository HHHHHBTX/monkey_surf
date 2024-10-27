import pygame.display

from sprites import *


class Run_and_Jump_Game(object):
    

    def __init__(self):
        print("game start")
        pygame.init()
        pygame.display.set_caption("monkey_surf")
        # 1.set up windows
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.Create the game clock to control the frame rate
        self.clock = pygame.time.Clock()
        # 3.Create sprites and sprite groups
        self.__create_sprites()
        # 4.Set a timer event to create waves every 3 seconds
        pygame.time.set_timer(CREATE_WAVE_EVENT, 3000)
        # 5.Set a countdown timer to trigger every 1 second
        pygame.time.set_timer(CREATE_I_EVENT, 1000)
        # 6.Set a game-over timer to end the game after 30 seconds
        pygame.time.set_timer(CREATE_OVER_EVENT, 30000)
        # 7.Initialize the game state (1 = running, 0 = ended, -1 = exit
        self.game_state = 1

    def __create_sprites(self):
       

        # Create the sky background
        bg1 = Background("./images/background_16_9.png", False)
        bg2 = Background("./images/background_16_9.png", True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # Create the inner sea background and set its speed
        sea_bg_1 = Background("./images/sea_bg_1_16_9.png", False)
        sea_bg_2 = Background("./images/sea_bg_1_16_9.png", True)
        #speed
        sea_bg_1.speed = 2
        sea_bg_2.speed = 2
        sea_bg_1.rect.bottom = SCREEN_RECT.height
        sea_bg_2.rect.bottom = SCREEN_RECT.height
        self.sea_bg_ground_1 = pygame.sprite.Group(sea_bg_1, sea_bg_2)

        # Create the outer sea background and set its speed
        sea_bg_3 = Background("./images/sea_bg_2_16_9.png", False)
        sea_bg_4 = Background("./images/sea_bg_2_16_9.png", True)
        # speed
        sea_bg_3.speed = 3
        sea_bg_4.speed = 3
        sea_bg_3.rect.bottom = SCREEN_RECT.height
        sea_bg_4.rect.bottom = SCREEN_RECT.height
        self.sea_bg_ground_2 = pygame.sprite.Group(sea_bg_3, sea_bg_4)

        # Create the wave sprite group
        self.wave_group = pygame.sprite.Group()
        # Create the monkey character sprite and its group
        self.man = Man()
        self.man_group = pygame.sprite.Group(self.man)
        # Create the score sprite and its group
        self.score_sprite = Score()
        self.score_group = pygame.sprite.Group(self.score_sprite)
        # Create the countdown sprite and its group
        self.countdown_sprite = Countdown(30)
        self.countdown_group = pygame.sprite.Group(self.countdown_sprite)
        # Create the menu sprite and its group
        self.menu_sprite = Menu()
        self.menu_group = pygame.sprite.Group(self.menu_sprite)
        # Create the mouse sprite and its group
        self.mouse_sprite = Mouse()
        self.mouse_group = pygame.sprite.Group(self.mouse_sprite)

    def start_game(self):
        print("game start")
        # pygame.mixer.init()
        # pygame.mixer.music.load("./music/music.mp3")
        # pygame.mixer.music.play()

        while True:
            if self.game_state == 1:
                """game is running"""
                self.clock.tick(FRAME_PER_SEC)  # Set the frame rate
                self.__event_handler()  # Handle game events
                self.__check_collide()  # Check for collisions
                self.__update_sprites()  # Update and draw all sprites
                pygame.display.update()  # Refresh the display

            elif self.game_state == 0:
                """game ends"""

                self.__event_menu_handler()  # Handle menu events
                self.__check_menu_collide()  # Check for menu clicks
                self.__update_menu()  # Update the menu display
                pygame.display.update()  # Refresh the display
            elif self.game_state == -1:
                """game exit"""
                Run_and_Jump_Game.__game_over()


    def __event_handler(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = -1  # Exit the game
            elif event.type == CREATE_WAVE_EVENT: #（exit and create wave)
                wave = Wave()  
                self.wave_group.add(wave)  
                self.countdown_sprite.start_time -= 1  # Decrease countdown
                self.score_sprite.score += 10  # Increase score
            elif event.type == CREATE_OVER_EVENT:
                self.menu_sprite.display = True  # Show the menu
                self.game_state = 0  # End the current round

        keys_pressed = pygame.key.get_pressed()  # Get pressed keys
        if keys_pressed[pygame.K_SPACE]:
            self.man.speed = -10  # Jump if spacebar is pressed
        else:
            self.man.speed = 10  # Fall otherwise

    def __check_collide(self):
        """Check for collisions."""
        waves = pygame.sprite.spritecollide(self.man, self.wave_group, True)
        if len(waves) > 0:  # If collision occurs
            self.menu_sprite.display = True  # Show the menu
            self.game_state = 0  # End the current round

    def __update_sprites(self):
        """Update and draw all sprites."""
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.sea_bg_ground_1.update()
        self.sea_bg_ground_1.draw(self.screen)

        self.man_group.update()
        self.man_group.draw(self.screen)

        self.wave_group.update()
        self.wave_group.draw(self.screen)

        self.sea_bg_ground_2.update()
        self.sea_bg_ground_2.draw(self.screen)

        self.score_group.update()
        self.score_group.draw(self.screen)

        self.countdown_group.update()
        self.countdown_group.draw(self.screen)

    def __event_menu_handler(self):
        """Handle menu events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = -1  # Exit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()  # Get the mouse position
                    self.mouse_sprite.rect.top = pos[1]
                    self.mouse_sprite.rect.left = pos[0]
                    self.menu_sprite.update()  # Update the menu

    def __check_menu_collide(self):
        """Check if the mouse clicks on the menu."""
        click_list = pygame.sprite.spritecollide(self.menu_sprite, self.mouse_group, False)
        if len(click_list) > 0:  # If the menu is clicked
            self.game_state = 1  # Restart the game
            self.mouse_sprite.rect.top = 0  # Reset mouse position
            self.mouse_sprite.rect.left = 0
            pygame.time.set_timer(CREATE_OVER_EVENT, 0)  # Reset timer
            pygame.time.set_timer(CREATE_OVER_EVENT, 30000)
            self.score_sprite.score = 0  # Reset score
            self.countdown_sprite.start_time = 30  # Reset countdown

    def __update_menu(self):
        """Update and draw the menu."""
        self.menu_group.update()
        self.menu_group.draw(self.screen)

        self.mouse_group.update()
        self.mouse_group.draw(self.screen)

    @staticmethod
    def __game_over():
        """End the game."""
        print("Game over")
        pygame.quit()  
        exit()  

if __name__ == "__main__":
    game = Run_and_Jump_Game()
 
    game.start_game()