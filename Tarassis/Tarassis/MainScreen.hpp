//
//  MainScreen.hpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/3/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#ifndef Tarassis_MainScreen_hh
#define Tarassis_MainScreen_hh

#include <SFML/Graphics.hpp>
#include "Screen.hpp"

class MainScreen:public Screen {
    //instance variables
    sf::Texture bgTex;
    sf::Sprite background;
    
public:
    MainScreen (sf::RenderWindow*);
    
    //<#member functions#>
    void processInput(sf::Event event);
    void updateLogic();
    void updateDraw();
};

#endif
