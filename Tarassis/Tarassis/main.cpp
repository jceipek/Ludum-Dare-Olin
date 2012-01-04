#include <SFML/Graphics.hpp>
#include "ResourcePath.hpp"
#include "constants.h"
#include "MainScreen.hpp"
#include "Game.hpp"

int main (int argc, const char * argv[])
{
    // Create the main window
    sf::RenderWindow window(sf::VideoMode(SCREEN_WIDTH, SCREEN_HEIGHT), "Tarassis", sf::Style::Close); //sf::Style::Fullscreen

    /*
    // Create a graphical text to display
    sf::Font font;
    if (!font.LoadFromFile(ResourcePath() + "sansation.ttf"))
    	return EXIT_FAILURE;
    sf::Text text("Hello SFML", font, 50);
    text.SetColor(sf::Color::Black);*/
    
    
    Game game(&window);
    
    //MainScreen tempScreen(&window);
        

    // Start the game loop
    while (window.IsOpened())
    {
        
    	// Clear screen
    	window.Clear();
        
        game.step();
    	
    	// Draw the string
    	//window.Draw(text);

    	// Update the window
    	window.Display();
    }

	return EXIT_SUCCESS;
}
