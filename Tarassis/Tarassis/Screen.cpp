//
//  Level.cpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/4/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#include <iostream>
#include "Screen.hpp"

Screen::Screen (sf::RenderWindow *window) {
    this->window = window;
}

void Screen::updateDraw() {
    // Draw the sprite
    
    
    //std::cout << "Drawing\n";
}

void Screen::processInput(sf::Event event) {
    // Process events
    
    // Close window : exit
    if (event.Type == sf::Event::Closed)
        this->window->Close();
    
    // Escape pressed : exit
    if (event.Type == sf::Event::KeyPressed && event.Key.Code == sf::Keyboard::Escape)
        this->window->Close();
}