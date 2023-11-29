#include <iostream>
#include "pystrlib.hpp"

int timer, x, ans;

char ch[50];

inline void draw(int y) {
    ch[y] = (x <= y && y <= x + 2) ? '#' : '.';
    if (y == 39) std::cout << ch << std::endl;
}

int main() {
    freopen("day10.txt", "r", stdin);
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> vec = lib::split(line, " ");
            if (vec[0] == "addx") draw(timer % 40), draw((timer + 1) % 40), x += std::stoi(vec[1]), timer += 2;
            else draw(timer % 40), ++timer;
        }
    }
    std::cout << ans << std::endl;
    return 0;
}