#include <iostream>
#include "pystrlib.hpp"
#include <set>
#include <tuple>
#include <vector>
#include <queue>

std::set< std::tuple<int, int, int> > S, S2;
std::queue< std::tuple<int, int, int> > Q;
int n;

constexpr int dx[6] = { -1, 1, 0, 0, 0, 0 }, dy[6] = { 0, 0, -1, 1, 0, 0 }, dz[6] = { 0, 0, 0, 0, -1, 1 };

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::vector<std::string> tokens = lib::split(line, ",");
        S.emplace(std::stoi(tokens[0]), std::stoi(tokens[1]), std::stoi(tokens[2]));
    }
    Q.emplace(-1, -1, -1);
    S2.emplace(-1, -1, -1);
    while (Q.size()) {
        auto [x, y, z] = Q.front(); Q.pop();
        for (int i = 0; i < 6; ++i) {
            int nx = x + dx[i], ny = y + dy[i], nz = z + dz[i];
            std::tuple<int, int, int> np = std::make_tuple(nx, ny, nz);
            if (nx < -1 || nx > 25 || ny < -1 || ny > 25 || nz < -1 || nz > 25 || S.count(np) || S2.count(np)) continue;
            S2.insert(np); Q.push(np);
        }
    }
    for (auto [x, y, z] : S2)
        for (int i = 0; i < 6; ++i) {
            int nx = x + dx[i], ny = y + dy[i], nz = z + dz[i];
            n += nx >= -1 && nx <= 25 && ny >= -1 && ny <= 25 && nz >= -1 && nz <= 25 && !S2.count(std::make_tuple(nx, ny, nz));
        }
    std::cout << n << std::endl;
    return 0;
}