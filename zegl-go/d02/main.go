package main

import (
	_ "embed"
	"fmt"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)
	var score int

	for _, row := range strings.Split(input, "\n") {
		a, b := row[0], row[2]
		if (b == 'X' && a == 'C') || (b == 'Y' && a == 'A') || (b == 'Z' && a == 'B') {
			score += 6
		} else if a-'A' == b-'X' {
			score += 3
		}
		score += int(b - 'X' + 1)
	}

	fmt.Println(score)

	score = 0
	for _, row := range strings.Split(input, "\n") {
		a, b := row[0], row[2]
		if b == 'X' {
			score += int(a-'A'+2)%3 + 1
		} else if b == 'Y' {
			score += int(a-'A'+1) + 3
		} else {
			score += int(a-'A'+1)%3 + 1 + 6
		}
	}

	fmt.Println(score)
}
