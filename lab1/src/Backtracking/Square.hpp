#ifndef Square_hpp
#define Square_hpp

struct Square {
    const int trailing, bottom;
    int x, y, size;
    
    Square(int x, int y, int size);
    Square(const Square &other);
    Square &operator=(const Square &other);
};

#endif /* Square_hpp */
