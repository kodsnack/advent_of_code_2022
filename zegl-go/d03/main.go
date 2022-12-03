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

	var sum int

	for _, row := range strings.Split(input, "\n") {
		chars := make(map[rune]bool)
		firstHalf := row[:len(row)/2]
		secondHalf := row[len(row)/2:]

		for _, c := range firstHalf {
			chars[c] = true
		}

		for _, c := range secondHalf {
			if chars[c] {
				if c >= 'a' && c <= 'z' {
					sum += int(c - 'a' + 1)
				} else if c >= 'A' && c <= 'Z' {
					sum += int(c - 'A' + 27)
				}
				break
			}
		}
	}

	fmt.Println(sum)

	sum = 0
	rows := strings.Split(input, "\n")
	for i := 0; i < len(rows); i += 3 {
		row1 := rows[i]
		row2 := rows[i+1]
		row3 := rows[i+2]

		chars1 := make(map[rune]bool)
		chars2 := make(map[rune]bool)

		for _, c := range row1 {
			chars1[c] = true
		}
		for _, c := range row2 {
			chars2[c] = true
		}

		for _, c := range row3 {
			if chars1[c] && chars2[c] {
				if c >= 'a' && c <= 'z' {
					sum += int(c - 'a' + 1)
				} else if c >= 'A' && c <= 'Z' {
					sum += int(c - 'A' + 27)
				}
				break
			}
		}
	}

	fmt.Println(sum)
}
