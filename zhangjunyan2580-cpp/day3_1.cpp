#include <iostream>
#include <vector>

int ans;

inline int priority(char ch) { return isupper(ch) ? (ch - 'A' + 27) : (ch - 'a' + 1); }

int main() {
    {
        std::string line;
        while (std::cin >> line) {
            std::vector<int> sl(53), sr(53);
            int v = line.size() >> 1;
            for (int i = 0; i < v; ++i) ++sl[priority(line[i])];
            for (int i = v; i < v + v; ++i) ++sr[priority(line[i])];
            for (int i = 1; i <= 52; ++i) if (sl[i] && sr[i]) { ans += i; break; }
        }
    }
    std::cout << ans << std::endl;
    return 0;
}