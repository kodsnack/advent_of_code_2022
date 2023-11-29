#include <iostream>
#include "pystrlib.hpp"

int map[1000][200], mh;

bool fall_sand() {
    int px = 500, py = 0;
    while (py <= mh) {
        if (!map[px][py + 1]) ++py;
        else if (!map[px - 1][py + 1]) ++py, --px;
        else if (!map[px + 1][py + 1]) ++py, ++px;
        else break;
    }
    map[px][py] = 1;
    return px != 500 || py;
}

int main() {
    freopen("day14.txt", "r", stdin);
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> vec = lib::split(line, " -> ");
            int lx, ly, first = true;
            for (const std::string & str: vec) {
                auto [X, _, Y] = lib::partition(str, ",");
                int x = std::stoi(X), y = std::stoi(Y);
                if (!first) {
                    if (x == lx) {
                        if (y < ly) for (int j = y; j <= ly; ++j) map[x][j] = 1;
                        else for (int j = ly; j <= y; ++j) map[x][j] = 1;
                    } else {
                        if (x < lx) for (int i = x; i <= lx; ++i) map[i][y] = 1;
                        else for (int i = lx; i <= x; ++i) map[i][y] = 1;
                    }
                }
                mh = std::max(y, mh);
                first = false; lx = x; ly = y;
            }
        }
    }
    int c = 0;
    while (fall_sand()) ++c;
    std::cout << c + 1 << std::endl;
    return 0;
}