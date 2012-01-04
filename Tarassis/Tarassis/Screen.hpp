//
//  Screen.hpp
//  Tarassis
//
//  Created by Julian Ceipek on 1/4/12.
//  Copyright (c) 2012 Franklin W. Olin College of Engineering. All rights reserved.
//

#ifndef Tarassis_Screen_hpp
#define Tarassis_Screen_hpp

#include <SFML/Graphics.hpp>

class Screen {

protected:
    sf::RenderWindow* window;
public:
    Screen (sf::RenderWindow*);
    void processInput(sf::Event);
    void updateLogic();
    void updateDraw();
};

#endif
