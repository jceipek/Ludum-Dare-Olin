//
//  Game.cpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/3/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#include <iostream>

#include "Game.hpp"

Game::Game (sf::RenderWindow* window) : menu(window) {
    this->window = window;
    this->activeLevelIndex = 0;
    this->loadMenu();
}

void Game::loadNextLevel() {
    this->activeLevelIndex ++;
}

void Game::loadMenu() {
    //this->menu = MainScreen::MainScreen(this->window);
    
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
            menu.updateLogic();
            menu.updateDraw();
            break;
            
        default:
            break;
    }
}


