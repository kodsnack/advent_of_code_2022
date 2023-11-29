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

int delta[10001], nxt[10001];

int main() {
    std::cin >> str;
    for (int i = 0, j = 0; i < 10000; ++i) {
        int st_h = S.empty() ? 0 : (std::prev(S.end())->first + 1);
        int x = st_h + 3, y = 2;
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
        delta[10000 - i] = v - st_h;
    }
    for (int i = 2, j = 0; i <= 10000; ++i) {
        while (j && delta[j + 1] != delta[i]) j = nxt[j];
        if (delta[j + 1] == delta[i]) nxt[i] = ++j;
    }
    int len = 10000, start = 0;
    for (int i = 10000; i; --i)
        if (i % (i - nxt[i]) == 0 && i / (i - nxt[i]) >= 4) {
            len = i - nxt[i];
            start = 10001 - i;
            break;
        }
    int loop_sum = 0, start_sum = 0, end_sum = 0, end_len = (1000000000001ll - start) % len;
    long long loop_cnt = (1000000000001ll - start) / len;
    for (int i = 1; i < start; ++i) start_sum += delta[10001 - i];
    for (int i = start; i < start + len; ++i) loop_sum += delta[10001 - i];
    for (int i = start; i < start + end_len; ++i) end_sum += delta[10001 - i];
    std::cout << loop_cnt * loop_sum + end_sum + start_sum << std::endl;
    return 0;
}