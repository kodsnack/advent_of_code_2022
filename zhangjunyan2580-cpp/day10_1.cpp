#include <iostream>
#include "pystrlib.hpp"

int timer, x, ans;

int main() {
    freopen("day10.txt", "r", stdin);
    x = 1; timer = 1;
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> vec = lib::split(line, " ");
            int v = timer % 40;
            if ((v == 19 && vec[0] == "addx") || v == 20) ans += (timer / 40 * 40 + 20) * x;
            if (vec[0] == "addx") x += std::stoi(vec[1]), timer += 2;
            else ++timer;
        }
    }
    std::cout << ans << std::endl;
    return 0;
}