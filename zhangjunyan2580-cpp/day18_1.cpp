#include <iostream>
#include "pystrlib.hpp"
#include <set>
#include <tuple>
#include <vector>

std::set< std::tuple<int, int, int> > S;
int n;

constexpr int dx[6] = { -1, 1, 0, 0, 0, 0 }, dy[6] = { 0, 0, -1, 1, 0, 0 }, dz[6] = { 0, 0, 0, 0, -1, 1 };

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::vector<std::string> tokens = lib::split(line, ",");
        S.emplace(std::stoi(tokens[0]), std::stoi(tokens[1]), std::stoi(tokens[2]));
    }
    for (auto [x, y, z] : S)
        for (int i = 0; i < 6; ++i)
            n += !S.count(std::make_tuple(x + dx[i], y + dy[i], z + dz[i]));
    std::cout << n << std::endl;
    return 0;
}