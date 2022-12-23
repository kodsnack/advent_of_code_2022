#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

struct dir {
    size_t size = 0;
    dir *parent = nullptr;
    std::vector<std::unique_ptr<dir>> sub;
};

size_t calcsizes(dir * d) {
    for(auto && s : d->sub) {
        d->size += calcsizes(s.get());
    }
    return d->size;
}

int64_t find1(dir *d) {
    int64_t ret = 0;
    if(d->size <= 100000) ret += d->size;
    for(auto && s : d->sub) {
        ret += find1(s.get());
    }
    return ret;
}

int64_t find2(dir *d, size_t goal) {
    int64_t ret = std::numeric_limits<int64_t>::max();
    if(d->size >= goal) ret = d->size;
    for(auto && s : d->sub) {
        auto tmp = find2(s.get(), goal);
        if(tmp < ret) ret = tmp;
    }
    return ret;
}


std::tuple<std::string, std::string> p07(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    dir root;
    dir *cur = &root;
    {
        int num = 0;
        bool havenum = false;
        std::string s;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                if(c == '\n') {
                    if(!s.empty()) {
                        if(s.substr(0, 5) == "$ cd ") {
                            auto d = s.substr(5);
                            if(d == "/") {
                            } else if(d == "..") {
                                cur = cur->parent;
                            } else {
                                cur->sub.emplace_back(std::make_unique<dir>());
                                auto old = cur;
                                cur = cur->sub.back().get();
                                cur->parent = old;
                            }

                        }
                    }

                    if(havenum) {
                        cur->size += num;
                    }
                    havenum = false;
                    num = 0;
                    s.clear();
                } else {
                    s.push_back(c);
                }
            }
        }

    }

    calcsizes(&root);
    ans1 = find1(&root);

    auto tofree = 30000000 - (70000000 - root.size);

    ans2 = find2(&root, tofree);

    return {std::to_string(ans1), std::to_string(ans2)};
}
