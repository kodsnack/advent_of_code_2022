

public static class Day1 {
    public static void Solve() {
      List<int> calories = new List<int>() {0};
      int elfIndex = 0;
      foreach (string line in System.IO.File.ReadLines(@"day1-input.txt"))
      {  
            if(String.IsNullOrWhiteSpace(line)) {
                elfIndex += 1;
                calories.Add(0);
            }
            else {
                calories[elfIndex] += Int32.Parse(line);
            }
      }
      calories.Sort();
      int answer1 = calories[calories.Count - 1];
      int answer2 = calories.GetRange(calories.Count - 3, 3).Sum();
      Console.WriteLine("1. " + answer1 + " 2. " + answer2);   
    }
}