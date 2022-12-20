#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p01(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;
    std::vector<int> top;
    {
        int num = 0;
        bool havenum = false;
        char last = 0;
        int sum = 0;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                if(last == '\n') {
                    top.push_back(sum);
                    sum = 0;
                }
                sum += num;
                havenum = false;
                num = 0;
            }
            last = c;
        }
    }

    std::sort(top.begin(), top.end(), std::greater<>());
    ans1 = top[0];
    for(int i = 0; i < 3; i++)
    {
        ans2 += top[i];
    }
    
    return {std::to_string(ans1), std::to_string(ans2)};
}
