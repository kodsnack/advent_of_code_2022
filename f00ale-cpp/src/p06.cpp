#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p06(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;
    std::string data;
    data.reserve(input.size());

    {
        for (const auto c: input) {
            if (c >= 'a' && c <= 'z') {
                data.push_back(c);
            }
        }

    }

    for(auto p : {1, 2}) {
        const size_t N = p == 1 ? 4 : 14;
        for (size_t i = 0; i < data.size() - N; i++) {
            bool nope = false;
            int set = 0;
            for (size_t k = 0; k < N; k++) {
                auto mask = (1 << (data[i+k]-'a'));
                if(set & mask) {
                    nope = true;
                    break;
                }
                set |= mask;
            }
            if (!nope) {
                (p == 1 ? ans1 : ans2) = static_cast<int>(i + N);
                break;
            }
        }
    }
    return {std::to_string(ans1), std::to_string(ans2)};
}
