#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p04(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    {
        int num = 0;
        bool havenum = false;
        std::vector<int> vt;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                vt.push_back(num);
                havenum = false;
                num = 0;
                if(c == '\n')
                {
                    if(vt.size() == 4) {
                        if((vt[0]>=vt[2] && vt[1] <= vt[3]) || (vt[0]<=vt[2] && vt[1] >= vt[3])) ans1++;

                        ans2++;
                        if((vt[0] < vt[2] && vt[1] < vt[2]) || (vt[0] > vt[3] && vt[1] > vt[3])) ans2--;

                    }

                    vt.clear();
                }
            }
        }

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
