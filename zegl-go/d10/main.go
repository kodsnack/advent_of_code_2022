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
	rows := strings.Split(input, "\n")

	var res int
	var x int = 1
	var cycle, ins = 0, 0

	step := func() {
		if (cycle-20)%40 == 0 {
			res += x * cycle
		}

		col := ((cycle - 1) % 40)
		if x == col || x == col-1 || x == col+1 {
			fmt.Print("#")
		} else {
			fmt.Print(" ")
		}
		if col == 39 {
			fmt.Println()
		}
	}

	for cycle < 240 {
		cycle++
		row := rows[ins%len(rows)]
		ins++

		parts := strings.Split(row, " ")

		if parts[0] == "addx" {
			step()
			cycle++
			step()
			v, _ := strconv.Atoi(parts[1])
			x += v
		} else if parts[0] == "noop" {
			step()
		}
	}

	fmt.Println(res)
}
