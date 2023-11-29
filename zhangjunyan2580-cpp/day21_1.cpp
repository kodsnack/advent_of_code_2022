#include <iostream>
#include "pystrlib.hpp"
#include <unordered_map>
#include <vector>

template<typename _Key>
struct order {
    
    std::unordered_map<_Key, int> to;
    std::vector<_Key> from;
    
    int operator()(const _Key &str) {
        if (to.count(str)) return to[str];
        to[str] = from.size(); from.push_back(str);
        return from.size() - 1;
    }

    _Key operator[](int index) { return from[index]; }

};

order<std::string> strs;

int l[5005], r[5005];
long long v[5005];
bool f[5005];
char t[5005];

long long value(int k) {
    if (!f[k]) {
        long long lv = value(l[k]), rv = value(r[k]);
        switch (t[k]) {
            case '+': v[k] = lv + rv; break;
            case '-': v[k] = lv - rv; break;
            case '*': v[k] = lv * rv; break;
            case '/': v[k] = lv / rv; break;
        }
        f[k] = 1;
    }
    return v[k];
}

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::vector<std::string> tokens = lib::split(line, " ");
        int k = strs(tokens[0].substr(0, tokens[0].size() - 1));
        if (tokens.size() == 4u) l[k] = strs(tokens[1]), r[k] = strs(tokens[3]), t[k] = tokens[2][0];
        else v[k] = std::stoi(tokens[1]), f[k] = 1;
    }
    std::cout << value(strs("root")) << std::endl;
    return 0;
}