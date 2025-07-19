#!/usr/bin/env python3
"""
Generate a visual demo of the UI to show the fixes work.
Creates a screenshot of the game interface.
"""
import pygame
import os
import sys

# Set up headless display
os.environ['SDL_VIDEODRIVER'] = 'dummy'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_demo_screenshot():
    """Create a demo screenshot showing the fixed UI."""
    pygame.init()
    
    # Create screens at different sizes to show scaling
    sizes = [(800, 600), (1200, 900)]
    
    from display_manager import DisplayManager
    from main_menu import MainMenu
    from game import Game
    from game_multiplayer import MultiplayerGame
    
    for i, (width, height) in enumerate(sizes):
        print(f"Creating demo for {width}x{height}...")
        
        # Create surface
        screen = pygame.Surface((width, height))
        dm = DisplayManager(800, 600)  # Virtual size
        dm.update_actual_size(width, height)
        
        # Demo main menu
        main_menu = MainMenu(screen, dm)
        main_menu.draw_main_menu()
        
        # Save main menu screenshot
        pygame.image.save(screen, f"demo_main_menu_{width}x{height}.png")
        print(f"✓ Saved demo_main_menu_{width}x{height}.png")
        
        # Demo single player menu
        game = Game(screen, dm)
        game.draw_game_menu()
        pygame.image.save(screen, f"demo_single_player_{width}x{height}.png")
        print(f"✓ Saved demo_single_player_{width}x{height}.png")
        
        # Demo multiplayer IP screen
        multiplayer = MultiplayerGame(screen, dm)
        multiplayer.ip_input = "192.168.1.100"
        multiplayer.draw_ip_input_screen()
        pygame.image.save(screen, f"demo_multiplayer_{width}x{height}.png")
        print(f"✓ Saved demo_multiplayer_{width}x{height}.png")
    
    print("\nDemo screenshots created! These show:")
    print("- Properly scaled UI elements at different window sizes")
    print("- Centered buttons and text")
    print("- Fixed input fields with proper scaling")
    print("- All elements maintain proper proportions")

if __name__ == "__main__":
    create_demo_screenshot()