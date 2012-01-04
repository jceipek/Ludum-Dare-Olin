//
//  Game.hpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/3/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#ifndef Tarassis_Game_hpp
#define Tarassis_Game_hpp

#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include "ResourcePath.hpp"
#include "MainScreen.hpp"

enum gameState {
    INITIALIZING,
    MAIN_SCREEN,
    PLAYING
};

class Game {
    sf::RenderWindow* window;
    
    int activeLevelIndex;
    enum gameState state;
    
    MainScreen* menu;
    
    // Load background music
    sf::Music music;

    
public:
    Game (sf::RenderWindow*);
    ~Game();
    void loadNextLevel();
    void loadMenu();
    int getActiveLevelIndex();
    enum gameState getGameState();
    
    void step();
};

#endif
