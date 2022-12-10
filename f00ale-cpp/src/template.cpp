#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> pXX(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    {
        int num = 0;
        bool havenum = false;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {

                havenum = false;
                num = 0;
            }
        }

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
