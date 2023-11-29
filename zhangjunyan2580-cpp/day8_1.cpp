#include <iostream>
#include <algorithm>

int v[105][105], mu[105][105], md[105][105], ml[105][105], mr[105][105];
std::string lines[105];

int n, m, ans;

int main() {
    while (std::getline(std::cin, lines[n])) n++;
    m = lines[0].size();
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) v[i][j] = (lines[i - 1][j - 1] & 15) + 1;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j)
            ml[i][j] = std::max(ml[i][j - 1], v[i][j]);
        for (int j = m; j; --j)
            mr[i][j] = std::max(mr[i][j + 1], v[i][j]);
    }
    for (int j = 1; j <= m; ++j) {
        for (int i = 1; i <= n; ++i)
            mu[i][j] = std::max(mu[i - 1][j], v[i][j]);
        for (int i = n; i; --i)
            md[i][j] = std::max(md[i + 1][j], v[i][j]);
    }
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j)
            ans += v[i][j] > mu[i - 1][j] || v[i][j] > md[i + 1][j] || v[i][j] > ml[i][j - 1] || v[i][j] > mr[i][j + 1];
    std::cout << ans << std::endl;
    return 0;
}