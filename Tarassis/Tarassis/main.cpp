#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include "ResourcePath.hpp"
#include "constants.h"
#include "MainScreen.hpp"

enum gameState {
    MAIN_SCREEN,
    PLAYING
    } gameState;

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

    // Load a music to play
    sf::Music music;
    if (!music.OpenFromFile(ResourcePath() + "title.ogg"))
    	return EXIT_FAILURE;

    // Play the music
    music.SetLoop(true);
    music.Play();
    
    MainScreen tempScreen(&window);
        
    
    gameState = MAIN_SCREEN;

    // Start the game loop
    while (window.IsOpened())
    {
        
    	// Clear screen
    	window.Clear();
        
        switch (gameState) {
            case MAIN_SCREEN:
                //<#statements#>
                tempScreen.updateLogic();
                tempScreen.updateDraw();
                break;
                
            default:
                break;
        }
    	
    	// Draw the string
    	//window.Draw(text);

    	// Update the window
    	window.Display();
    }

	return EXIT_SUCCESS;
}
