//
//  MainScreen.cpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/3/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#include <iostream>
#include "MainScreen.hpp"
#include "ResourcePath.hpp"



MainScreen::MainScreen (sf::RenderWindow *window) :Screen(window) {
    
    // Load a sprite to display
    sf::Texture texture;
    this->bgTex = texture;
    if (!(this->bgTex).LoadFromFile(ResourcePath() + "IntroPage.png")) {
        std::cout << ResourcePath() + "IntroPage.png" << " Not found!\n";
        throw "IntroPage Image Does Not Exist";
    }
    sf::Sprite bg(this->bgTex);
    
    this->background = bg;
}

void MainScreen::updateLogic() {
    sf::Event event;
    while (this->window->PollEvent(event))
    {
        this->processInput(event);
    }
}

void MainScreen::updateDraw() {
    this->window->Draw(this->background);
}

void MainScreen::processInput(sf::Event event) {
    Screen::processInput(event);
}