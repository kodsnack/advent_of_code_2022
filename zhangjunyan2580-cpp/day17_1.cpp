#include <iostream>
#include <set>
#include <utility>

std::set< std::pair<int, int> > S;

const std::set< std::pair<int, int> > blocks[5] = {
    { { 0, 0 }, { 0, 1 }, { 0, 2 }, { 0, 3 } },
    { { 0, 1 }, { 1, 0 }, { 1, 1 }, { 1, 2 }, { 2, 1 } },
    { { 0, 0 }, { 0, 1 }, { 0, 2 }, { 1, 2 }, { 2, 2 } },
    { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 3, 0 } },
    { { 0, 0 }, { 0, 1 }, { 1, 0 }, { 1, 1 } }
};

inline bool check_collision(int x, int y, const std::set< std::pair<int, int> > &block) {
    for (const auto [dx, dy] : block)
        if (y + dy < 0 || y + dy > 6 || x + dx < 0 || S.count(std::make_pair(x + dx, y + dy)))
            return 1;
    return 0;
}
inline void add_block(int x, int y, const std::set< std::pair<int, int> > &block) {
    for (const auto [dx, dy] : block) S.emplace(x + dx, y + dy);
}

std::string str;

int main() {
    std::cin >> str;
    for (int i = 0, j = 0; i < 2022; ++i) {
        int x = S.empty() ? 3 : (std::prev(S.end())->first + 4), y = 2;
        while (1) {
            if (str[j % str.size()] == '<') {
                if (!check_collision(x, y - 1, blocks[i % 5]))
                    --y;
            } else {
                if (!check_collision(x, y + 1, blocks[i % 5]))
                    ++y;
            }
            ++j;
            if (check_collision(x - 1, y, blocks[i % 5])) {
                add_block(x, y, blocks[i % 5]);
                break;
            }
            --x;
        }
        int v = std::prev(S.end())->first + 1;
        std::cout << v << std::endl;
    }
    std::cout << std::prev(S.end())->first + 1 << std::endl;
    return 0;
}