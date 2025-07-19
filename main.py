"""
Main application that demonstrates the fixed resizing and button detection issues.
This file serves as a test harness to verify that all the fixes work correctly.
"""
import pygame
import sys
from display_manager import DisplayManager
from main_menu import MainMenu
from game import Game
from game_multiplayer import MultiplayerGame

class SocketGameApp:
    def __init__(self):
        """Initialize the main application."""
        pygame.init()
        
        # Initialize display with resizable window
        self.initial_width = 800
        self.initial_height = 600
        self.screen = pygame.display.set_mode(
            (self.initial_width, self.initial_height), 
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Juego de Sockets - Redimensionamiento Corregido")
        
        # Initialize display manager
        self.display_manager = DisplayManager(self.initial_width, self.initial_height)
        
        # Enable text input for multiplayer IP input
        pygame.key.set_repeat(500, 50)
        
        self.running = True
        
    def run(self):
        """Run the main application loop."""
        while self.running:
            # Show main menu
            main_menu = MainMenu(self.screen, self.display_manager)
            result = main_menu.run()
            
            if result == "single_player":
                # Run single player game
                game = Game(self.screen, self.display_manager)
                game_result = game.run()
                
                if game_result == "exit":
                    self.running = False
                    
            elif result == "multiplayer":
                # Run multiplayer game
                multiplayer = MultiplayerGame(self.screen, self.display_manager)
                multiplayer_result = multiplayer.run()
                
                if multiplayer_result == "exit":
                    self.running = False
                    
            elif result == "exit":
                self.running = False
                
        pygame.quit()
        sys.exit()

def main():
    """Main entry point."""
    try:
        app = SocketGameApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()