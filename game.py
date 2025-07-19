"""
Single Player Game class with proper button detection for all internal menus.
This fixes the button detection issues mentioned in the problem statement.
"""
import pygame
import sys
from display_manager import DisplayManager

class Game:
    def __init__(self, screen, display_manager):
        """
        Initialize the single player game.
        
        Args:
            screen: Pygame screen surface
            display_manager: DisplayManager instance for scaling
        """
        self.screen = screen
        self.display_manager = display_manager
        self.running = True
        self.current_state = "menu"  # menu, game, instructions, scores
        self.result = None
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 200)
        self.DARK_BLUE = (0, 50, 150)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 200, 0)
        
        # Store actual button rectangles for collision detection
        self.button_rects = {}
        
    def draw_button(self, text, virtual_rect, button_id, color=None):
        """
        Draw a button and store its actual rectangle for collision detection.
        Uses the same pattern as MainMenu for consistency.
        
        Args:
            text (str): Button text
            virtual_rect (pygame.Rect): Button rectangle in virtual coordinates
            button_id (str): Unique identifier for the button
            color (tuple): Button color, defaults to blue
        """
        if color is None:
            color = self.BLUE
            
        # Scale the virtual rectangle to actual coordinates
        actual_rect = self.display_manager.scale_rect(virtual_rect)
        
        # Store the actual rectangle for collision detection
        self.button_rects[button_id] = actual_rect
        
        # Draw button background
        pygame.draw.rect(self.screen, color, actual_rect)
        pygame.draw.rect(self.screen, self.BLACK, actual_rect, 2)
        
        # Draw button text
        font_size = self.display_manager.scale_font_size(32)
        font = pygame.font.Font(None, font_size)
        button_text = font.render(text, True, self.WHITE)
        
        # Center text in button
        text_rect = button_text.get_rect()
        text_rect.center = actual_rect.center
        
        self.screen.blit(button_text, text_rect)
        
    def draw_title(self, title_text):
        """Draw a title at the top of the screen."""
        title_font = pygame.font.Font(None, self.display_manager.scale_font_size(48))
        title = title_font.render(title_text, True, self.BLACK)
        
        # Center the title
        title_rect = title.get_rect()
        title_rect.center = self.display_manager.virtual_to_actual(
            self.display_manager.virtual_width // 2, 80
        )
        
        self.screen.blit(title, title_rect)
        
    def draw_game_menu(self):
        """Draw the single player game menu with proper button storage."""
        self.screen.fill(self.WHITE)
        
        # Clear button rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title("SINGLE PLAYER")
        
        # Define button dimensions in virtual coordinates
        button_width = 250
        button_height = 50
        button_spacing = 70
        start_y = 200
        
        # Draw menu buttons using the corrected pattern
        buttons = [
            ("JUGAR", "play"),
            ("INSTRUCCIONES", "instructions"),
            ("MEJORES PUNTUACIONES", "scores"),
            ("VOLVER", "back")
        ]
        
        for i, (text, button_id) in enumerate(buttons):
            y = start_y + i * button_spacing
            virtual_rect = self.display_manager.get_centered_rect(button_width, button_height)
            virtual_rect.y = y
            self.draw_button(text, virtual_rect, button_id)
            
    def draw_instructions_screen(self):
        """Draw the instructions screen with proper button detection."""
        self.screen.fill(self.WHITE)
        
        # Clear button rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title("INSTRUCCIONES")
        
        # Draw instructions text
        instructions = [
            "1. Usa las teclas de flecha para mover",
            "2. Evita los obstáculos",
            "3. Recoge puntos para aumentar tu puntuación",
            "4. El juego termina si tocas un obstáculo",
            "",
            "¡Diviértete jugando!"
        ]
        
        font = pygame.font.Font(None, self.display_manager.scale_font_size(24))
        start_y = 150
        
        for i, line in enumerate(instructions):
            if line:  # Skip empty lines
                text_surface = font.render(line, True, self.BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = self.display_manager.virtual_to_actual(
                    self.display_manager.virtual_width // 2, start_y + i * 30
                )
                self.screen.blit(text_surface, text_rect)
                
        # Back button
        back_button_rect = self.display_manager.get_centered_rect(200, 50)
        back_button_rect.y = 450
        self.draw_button("VOLVER", back_button_rect, "back")
        
    def draw_scores_screen(self):
        """Draw the high scores screen with proper button detection."""
        self.screen.fill(self.WHITE)
        
        # Clear button rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title("MEJORES PUNTUACIONES")
        
        # Draw sample scores
        scores = [
            "1. 15000 puntos",
            "2. 12500 puntos", 
            "3. 10000 puntos",
            "4. 8500 puntos",
            "5. 7000 puntos"
        ]
        
        font = pygame.font.Font(None, self.display_manager.scale_font_size(28))
        start_y = 200
        
        for i, score in enumerate(scores):
            text_surface = font.render(score, True, self.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = self.display_manager.virtual_to_actual(
                self.display_manager.virtual_width // 2, start_y + i * 40
            )
            self.screen.blit(text_surface, text_rect)
            
        # Back button
        back_button_rect = self.display_manager.get_centered_rect(200, 50)
        back_button_rect.y = 450
        self.draw_button("VOLVER", back_button_rect, "back")
        
    def draw_game_screen(self):
        """Draw the actual game screen with proper controls."""
        self.screen.fill(self.WHITE)
        
        # Clear button rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title("JUGANDO...")
        
        # Draw game area (placeholder)
        game_area_rect = pygame.Rect(100, 150, 600, 300)
        actual_game_rect = self.display_manager.scale_rect(game_area_rect)
        pygame.draw.rect(self.screen, self.GRAY, actual_game_rect)
        pygame.draw.rect(self.screen, self.BLACK, actual_game_rect, 3)
        
        # Game instructions
        font = pygame.font.Font(None, self.display_manager.scale_font_size(24))
        instruction_text = font.render("Presiona ESC para volver al menú", True, self.BLACK)
        instruction_rect = instruction_text.get_rect()
        instruction_rect.center = self.display_manager.virtual_to_actual(
            self.display_manager.virtual_width // 2, 500
        )
        self.screen.blit(instruction_text, instruction_rect)
        
    def handle_click(self, mouse_pos):
        """
        Handle mouse click events using direct collision detection.
        Fixed to use the same pattern as MainMenu.
        
        Args:
            mouse_pos (tuple): Mouse position in screen coordinates
        """
        for button_id, rect in self.button_rects.items():
            if rect.collidepoint(mouse_pos):
                if button_id == "play":
                    self.current_state = "game"
                elif button_id == "instructions":
                    self.current_state = "instructions"
                elif button_id == "scores":
                    self.current_state = "scores"
                elif button_id == "back":
                    if self.current_state in ["instructions", "scores"]:
                        self.current_state = "menu"
                    else:
                        self.result = "back_to_main"
                        self.running = False
                break
                
    def handle_key_press(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            if self.current_state == "game":
                self.current_state = "menu"
            else:
                self.result = "back_to_main"
                self.running = False
                
    def run(self):
        """Run the single player game loop."""
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
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                    
            # Draw current state
            if self.current_state == "menu":
                self.draw_game_menu()
            elif self.current_state == "instructions":
                self.draw_instructions_screen()
            elif self.current_state == "scores":
                self.draw_scores_screen()
            elif self.current_state == "game":
                self.draw_game_screen()
                
            pygame.display.flip()
            clock.tick(60)
            
        return self.result