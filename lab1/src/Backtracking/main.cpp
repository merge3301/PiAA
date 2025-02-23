#include "main.h"
#include "Table.hpp"

int** getBestSolution(int* bestCount, int gridSize){
    Table table(gridSize);
    table.placeSquares();
    
    *bestCount = table.bestCount;
    int **solution = new int *[*bestCount];

    for (int i = 0; i < *bestCount; ++i) {
        solution[i] = new int[3];
    }
    for (int i = 0; i < *bestCount; ++i) {
        solution[i][0] = table.bestSolution[i].x * table.squareSize;
        solution[i][1] = table.bestSolution[i].y * table.squareSize;
        solution[i][2] = table.bestSolution[i].size * table.squareSize;
    }
    return solution;
}
