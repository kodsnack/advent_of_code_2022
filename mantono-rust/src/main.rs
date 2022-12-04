mod day1;
mod day2;
mod day3;

fn main() {
    let answer: String = aoc::run::<day3::Aoc>().unwrap();
    println!("Answer: {}", answer);
}
