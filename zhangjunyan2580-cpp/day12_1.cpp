#include <iostream>
#include <cstring>
#include <queue>
#include <tuple>

char map[50][200];
int n, m;

std::queue< std::tuple<int, int, int> > Q;
int vis[50][200];
int sx, sy, ex, ey;

constexpr int dx[4] = { 0, 1, 0, -1 }, dy[4] = { 1, 0, -1, 0 };

int main() {
    freopen("day12.txt", "r", stdin);
    while (std::cin >> map[n]) ++n;
    m = std::strlen(map[0]);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            if (map[i][j] == 'S') sx = i, sy = j, map[i][j] = 'a';
            else if (map[i][j] == 'E') ex = i, ey = j, map[i][j] = 'z';
    vis[sx][sy] = 1; Q.emplace(sx, sy, 0);
    while (!Q.empty()) {
        auto [x, y, d] = Q.front(); Q.pop();
        if (x == ex && y == ey) { std::cout << d << std::endl; return 0; }
        for (int i = 0; i < 4; ++i) {
            int nx = x + dx[i], ny = y + dy[i];
            if (nx < 0 || ny < 0 || nx >= n || ny >= m || vis[nx][ny] || map[nx][ny] - map[x][y] > 1) continue;
            vis[nx][ny] = 1; Q.emplace(nx, ny, d + 1);
        }
    }
}