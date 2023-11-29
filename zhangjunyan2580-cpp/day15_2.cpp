#include <iostream>
#include <algorithm>
#include <vector>
#include "pystrlib.hpp"

std::vector< std::pair<int, int> > rg[4000005];

int n;

int main() {
    freopen("day15.txt", "r", stdin);
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> vec = lib::split(line, "=");
            int xs = std::stoi(vec[1]), ys = std::stoi(vec[2]), xb = std::stoi(vec[3]), yb = std::stoi(vec[4]);
            int dist = std::abs(ys - yb) + std::abs(xs - xb);
            for (int d = 0; d <= dist; ++d) {
                int y1 = ys - d, y2 = ys + d;
                if (y1 >= 0) rg[y1].emplace_back(xs - dist + d, xs + dist - d);
                if (y2 <= 4000000) rg[y2].emplace_back(xs - dist + d, xs + dist - d);
            }
        }
    }
    for (int y = 0; y <= 4000000; ++y) {
        auto &V = rg[y];
        std::sort(V.begin(), V.end());
        int lv = V[0].second;
        for (int i = 1; i < V.size(); ++i)
            if (V[i].first > lv + 1) { std::cout << (long long) (lv + 1) * 4000000 + y << std::endl; break; }
            else if (V[i].second > lv) lv = V[i].second;
    }
    return 0;
}