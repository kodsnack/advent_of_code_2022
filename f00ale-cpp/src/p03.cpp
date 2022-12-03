#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p03(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    std::vector<std::string> v;
    {
        std::string s;
        for (const auto c: input) {
            if((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                s.push_back(c);
            } else if(c == '\n') {
                if(!s.empty()) {
                    v.push_back(s);
                    s.clear();
                }
            }
        }

    }

    for(auto && s : v) {
        auto l = s.length();
        auto s1 = s.substr(0, l/2);
        auto s2 = s.substr(l/2);

        for(auto c : s1) {
            if(s2.find(c) != std::string::npos) {
                if(c >= 'a' && c <= 'z') {
                    ans1 += 1 + c - 'a';
                } else {
                    ans1 += 27 + c - 'A';
                }
                break;
            }
        }
    }

    for(size_t i = 0; i < v.size(); i+=3) {
        for(int j = 0; j < 3; j++) {
            std::sort(v[i+j].begin(), v[i+j].end());
        }

        std::string tmp, f;
        std::set_intersection(v[i].begin(), v[i].end(), v[i+1].begin(), v[i+1].end(), std::back_inserter(tmp));
        std::set_intersection(tmp.begin(), tmp.end(), v[i+2].begin(), v[i+2].end(), std::back_inserter(f));

        auto c = f[0];
        if(c >= 'a' && c <= 'z') {
            ans2 += 1 + c - 'a';
        } else {
            ans2 += 27 + c - 'A';
        }

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
