#include <iostream>
#include <set>

int x1, y1, x2, y2;

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

int main() {
    {
        std::string op; int st;
        V.emplace(0, 0);
        while (std::cin >> op >> st) {
            int k = get_dir(op[0]);
            for (; st; --st) {
                x1 += dx[k]; y1 += dy[k];
                if ((k & 1) && (y1 - 2 * dy[k]) == y2) y2 = y1 - dy[k], x2 = x1;
                else if (!(k & 1) && (x1 - 2 * dx[k]) == x2) x2 = x1 - dx[k], y2 = y1;
                V.emplace(x2, y2);
            }
        }
    }
    std::cout << V.size() << std::endl;
    return 0;
}