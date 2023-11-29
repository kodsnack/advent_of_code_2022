#include <iostream>
#include <queue>
#include <tuple>
#include <bitset>

int n, m, p;
bool r[150][150], l[150][150], u[150][150], d[150][150];
std::bitset<20000> vis[150][150];
std::queue< std::tuple<int, int, int> > Q;

constexpr int dx[5] = { -1, 0, 1, 0, 0 }, dy[5] = { 0, -1, 0, 1, 0 };

inline bool blizzard(int t, int x, int y) { return 0 <= x && x < n && (d[((x - t) % n + n) % n][y] || u[(x + t) % n][y] || r[x][((y - t) % m + m) % m] || l[x][(y + t) % m]); }
inline bool within(int x, int y) { return (0 <= x && x < n && 0 <= y && y < m) || (x == -1 && y == 0) || (x == n && y == m - 1); }

int main() {
    std::string line;
    std::cin >> line;
    while (1) {
        std::cin >> line;
        if (line[1] == '#') break;
        m = line.size() - 2;
        for (int i = 0; i < m; ++i)
            switch (line[i + 1]) {
                case '>': r[n][i] = 1; break;
                case '<': l[n][i] = 1; break;
                case 'v': d[n][i] = 1; break;
                case '^': u[n][i] = 1; break;
            }
        ++n;
    }
    p = n * m;
    Q.emplace(1, -1, 0);
    while (!Q.empty()) {
        auto [t, x, y] = Q.front(); Q.pop(); int k = t % p;
        if (x == n && y == m - 1) { std::cout << t - 1 << std::endl; break; }
        for (int d = 0; d < 5; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (within(nx, ny) && !(nx == -1 ? (ny == 0 && d != 4) : vis[nx][ny][k]) && !blizzard(t, nx, ny)) {
                Q.emplace(t + 1, nx, ny);
                if (nx != -1) vis[nx][ny][k] = 1;
            }
        }
    }
    return 0;
}