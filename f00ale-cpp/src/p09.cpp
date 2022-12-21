#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p09(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    std::vector<std::tuple<char, int>> moves;
    {
        int num = 0;
        bool havenum = false;
        char M = 0;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else if (c >= 'A' && c <= 'Z') {
                M = c;
            } else if (c == '\n') {
                if (havenum && M) {
                    moves.emplace_back(M, num);
                }
                M = 0;
                havenum = false;
                num = 0;
            }
        }

    }

    for (auto p: {1, 2}) {
        std::vector<std::pair<int, int>> pos(p == 1 ? 2 : 10);
        std::set<std::pair<int, int>> tpos;
        tpos.insert(pos.back());

        for (auto [d, m]: moves) {
            for (int s = 0; s < m; s++) {
                {
                    auto &[hx, hy] = pos[0];
                    switch (d) {
                        case 'U':
                            hy++;
                            break;
                        case 'D':
                            hy--;
                            break;
                        case 'R':
                            hx++;
                            break;
                        case 'L':
                            hx--;
                            break;
                        default:
                            std::cout << d << '\n';
                            break;
                    }
                }
                for (size_t i = 1; i < pos.size(); i++) {
                    auto &[px, py] = pos[i - 1];
                    auto &[nx, ny] = pos[i];
                    // update nx,y to follow px,y
                    if(abs(px-nx) > 1 || abs(py-ny) > 1) {
                        if(px==nx) ny += (ny<py) ? 1 : -1;
                        else if(py==ny) nx += (nx<px) ? 1 : -1;
                        else {
                            ny += ny < py ? 1 : -1;
                            nx += nx < px ? 1 : -1;
                        }
                    }
                }
                tpos.insert(pos.back());
            }
        }
        (p == 1 ? ans1 : ans2) = tpos.size();
    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
