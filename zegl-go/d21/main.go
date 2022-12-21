package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)

	words := make(map[string]string)

	for _, row := range strings.Split(input, "\n") {
		parts := strings.Split(row, ": ")
		words[parts[0]] = parts[1]
	}

	fmt.Println(part1(words))
	fmt.Println(part2(words))
}

func part1(words map[string]string) int {
	var solve func(str string) int
	solve = func(str string) int {
		w := words[str]
		p := strings.Split(w, " ")
		if len(p) == 1 {
			r, _ := strconv.Atoi(w)
			return r
		}
		switch p[1] {
		case "+":
			return solve(p[0]) + solve(p[2])
		case "-":
			return solve(p[0]) - solve(p[2])
		case "*":
			return solve(p[0]) * solve(p[2])
		case "/":
			return solve(p[0]) / solve(p[2])
		default:
			panic("unknown operator")
		}
	}

	return solve("root")
}

func part2(words map[string]string) int {
	var solve func(str string, n int) int
	solve = func(str string, n int) int {
		if str == "humn" {
			return n
		}
		w := words[str]
		p := strings.Split(w, " ")
		if len(p) == 1 {
			r, _ := strconv.Atoi(w)
			return r
		}
		switch p[1] {
		case "+":
			return solve(p[0], n) + solve(p[2], n)
		case "-":
			return solve(p[0], n) - solve(p[2], n)
		case "*":
			return solve(p[0], n) * solve(p[2], n)
		case "/":
			return solve(p[0], n) / solve(p[2], n)
		default:
			panic("unknown operator")
		}
	}

	min := 0
	max := 10_000_000_000_000
	var found int

	lr := strings.Split(words["root"], " ")

	for min < max {
		mid := (min + max) / 2
		a := solve(lr[0], mid)
		b := solve(lr[2], mid)
		if a == b {
			found = mid
			break
		}
		if a > b {
			min = mid + 1
		} else {
			max = mid
		}
	}

	for i := found - 10000; i <= found; i++ {
		a := solve(lr[0], i)
		b := solve(lr[2], i)
		if a == b {
			return i
		}
	}

	return -1
}
