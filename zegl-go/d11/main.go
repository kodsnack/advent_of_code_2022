package main

import (
	_ "embed"
	"fmt"
	"sort"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)

	var monkeys []monkey

	for _, monkeystr := range strings.Split(input, "\n\n") {
		rows := strings.Split(monkeystr, "\n")
		for k, row := range rows {
			rows[k] = strings.TrimSpace(row)
		}
		m := monkey{
			items:   csvInts(strings.Split(rows[1], ": ")[1]),
			opop:    strings.Split(rows[2], " ")[4],
			opright: num(strings.Split(rows[2], " ")[5]),
			test:    num(strings.Split(rows[3], " ")[3]),
			iftrue:  num(strings.Split(rows[4], " ")[5]),
			iffalse: num(strings.Split(rows[5], " ")[5]),
		}

		fmt.Printf("%+v\n", m)
		monkeys = append(monkeys, m)
	}

	var lcm []int64
	for _, m := range monkeys {
		lcm = append(lcm, int64(m.test))
	}
	LCM := lowestCommonDenominator(lcm)

	fmt.Println(play(monkeys, 20, 0))
	fmt.Println(play(monkeys, 10000, LCM))
}

type monkey struct {
	items   []int64
	opop    string
	opright int
	test    int
	iftrue  int
	iffalse int
}

func play(monkeys []monkey, rounds int, LCM int64) int64 {
	inspections := make([]int64, len(monkeys))
	for r := 0; r < rounds; r++ {
		for i, m := range monkeys {
			for _, item := range m.items {
				inspections[i]++

				if m.opop == "*" {
					if m.opright == 0 {
						item = item * item
					} else {
						item *= int64(m.opright)
					}
				} else {
					item += int64(m.opright)
				}

				if LCM > 0 {
					item = item % LCM
				} else {
					item /= 3 // part 1
				}

				if item%int64(m.test) == 0 {
					monkeys[m.iftrue].items = append(monkeys[m.iftrue].items, item)
				} else {
					monkeys[m.iffalse].items = append(monkeys[m.iffalse].items, item)
				}
			}
			monkeys[i].items = []int64{}
		}
	}
	sortIntsDesc(inspections)
	return inspections[0] * inspections[1]
}

func num(s string) int {
	n, _ := strconv.Atoi(s)
	return n
}

func sortIntsDesc(n []int64) {
	sort.Slice(n, func(i, j int) bool {
		return n[i] > n[j]
	})
}

func lowestCommonDenominator(n []int64) int64 {
	res := n[0]
	for _, v := range n[1:] {
		res = lcm(res, v)
	}
	return res
}

func lcm(a, b int64) int64 {
	return a * b / gcd(a, b)
}

func gcd(a, b int64) int64 {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func csvInts(s string) []int64 {
	var res []int64
	s = strings.ReplaceAll(s, " ", "")
	for _, ss := range strings.Split(s, ",") {
		num, _ := strconv.Atoi(ss)
		res = append(res, int64(num))
	}
	return res
}
