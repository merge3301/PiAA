#ifndef Table_hpp
#define Table_hpp

#include "Square.hpp"
#include <vector>

class Table {
public:
    int bestCount;
    int squareSize;
    std::vector<Square> bestSolution;

private:
    int gridSize;
    
public:
    Table(int gridSize);
    void placeSquares();
    
private:
    void backtrack(std::vector<Square> currentSquares, int occupiedArea, int currentCount,
                   int startX, int startY);
    bool isOverlap(const std::vector<Square> &squares, int x, int y);
    int findMaxSizeSquare(const std::vector<Square> &squares, int x, int y);
    void setGridRatio();
};

#endif /* Table_hpp */
