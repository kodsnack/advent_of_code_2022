package main

import (
	_ "embed"
	"fmt"
	"math"
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

	var solve func(str string) float64
	solve = func(str string) float64 {
		w := words[str]
		p := strings.Split(w, " ")
		if len(p) == 1 {
			r, _ := strconv.Atoi(w)
			return float64(r)
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

	fmt.Println(int64(solve("root")))

	var min = 0
	var max = math.MaxInt64

	lr := strings.Split(words["root"], " ")

	for min < max {
		mid := (min + max) / 2
		words["humn"] = fmt.Sprintf("%d", mid)
		a := solve(lr[0])
		b := solve(lr[2])
		if int(a) == int(b) {
			fmt.Println(mid)
			return
		}
		if a > b {
			min = mid + 1
		} else {
			max = mid
		}
	}
}
