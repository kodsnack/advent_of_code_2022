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
		if strings.Contains(w, "+") {
			parts := strings.Split(w, " + ")
			return solve(parts[0]) + solve(parts[1])
		}
		if strings.Contains(w, "-") {
			parts := strings.Split(w, " - ")
			return solve(parts[0]) - solve(parts[1])
		}
		if strings.Contains(w, "*") {
			parts := strings.Split(w, " * ")
			return solve(parts[0]) * solve(parts[1])
		}
		if strings.Contains(w, "/") {
			parts := strings.Split(w, " / ")
			return solve(parts[0]) / solve(parts[1])
		}
		r, _ := strconv.Atoi(w)
		return r
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
		if strings.Contains(w, "+") {
			parts := strings.Split(w, " + ")
			return solve(parts[0], n) + solve(parts[1], n)
		}
		if strings.Contains(w, "-") {
			parts := strings.Split(w, " - ")
			return solve(parts[0], n) - solve(parts[1], n)
		}
		if strings.Contains(w, "*") {
			parts := strings.Split(w, " * ")
			return solve(parts[0], n) * solve(parts[1], n)
		}
		if strings.Contains(w, "/") {
			parts := strings.Split(w, " / ")
			return solve(parts[0], n) / solve(parts[1], n)
		}
		r, _ := strconv.Atoi(w)
		return r
	}

	b := solve("tjtt", 0)
	// lol manual bisection
	for n := 3330805240000; ; n += 1 {
		a := solve("bjgs", n)
		if a == b {
			return n
		}
	}
}
