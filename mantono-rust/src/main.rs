mod day1;
mod day2;
mod day3;
mod day4;

fn main() {
    let answer: String = aoc::run::<day4::Aoc>().unwrap();
    println!("Answer: {}", answer);
}
