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

	var s int
	for _, row := range strings.Split(input, "\n") {
		var s2 int
		for p, c := range row {
			place := pow(5, int(len(row)-p-1))
			if c == '2' {
				s2 += place * 2
			} else if c == '1' {
				s2 += place * 1
			} else if c == '0' {
				s2 += place * 0
			} else if c == '-' {
				s2 += place * -1
			} else if c == '=' {
				s2 += place * -2
			}
		}
		s += s2
	}

	var res string
	for {
		if s == 0 {
			break
		}
		switch s % 5 {
		case 0:
			res = "0" + res
			s /= 5
		case 1:
			res = "1" + res
			s = (s - 1) / 5
		case 2:
			res = "2" + res
			s = (s - 2) / 5
		case 3:
			res = "=" + res
			s = (s + 2) / 5
		case 4:
			res = "-" + res
			s = (s + 1) / 5
		}
	}

	fmt.Println(res)
}

func pow(a, b int) int {
	res := int(1)
	for i := int(0); i < b; i++ {
		res *= a
	}
	return res
}
