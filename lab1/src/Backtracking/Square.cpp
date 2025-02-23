#include "Square.hpp"

Square::Square(int x, int y, int size)
    : x(x), y(y), size(size), trailing(x + size), bottom(y + size) {}

Square::Square(const Square &other)
    : x(other.x), y(other.y), size(other.size), trailing(other.trailing), bottom(other.bottom) {}

Square &Square::operator=(const Square &other) {
    if (this != &other) {
        x = other.x;
        y = other.y;
        size = other.size;
    }
    return *this;
}
