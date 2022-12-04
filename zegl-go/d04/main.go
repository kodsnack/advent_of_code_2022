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

	var p1 int
	var p2 int

	for _, row := range strings.Split(input, "\n") {
		ranges := strings.Split(row, ",")

		f1, _ := strconv.Atoi(strings.Split(ranges[0], "-")[0])
		f2, _ := strconv.Atoi(strings.Split(ranges[0], "-")[1])
		s1, _ := strconv.Atoi(strings.Split(ranges[1], "-")[0])
		s2, _ := strconv.Atoi(strings.Split(ranges[1], "-")[1])

		if f1 >= s1 && f2 <= s2 {
			p1++
		} else if s1 >= f1 && s2 <= f2 {
			p1++
		} else if f1 >= s1 && f1 <= s2 {
			p2++
		} else if s1 >= f1 && s1 <= f2 {
			p2++
		}
	}

	fmt.Println(p1)
	fmt.Println(p1 + p2)
}
