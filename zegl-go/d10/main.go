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

	var res int
	var x int = 1

	rows := strings.Split(input, "\n")

	i := 0
	ins := 0

	step := func() {
		i++
		if i == 20 || i == 60 || i == 100 || i == 140 || i == 180 || i == 220 {
			res += x * i
		}
	}

	pr := func() {
		if i%40 == 0 {
			fmt.Println("")
		}
		col := i % 40
		if x == col || x == col-1 || x == col-2 {
			fmt.Print("#")
		} else {
			fmt.Print(" ")
		}
	}

	pr()

	for i < 240 {
		row := rows[ins%len(rows)]
		ins++

		parts := strings.Split(row, " ")

		if parts[0] == "addx" {
			step()
			pr()

			step()
			pr()

			v, _ := strconv.Atoi(parts[1])
			x += v
		} else if parts[0] == "noop" {
			step()
			pr()
		}
	}

	fmt.Println()
	fmt.Println()
	fmt.Println(res)
}
