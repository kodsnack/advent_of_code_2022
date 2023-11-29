#include <iostream>
#include <vector>

int ans;

inline int priority(char ch) { return isupper(ch) ? (ch - 'A' + 27) : (ch - 'a' + 1); }

int main() {
    {
        std::string line, line2, line3;
        while (std::cin >> line >> line2 >> line3) {
            std::vector<int> s1(53), s2(53), s3(53);
            for (char c : line) ++s1[priority(c)];
            for (char c : line2) ++s2[priority(c)];
            for (char c : line3) ++s3[priority(c)];
            for (int i = 1; i <= 52; ++i) if (s1[i] && s2[i] && s3[i]) { ans += i; break; }
        }
    }
    std::cout << ans << std::endl;
    return 0;
}