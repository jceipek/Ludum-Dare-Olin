//
//  MainScreen.hpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/3/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#ifndef Tarassis_MainScreen_h
#define Tarassis_MainScreen_h

#include <SFML/Graphics.hpp>

class MainScreen {
    //instance variables
    sf::Texture bgTex;
    sf::Sprite background;
    sf::RenderWindow* window;
public:
    MainScreen (sf::RenderWindow*);
    
    //<#member functions#>
    void processStandardInput(sf::Event event);
    void updateLogic();
    void updateDraw();
};

#endif
