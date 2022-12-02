namespace adventofcode;

public class Day1 
{
    private static IEnumerable<string> ElfsData() 
    {
        var data = System.IO.File.ReadAllText("day1.txt");
        var elfsData = data.Split("\r\n\r\n");

        return elfsData.ToList();
    }

    public static void A() 
    {
        var elfsData = ElfsData();
        var currentMax = 0;

        foreach(var elf in elfsData)
        {
            var sum = elf.Split("\r\n").Sum(x => int.Parse(x));
            currentMax = sum > currentMax ? sum : currentMax;
        }

        Console.WriteLine(currentMax);
    }
    public static void B() 
    {
        var elfsData = ElfsData();
        var sums = new List<int>();

        foreach(var elf in elfsData)
        {
            var sum = elf.Split("\r\n").Sum(x => int.Parse(x));
            sums.Add(sum);
        }

        sums.Sort();
        var result = sums.Skip(sums.Count - 3).Sum();

        Console.WriteLine(result);
    }}