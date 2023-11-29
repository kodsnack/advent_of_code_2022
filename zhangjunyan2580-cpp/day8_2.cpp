#include <iostream>
#include <algorithm>

int v[105][105];
std::string lines[105];

int n, m, ans;

constexpr int dx[4] = { 0, 1, 0, -1 }, dy[4] = { 1, 0, -1, 0 };

int main() {
    while (std::getline(std::cin, lines[n])) n++;
    m = lines[0].size();
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) v[i][j] = (lines[i - 1][j - 1] & 15) + 1;
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) {
            int s = 1;
            for (int d = 0; d < 4; ++d) {
                int x = i + dx[d], y = j + dy[d], c = 0;
                while (x && x <= n && y && y <= m) {
                    ++c;
                    if (v[i][j] <= v[x][y]) break;
                    x += dx[d]; y += dy[d];
                }
                s *= c;
            }
            if (s > ans) ans = s;
        }
    std::cout << ans << std::endl;
    return 0;
}