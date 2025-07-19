#!/usr/bin/env python3
"""
Test script to verify the game functionality and resizing fixes.
This script can be run to test that all buttons work and resizing functions correctly.
"""
import pygame
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_display_manager():
    """Test the display manager functionality."""
    print("Testing DisplayManager...")
    
    from display_manager import DisplayManager
    
    # Create display manager
    dm = DisplayManager(800, 600)
    
    # Test scaling
    dm.update_actual_size(1600, 1200)
    scale_x, scale_y = dm.get_scale_factors()
    
    assert scale_x == 2.0, f"Expected scale_x=2.0, got {scale_x}"
    assert scale_y == 2.0, f"Expected scale_y=2.0, got {scale_y}"
    
    # Test coordinate conversion
    actual_x, actual_y = dm.virtual_to_actual(100, 100)
    assert actual_x == 200, f"Expected actual_x=200, got {actual_x}"
    assert actual_y == 200, f"Expected actual_y=200, got {actual_y}"
    
    virtual_x, virtual_y = dm.actual_to_virtual(200, 200)
    assert virtual_x == 100, f"Expected virtual_x=100, got {virtual_x}"
    assert virtual_y == 100, f"Expected virtual_y=100, got {virtual_y}"
    
    # Test rect scaling
    virtual_rect = pygame.Rect(50, 50, 100, 100)
    actual_rect = dm.scale_rect(virtual_rect)
    
    assert actual_rect.x == 100, f"Expected rect.x=100, got {actual_rect.x}"
    assert actual_rect.y == 100, f"Expected rect.y=100, got {actual_rect.y}"
    assert actual_rect.width == 200, f"Expected rect.width=200, got {actual_rect.width}"
    assert actual_rect.height == 200, f"Expected rect.height=200, got {actual_rect.height}"
    
    print("✓ DisplayManager tests passed!")

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from display_manager import DisplayManager
        print("✓ display_manager imported successfully")
        
        from main_menu import MainMenu
        print("✓ main_menu imported successfully")
        
        from game import Game
        print("✓ game imported successfully")
        
        from game_multiplayer import MultiplayerGame
        print("✓ game_multiplayer imported successfully")
        
        import main
        print("✓ main imported successfully")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
        
    return True

def test_pygame_initialization():
    """Test that pygame initializes correctly."""
    print("Testing pygame initialization...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Test Window")
        print("✓ Pygame initialized successfully")
        
        # Test basic drawing
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), (100, 100, 200, 100))
        pygame.display.flip()
        print("✓ Basic drawing works")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Pygame error: {e}")
        return False

def run_manual_test():
    """Run the actual game for manual testing."""
    print("\nStarting manual test of the game...")
    print("Instructions for manual testing:")
    print("1. Test window resizing by dragging window edges")
    print("2. Test all buttons in the main menu")
    print("3. Test all buttons in single player menus")
    print("4. Test IP input field in multiplayer")
    print("5. Press ESC to exit from any screen")
    print("6. Verify all UI elements scale properly with window size")
    print("\nStarting game in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        import main
        main.main()
    except Exception as e:
        print(f"Error running manual test: {e}")

def main():
    """Main test function."""
    print("=== Socket Game Test Suite ===\n")
    
    # Run automated tests
    if not test_imports():
        print("Import tests failed, cannot continue.")
        return
        
    test_display_manager()
    
    if not test_pygame_initialization():
        print("Pygame tests failed, cannot run manual test.")
        return
        
    print("\n=== All automated tests passed! ===\n")
    
    # Ask user if they want to run manual test
    response = input("Run manual test? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        run_manual_test()
    else:
        print("Manual test skipped.")
        print("\nTo run the game manually, execute: python main.py")

if __name__ == "__main__":
    main()