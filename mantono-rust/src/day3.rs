use std::{collections::HashSet, str::FromStr};

use aoc::Solver;

pub struct Aoc;

impl Solver for Aoc {
    type Item = Rucksack;

    fn solve_one(inputs: &[Self::Item]) -> String {
        for ele in inputs {
            println!("{}", ele.priority())
        }
        String::from("x")
    }
}

#[derive(Debug)]
pub struct Rucksack(Vec<u8>);

impl Rucksack {
    fn priority(&self) -> u8 {
        let i: u8 = self.intersection();
        match i {
            // A..=Z
            65..=90 => i - 38,
            // a..=z
            97..=122 => i - 96,
            _ => panic!("Invalid byte {}", i),
        }
    }

    fn first(&self) -> &[u8] {
        let div: usize = self.0.len() / 2;
        &self.0[0..div]
    }

    fn second(&self) -> &[u8] {
        let div: usize = self.0.len() / 2;
        &self.0[div..]
    }

    fn intersection(&self) -> u8 {
        let s0: HashSet<u8> = self.first().into_iter().map(|c| c.clone()).collect();
        let s1: HashSet<u8> = self.second().into_iter().map(|c| c.clone()).collect();
        s0.intersection(&s1)
            .take(1)
            .map(|c| c.clone())
            .collect::<Vec<u8>>()
            .first()
            .expect(&format!(
                "Should be exactly one element in intersection, was zero: {:?}, {:?}",
                s0, s1
            ))
            .clone()
    }
}

impl FromStr for Rucksack {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Rucksack(s.as_bytes().into()))
    }
}
