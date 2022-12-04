use std::str::FromStr;

use aoc::Solver;

pub struct Aoc;

impl Solver for Aoc {
    type Item = Entry;

    fn solve_one(inputs: &[Self::Item]) -> String {
        let mut max: usize = 0;
        let mut current: usize = 0;
        for input in inputs {
            match input {
                Entry::Calories(n) => current += n,
                Entry::Divider => {
                    if current > max {
                        max = current
                    }
                    current = 0;
                }
            }
        }
        max.to_string()
    }

    fn solve_two(inputs: &[Self::Item]) -> String {
        let mut carried: Vec<usize> = Vec::with_capacity(256);
        let mut current: usize = 0;
        for input in inputs {
            match input {
                Entry::Calories(n) => current += n,
                Entry::Divider => {
                    carried.push(current);
                    current = 0;
                }
            }
        }
        carried.sort();
        carried.reverse();
        let sum: usize = carried.iter().take(3).sum();
        sum.to_string()
    }

    fn parse_input<T: Into<String>>(input: T) -> Vec<Self::Item> {
        input
            .into()
            .lines()
            .map(|line| line.trim())
            .map(|line| match Self::parse(line) {
                Ok(val) => val,
                Err(_) => panic!("Unable to parse line: '{}'", line),
            })
            .collect()
    }
}

#[derive(Debug)]
pub enum Entry {
    Calories(usize),
    Divider,
}

impl FromStr for Entry {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let s = s.trim();
        match s.len() {
            0 => Ok(Entry::Divider),
            _ => match s.parse::<usize>() {
                Ok(num) => Ok(Entry::Calories(num)),
                Err(_) => Err(format!("Invalid input {}", s)),
            },
        }
    }
}
