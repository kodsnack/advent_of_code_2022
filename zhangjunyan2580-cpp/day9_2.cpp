#include <iostream>
#include <set>

int x[10], y[10];

std::set< std::pair<int, int> > V;

constexpr int dx[4] = { -1, 0, 1, 0 }, dy[4] = { 0, 1, 0, -1 };

inline int get_dir(char c) {
    switch (c) {
        case 'U': return 0;
        case 'R': return 1;
        case 'D': return 2;
        case 'L': return 3;
    }
    return -1;
}

void update(int i) {
    if (x[i] == x[i - 1] - 2) {
        x[i] = x[i - 1] - 1;
        if (y[i] == y[i - 1] + 2) y[i] = y[i - 1] + 1;
        else if (y[i] == y[i - 1] - 2) y[i] = y[i - 1] - 1;
        else y[i] = y[i - 1];
    }
    if (x[i] == x[i - 1] + 2) {
        x[i] = x[i - 1] + 1;
        if (y[i] == y[i - 1] + 2) y[i] = y[i - 1] + 1;
        else if (y[i] == y[i - 1] - 2) y[i] = y[i - 1] - 1;
        else y[i] = y[i - 1];
    }
    if (y[i] == y[i - 1] - 2) {
        y[i] = y[i - 1] - 1;
        if (x[i] == x[i - 1] + 2) x[i] = x[i - 1] + 1;
        else if (x[i] == x[i - 1] - 2) x[i] = x[i - 1] - 1;
        else x[i] = x[i - 1];
    }
    if (y[i] == y[i - 1] + 2) {
        y[i] = y[i - 1] + 1;
        if (x[i] == x[i - 1] + 2) x[i] = x[i - 1] + 1;
        else if (x[i] == x[i - 1] - 2) x[i] = x[i - 1] - 1;
        else x[i] = x[i - 1];
    }
}

int main() {
    freopen("day9.txt", "r", stdin);
    {
        std::string op; int st;
        V.emplace(0, 0);
        while (std::cin >> op >> st) {
            int k = get_dir(op[0]);
            for (; st; --st) {
                x[0] += dx[k]; y[0] += dy[k];
                for (int i = 1; i < 10; ++i) update(i);
                V.emplace(x[9], y[9]);
            }
        }
    }
    std::cout << V.size() << std::endl;
    return 0;
}