#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p02(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    std::vector<std::string> v;

    {
        char a = 0, b = 0;

        for (const auto c: input) {
            if(c >= 'A' && c <= 'Z') {
                if(a) b = c;
                else a = c;
            } else if(c == '\n'){
                if(a && b) {
                    v.push_back(std::string{a,b});
                    a = b = 0;
                }
            }
        }
    }

    for(auto && s : v) {
        char a = s[0] - 'A';
        char b = s[1] - 'X';
        ans1 += 1+b;

        if(a == b) { ans1 += 3; }
        else {
            if(a == 0 && b == 1) { ans1 += 6; }
            else if(a == 1 && b == 2) { ans1 += 6; }
            else if(a == 2 && b == 0) { ans1 += 6; }
        }

        ans2 += 3*b;
        if(b == 0) {
            if(a == 0) { ans2 += 3; }
            if(a == 1) { ans2 += 1; }
            if(a == 2) { ans2 += 2; }
        } else if (b == 1) {
            ans2 += a+1;
        } else {  // b == 2
            if(a == 0) { ans2 += 2; }
            if(a == 1) { ans2 += 3; }
            if(a == 2) { ans2 += 1; }
        }

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
// 12734
// 13568

//13417
