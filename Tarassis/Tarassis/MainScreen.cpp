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



MainScreen::MainScreen (sf::RenderWindow *window) {
    this->window = window;
    
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
        this->processStandardInput(event);
    }
}

void MainScreen::updateDraw() {
    // Draw the sprite
    this->window->Draw(this->background);
    
    //std::cout << "Drawing\n";
}

void MainScreen::processStandardInput(sf::Event event) {
    // Process events

    // Close window : exit
    if (event.Type == sf::Event::Closed)
        this->window->Close();
        
        // Escape pressed : exit
        if (event.Type == sf::Event::KeyPressed && event.Key.Code == sf::Keyboard::Escape)
            this->window->Close();
}