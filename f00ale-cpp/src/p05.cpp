#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>
#include <queue>

std::tuple<std::string, std::string> p05(const std::string &input) {
    std::string ans1, ans2;
    std::vector<std::tuple<int,int,int>> moves;
    std::vector<std::deque<char>> crates_in(10);
    {
        int num = 0;
        bool havenum = false;
        bool move = false;
        int col = 0;
        int n = 0;
        for (const auto c: input) {
            if(c >= 'A' && c <= 'Z') {
                crates_in[1 + (col-1)/4].push_back(c);
            } else if(c == 'm') {
                move = true;
            }
            else if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                if(havenum && move) {
                  if(n == 0) {
                      moves.emplace_back(num, 0, 0);
                  } else if(n == 1) {
                      std::get<1>(moves.back()) = num;
                  } else if(n == 2) {
                      std::get<2>(moves.back()) = num;
                  }
                  n++;
                }
                havenum = false;
                num = 0;

            }

            if(c == '\n') {
                col = 0;
                n = 0;
            } else { col++; }
        }
    }

    for(auto p : {1,2}) {
        auto crates = crates_in;
        for (auto [a, b, c]: moves) {
            std::deque<char> tmp;
            for (int i = 0; i < a; i++) {
                auto x = crates[b].front();
                crates[b].pop_front();
                if(p == 1) crates[c].push_front(x);
                else tmp.push_front(x);
            }
            for (auto x: tmp) {
                crates[c].push_front(x);
            }

        }
        for (int i = 0; i < 10; i++) {
            if (!crates[i].empty()) {
                auto x = crates[i].front();
                (p == 1 ? ans1 : ans2).push_back(x);
            }
        }
    }
    return {ans1, ans2};
}
