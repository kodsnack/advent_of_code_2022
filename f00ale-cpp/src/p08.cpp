#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p08(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;
    std::vector<std::vector<int>> map(1);

    {
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                map.back().push_back(c-'0');
            } else if(c == '\n') {
                map.emplace_back();
            }
        }
        while(map.back().empty()) {
            map.pop_back();
        }
    }

    auto vl = map;
    for(size_t r = 0; r < map.size(); r++) {
        int high = vl[r][0];
        for(size_t c = 1; c < vl[r].size(); c++) {
            if(high >= vl[r][c]) vl[r][c] = -1;
            else high = vl[r][c];
        }
    }

    auto vr = map;
    for(size_t r = 0; r < map.size(); r++) {
        int high = vr[r].back();
        for(size_t c = vr[r].size()-1; c > 0; c--) {
            if(high >= vr[r][c-1]) vr[r][c-1] = -1;
            else high = vr[r][c-1];
        }
    }

    auto vt = map;
    for(size_t c = 0; c < map[0].size(); c++) {
        int high = vt[0][c];
        for(size_t r = 1; r < map.size(); r++) {
            if(high >= vt[r][c]) vt[r][c] = -1;
            else high = vt[r][c];
        }
    }

    auto vb = map;
    for(size_t c = 0; c < map[0].size(); c++) {
        int high = vb[map.size()-1][c];
        for(size_t r = map.size()-1; r > 0; r--) {
            if(high >= vb[r-1][c]) vb[r-1][c] = -1;
            else high = vb[r-1][c];
        }
    }

    for(size_t r = 0; r < map.size(); r++) {
        for(size_t c = 0; c < map[r].size(); c++) {
            if(!(vl[r][c] < 0 && vr[r][c] < 0 && vt[r][c] < 0 && vb[r][c] < 0)) ans1++;
        }
    }

    for(size_t r = 1; r < map.size()-1; r++) {
        for (size_t c = 1; c < map[r].size()-1; c++) {
            int64_t score = 1;
            if(c > 0) {
                // look left
                int h = map[r][c];
                int64_t trees = 0;
                for(size_t cc = c; cc > 0; cc--) {
                    trees++;
                    if(h>map[r][cc-1]) {
                        //h = map[r][cc-1];
                    } else break;
                }
                score *= trees;
            }
            if(c < map[r].size()-1) {
                // look right
                int h = map[r][c];
                int64_t trees = 0;
                for(size_t cc = c; cc < map[r].size()-1; cc++) {
                    trees++;
                    auto tmp = map[r][cc+1];
                    if(h>tmp) {
                    } else break;
                }
                score *= trees;
            }
            if(r > 0) {
                // look up
                int h = map[r][c];
                int64_t trees = 0;
                for(size_t cr = r; cr > 0; cr--) {
                    trees++;
                    if(h>map[cr-1][c]) {
                        //h = map[cr-1][c];
                    } else break;
                }
                score *= trees;
            }
            if(r < map.size()-1) {
                // look down
                int h = map[r][c];
                int64_t trees = 0;
                for(size_t cr = r; cr < map.size()-1; cr++) {
                    trees++;
                    if(h>map[cr+1][c]) {
                    } else break;
                }
                score *= trees;
            }

            if(score > ans2) {
                ans2 = score;
            }
        }
    }


    return {std::to_string(ans1), std::to_string(ans2)};
}
