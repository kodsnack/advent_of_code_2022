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

	for i := range input {
		s := make(map[byte]bool)
		for j := 0; j < 4; j++ {
			s[input[i+j]] = true
		}
		if len(s) == 4 {
			fmt.Println(i + 4)
			break
		}
	}

	for i := range input {
		s := make(map[byte]bool)
		for j := 0; j < 14; j++ {
			s[input[i+j]] = true
		}
		if len(s) == 14 {
			fmt.Println(i + 14)
			break
		}
	}
}
