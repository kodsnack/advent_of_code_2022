#include <iostream>
#include <string>

template<typename _Tp, int size>
struct array {
    _Tp arr[2 * size + 1];
    _Tp& operator[](int x) { return arr[x + size]; }
    const _Tp& operator[](int x) const { return arr[x + size]; }
};

array< array<bool, 100>, 100 > arr, nw;
array< array<int, 100>, 100 > nxt;
int n, m;

constexpr int dx[4][3] = { { -1, -1, -1 }, {  1,  1,  1 }, { -1,  0,  1 }, { -1,  0,  1 } },
              dy[4][3] = { { -1,  0,  1 }, { -1,  0,  1 }, { -1, -1, -1 }, {  1,  1,  1 } },
              px[8] = { -1, -1, -1, 0,  1,  1,  1,  0 },
              py[8] = { -1,  0,  1, 1,  1,  0, -1, -1 };

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        m = line.size();
        for (int i = 0; i < m; ++i) arr[n][i] = line[i] == '#';
        ++n;
    }
    for (int t = 0; t < 10; ++t) {
        for (int i = -99; i <= 99; ++i)
            for (int j = -99; j <= 99; ++j)
                if (arr[i][j]) {
                    bool k = false;
                    for (int c = 0; c < 8; ++c)
                        if (arr[i + px[c]][j + py[c]]) { k = true; break; }
                    if (k) {
                        for (int c = t; c < t + 4; ++c) {
                            int p = c & 3;
                            if (!arr[i + dx[p][0]][j + dy[p][0]] && !arr[i + dx[p][1]][j + dy[p][1]] && !arr[i + dx[p][2]][j + dy[p][2]]) {
                                ++nxt[i + dx[p][1]][j + dy[p][1]];
                                break;
                            }
                        }
                    }
                }
        for (int i = -99; i <= 99; ++i)
            for (int j = -99; j <= 99; ++j)
                if (arr[i][j]) {
                    bool k = false;
                    for (int c = 0; c < 8; ++c)
                        if (arr[i + px[c]][j + py[c]]) { k = true; break; }
                    if (k) {
                        bool f = 0;
                        for (int c = t; c < t + 4; ++c) {
                            int p = c & 3;
                            if (!arr[i + dx[p][0]][j + dy[p][0]] && !arr[i + dx[p][1]][j + dy[p][1]] && !arr[i + dx[p][2]][j + dy[p][2]]) {
                                if (nxt[i + dx[p][1]][j + dy[p][1]] == 1) nw[i + dx[p][1]][j + dy[p][1]] = 1;
                                else nw[i][j] = 1;
                                f = 1;
                                break;
                            }
                        }
                        if (!f) nw[i][j] = 1;
                    } else nw[i][j] = 1;
                }
        for (int i = -100; i <= 100; ++i)
            for (int j = -100; j <= 100; ++j)
                arr[i][j] = nw[i][j], nw[i][j] = 0, nxt[i][j] = 0;
    }
    int u = 100, d = -100, l = 100, r = -100, k = 0;
    for (int i = -100; i <= 100; ++i)
        for (int j = -100; j <= 100; ++j)
            if (arr[i][j]) {
                if (i < u) u = i;
                if (i > d) d = i;
                if (j < l) l = j;
                if (j > r) r = j;
                ++k;
            }
    std::cout << (d - u + 1) * (r - l + 1) - k << std::endl;
    return 0;
}