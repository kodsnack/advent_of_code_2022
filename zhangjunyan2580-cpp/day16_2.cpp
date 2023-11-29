#include <iostream>
#include "pystrlib.hpp"
#include <unordered_map>
#include <string>
#include <cstring>

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
order<int> ints;

int dp[27][65536][16], dp2[27][65536][16], a[100][100], val[100], n, m, ans;

inline void upd(int S, int t, int i, int v) {
    if (v > dp[t][S][i]) dp[t][S][i] = v;
}

inline void upd2(int S, int t, int i, int v) {
    if (v > dp2[t][S][i]) dp2[t][S][i] = v;
    if (v > ans) ans = v;
}

int main() {
    std::memset(a, 0x3f, sizeof(a));
    std::string line;
    while (std::getline(std::cin, line)) {
        std::vector<std::string> tokens = lib::split(lib::strip(line), " ");
        std::string u = tokens[1]; int i = strs(u);
        val[i] = std::stoi(tokens[4].substr(5, tokens[4].size() - 6));
        if (val[i] || tokens[1] == "AA") ints(i), ++m;
        for (unsigned j = 9; j < tokens.size(); ++j) {
            if (tokens[j].back() == ',') tokens[j].pop_back();
            a[i][strs(tokens[j])] = 1;
        }
        ++n;
    }
    for (int i = 0; i < n; ++i) a[i][i] = 0;
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (a[i][k] + a[k][j] < a[i][j])
                    a[i][j] = a[i][k] + a[k][j];
    std::memset(dp, 0xc0, sizeof(dp));
    int st = ints(strs("AA"));
    dp[0][0][st] = 0;
    int mS = 1 << m;
    for (int t = 0; t < 26; ++t)
        for (int S = 0; S < mS; ++S)
            for (int i = 0; i < m; ++i) {
                int v = dp[t][S][i];
                if (!((S >> i) & 1)) upd(S | (1 << i), t + 1, i, v + (25 - t) * val[ints[i]]);
                for (int j = 0; j < m; ++j)
                    if (i != j && t + a[ints[i]][ints[j]] <= 26) upd(S, t + a[ints[i]][ints[j]], j, v);
            }
    std::memset(dp2, 0xc0, sizeof(dp2));
    for (int S = 0; S < mS; ++S)
        for (int t = 0; t < 26; ++t)
            for (int i = 0; i < m; ++i)
                if (dp[t][S][i] > dp2[0][S][st]) dp2[0][S][st] = dp[t][S][i];
    for (int t = 0; t < 26; ++t)
        for (int S = 0; S < mS; ++S)
            for (int i = 0; i < m; ++i) {
                int v = dp2[t][S][i];
                if (!((S >> i) & 1)) upd2(S | (1 << i), t + 1, i, v + (25 - t) * val[ints[i]]);
                for (int j = 0; j < m; ++j)
                    if (i != j && t + a[ints[i]][ints[j]] <= 26) upd2(S, t + a[ints[i]][ints[j]], j, v);
            }
    std::cout << ans << std::endl;
    return 0;
}