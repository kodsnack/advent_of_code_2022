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
	stacks := make(map[int][]string)
	p2 := make(map[int][]string)

	parts := strings.Split(input, "\n\n")
	for _, row := range strings.Split(parts[0], "\n") {
		for offset, ch := range row {
			if ch > 'A' && ch <= 'Z' {
				stack := offset/4 + 1
				stacks[stack] = append(stacks[stack], string(ch))
			}
		}
	}
	for k := 1; k <= len(stacks); k++ {
		stacks[k] = reverse(stacks[k])
		s := make([]string, len(stacks[k]))
		copy(s, stacks[k])
		p2[k] = s
	}

	for _, row := range strings.Split(parts[1], "\n") {
		args := strings.Split(row, " ")
		moves := atoi(args[1])
		from := atoi(args[3])
		to := atoi(args[5])

		// part 1
		for i := 0; i < moves; i++ {
			stacks[to] = append(stacks[to], stacks[from][len(stacks[from])-1])
			stacks[from] = stacks[from][:len(stacks[from])-1]
		}

		// part 2
		p2[to] = append(p2[to], p2[from][len(p2[from])-moves:]...)
		p2[from] = p2[from][:len(p2[from])-moves]
	}

	for k := 1; k <= len(stacks); k++ {
		fmt.Print(stacks[k][len(stacks[k])-1])
	}
	fmt.Println()
	for k := 1; k <= len(p2); k++ {
		fmt.Print(p2[k][len(p2[k])-1])
	}
}

func reverse(a []string) []string {
	for i := len(a)/2 - 1; i >= 0; i-- {
		opp := len(a) - 1 - i
		a[i], a[opp] = a[opp], a[i]
	}
	return a
}

func atoi(s string) int {
	num, _ := strconv.Atoi(s)
	return num
}
