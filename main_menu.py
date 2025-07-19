"""
Main Menu class with proper button detection pattern.
This serves as the reference implementation that other menus should follow.
"""
import pygame
import sys
from display_manager import DisplayManager

class MainMenu:
    def __init__(self, screen, display_manager):
        """
        Initialize the main menu.
        
        Args:
            screen: Pygame screen surface
            display_manager: DisplayManager instance for scaling
        """
        self.screen = screen
        self.display_manager = display_manager
        self.running = True
        self.result = None
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 200)
        self.DARK_BLUE = (0, 50, 150)
        self.GRAY = (128, 128, 128)
        
        # Store actual button rectangles for collision detection
        self.button_rects = {}
        
    def draw_title(self):
        """Draw the game title."""
        title_font = pygame.font.Font(None, self.display_manager.scale_font_size(72))
        title_text = title_font.render("JUEGO DE SOCKETS", True, self.BLACK)
        
        # Center the title
        title_rect = title_text.get_rect()
        title_rect.center = self.display_manager.virtual_to_actual(
            self.display_manager.virtual_width // 2, 100
        )
        
        self.screen.blit(title_text, title_rect)
        
    def draw_button(self, text, virtual_rect, button_id):
        """
        Draw a button and store its actual rectangle for collision detection.
        
        Args:
            text (str): Button text
            virtual_rect (pygame.Rect): Button rectangle in virtual coordinates
            button_id (str): Unique identifier for the button
        """
        # Scale the virtual rectangle to actual coordinates
        actual_rect = self.display_manager.scale_rect(virtual_rect)
        
        # Store the actual rectangle for collision detection
        self.button_rects[button_id] = actual_rect
        
        # Draw button background
        pygame.draw.rect(self.screen, self.BLUE, actual_rect)
        pygame.draw.rect(self.screen, self.BLACK, actual_rect, 2)
        
        # Draw button text
        font_size = self.display_manager.scale_font_size(36)
        font = pygame.font.Font(None, font_size)
        button_text = font.render(text, True, self.WHITE)
        
        # Center text in button
        text_rect = button_text.get_rect()
        text_rect.center = actual_rect.center
        
        self.screen.blit(button_text, text_rect)
        
    def draw_main_menu(self):
        """Draw the main menu screen."""
        self.screen.fill(self.WHITE)
        
        # Clear button rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title()
        
        # Define button dimensions in virtual coordinates
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = 250
        
        # Draw menu buttons
        buttons = [
            ("SINGLE PLAYER", "single_player"),
            ("MULTIJUGADOR", "multiplayer"),
            ("SALIR", "exit")
        ]
        
        for i, (text, button_id) in enumerate(buttons):
            y = start_y + i * button_spacing
            virtual_rect = self.display_manager.get_centered_rect(button_width, button_height)
            virtual_rect.y = y
            self.draw_button(text, virtual_rect, button_id)
            
    def handle_click(self, mouse_pos):
        """
        Handle mouse click events using direct collision detection.
        
        Args:
            mouse_pos (tuple): Mouse position in screen coordinates
        """
        for button_id, rect in self.button_rects.items():
            if rect.collidepoint(mouse_pos):
                if button_id == "single_player":
                    self.result = "single_player"
                    self.running = False
                elif button_id == "multiplayer":
                    self.result = "multiplayer"
                    self.running = False
                elif button_id == "exit":
                    self.result = "exit"
                    self.running = False
                break
                
    def run(self):
        """Run the main menu loop."""
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.result = "exit"
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    self.display_manager.update_actual_size(event.w, event.h)
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                        
            self.draw_main_menu()
            pygame.display.flip()
            clock.tick(60)
            
        return self.result