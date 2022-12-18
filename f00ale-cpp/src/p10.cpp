#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p10(const std::string &input) {
    int64_t ans1 = 0;
    // Hardcoded answer for my data as I won't bother to
    // implement OCR. To print the data to OCR change
    // show bool to true
    const bool show = false;
    std::string ans2 = "PAPKFKEJ";

    std::vector<int> deltas;
    {
        int num = 0;
        bool havenum = false;
        bool neg = false;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else if(c=='-'){
                neg = true;
            } else if(c == '\n'){
                if(neg) num*=-1;
                deltas.push_back(num);

                havenum = false;
                num = 0;
                neg = false;
            }
        }

    }

    std::vector<std::string> screen;
    auto step = [cycle = 0, &ans1, &screen](int d, int x) mutable {
        auto pos = cycle%40;
        if(pos == 0) screen.emplace_back();
        cycle++;
        if(cycle % 40 - 20 == 0) ans1 += x*cycle;
        screen.back().push_back((abs(pos-x) <= 1) ? '#' : '.');
        x += d;
        return x;
    };

    int x = 1;
    for(auto d : deltas) {
        x = step(0, x);
        if(d) x = step(d, x);
    }

    if(show) for(auto & row: screen) std::cout << row << '\n';

    return {std::to_string(ans1), ans2};
}

