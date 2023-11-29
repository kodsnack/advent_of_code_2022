#include <iostream>
#include <algorithm>
#include <utility>

#define KEY 811589153

std::pair<int, int> a[5005];
int bk[20005], n;
std::pair<int, int> b[5005];

int main() {
    freopen("day20.txt", "r", stdin);
    while (std::cin >> a[n].first) ++n;
    for (int i = 0; i < n; ++i) a[i].second = ++bk[a[i].first + 10000], b[i] = a[i];
    for (int t = 0; t < 10; ++t) {
        for (int i = 0; i < n; ++i) {
            int k = 0;
            for (; b[k] != a[i]; ++k);
            int v = ((long long) a[i].first * KEY % (n - 1) + (n - 1)) % (n - 1);
            for (; v; --v) {
                int nk = k == n - 1 ? 0 : k + 1;
                std::swap(b[k], b[nk]);
                k = nk;
            }
        }
    }
    long long v;
    for (int i = 0; i < n; ++i)
        if (b[i].first == 0) {
            v = b[(i + 1000) % n].first + b[(i + 2000) % n].first + b[(i + 3000) % n].first;
            break;
        }
    std::cout << v * KEY << std::endl;
    return 0;
}