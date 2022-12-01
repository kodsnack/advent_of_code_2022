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

	var max int
	var cals []int

	for _, elf := range strings.Split(input, "\n\n") {
		var sum int
		for _, row := range strings.Split(elf, "\n") {
			num, _ := strconv.Atoi(row)
			sum += num
		}
		if sum > max {
			max = sum
		}
		cals = append(cals, sum)
	}

	fmt.Println(max)
	sort.Sort(sort.Reverse(sort.IntSlice(cals)))
	fmt.Println(cals[0] + cals[1] + cals[2])
}
