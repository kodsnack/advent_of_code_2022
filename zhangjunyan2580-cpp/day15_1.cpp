#include <iostream>
#include <algorithm>
#include "pystrlib.hpp"

std::pair<int, int> rg[30];

int yc = 2000000, n;

int main() {
    freopen("day15.txt", "r", stdin);
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> vec = lib::split(line, "=");
            int xs = std::stoi(vec[1]), ys = std::stoi(vec[2]), xb = std::stoi(vec[3]), yb = std::stoi(vec[4]);
            int dist = std::abs(ys - yb) + std::abs(xs - xb) - std::abs(ys - yc);
            if (dist >= 0) {
                rg[n] = std::make_pair(xs - dist, xs + dist);
                if (yb == yc) {
                    if (rg[n].first == xb) ++rg[n].first;
                    else --rg[n].second;
                    if (rg[n].first <= rg[n].second) ++n;
                } else ++n;
            }
        }
    }
    std::sort(rg, rg + n); int ans = 0;
    for (int i = 0, lv = 0xc0c0c0c0; i < n; ++i) {
        if (rg[i].first > lv) ans += rg[i].second - rg[i].first + 1, lv = rg[i].second;
        else if (rg[i].second > lv) ans += rg[i].second - lv, lv = rg[i].second;
    }
    std::cout << ans << std::endl;
    return 0;
}