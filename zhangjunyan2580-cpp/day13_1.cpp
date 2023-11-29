#include <iostream>
#include <variant>
#include <vector>
#include <cctype>

struct node {

    int type;
    std::vector<node> sub;
    int val;

    explicit node(const std::vector<node> &v) : sub(v), type(0) {}
    explicit node(int v) : val(v), type(1) {}

    friend int compare_to(const node &, const node &);

};

int compare_to(const node &l, const node &r) {
    if (l.type && r.type) return (l.val < r.val) ? -1 : ((l.val == r.val) ? 0 : 1);
    if (!l.type && !r.type) {
        int i = 0;
        while (i < l.sub.size() && i < r.sub.size()) {
            int v = compare_to(l.sub[i], r.sub[i]);
            if (v) return v;
            ++i;
        }
        return (l.sub.size() < r.sub.size()) ? -1 : ((l.sub.size() == r.sub.size()) ? 0 : 1);
    }
    if (l.type && !r.type) {
        if (r.sub.empty()) return 1;
        int v = compare_to(node(l.val), r.sub[0]);
        if (v) return v;
        return (r.sub.size() == 1) ? 0 : -1;
    }
    if (l.sub.empty()) return -1;
    int v = compare_to(l.sub[0], node(r.val));
    if (v) return v;
    return (l.sub.size() == 1) ? 0 : 1;
}

node parse_string(const std::string &str, int &i) {
    if (std::isdigit(str[i])) {
        int num = 0;
        while (i < str.size() && std::isdigit(str[i])) num = num * 10 + (str[i++] & 15);
        return node(num);
    }
    std::vector<node> nodes; ++i;
    while (i < str.size()) {
        if (str[i] == ',') { ++i; continue; }
        if (str[i] == ']') { ++i; break; }
        nodes.push_back(parse_string(str, i));
    }
    return node(nodes);
}

int main() {
    freopen("day13.txt", "r", stdin);
    int ans = 0;
    {
        std::string line; int n = 0, i = 0;
        while (std::getline(std::cin, line)) {
            ++n;
            node n1 = parse_string(line, i); i = 0;
            std::getline(std::cin, line);
            node n2 = parse_string(line, i); i = 0;
            std::getline(std::cin, line);
            if (compare_to(n1, n2) == -1) ans += n;
        }
    }
    std::cout << ans << std::endl;
    return 0;
}