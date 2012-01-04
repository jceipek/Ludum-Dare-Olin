//
//  Game.cpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/3/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#include <iostream>

#include "Game.hpp"

Game::Game (sf::RenderWindow* window) {
    this->state = INITIALIZING;
    this->window = window;
    this->activeLevelIndex = 0;
    this->menu = NULL;
    this->loadMenu();
}

Game::~Game() {
    if (this->menu != NULL) {
        std::cout << "Deleting menu\n";
        delete this->menu;
    }
}

void Game::loadNextLevel() {
    this->activeLevelIndex ++;
}

void Game::loadMenu() {
    std::cout << "Loading menu\n";
    this->menu = new MainScreen(this->window);
    
    
    if (!this->music.OpenFromFile(ResourcePath() + "title.ogg"))
        std::cout << "Unable to load title music!";
    
    // Play the music
    music.SetLoop(true);
    music.Play();
    
    this->state = MAIN_SCREEN;
}

int Game::getActiveLevelIndex() {
    return this->activeLevelIndex;
}

enum gameState Game::getGameState() {
    return this->state;
}

void Game::step() {    
    switch (this->state) {
        case MAIN_SCREEN:
            this->menu->updateLogic();
            this->menu->updateDraw();
            break;
            
        default:
            break;
    }
}


