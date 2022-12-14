namespace adventofcode;

public class Day2 {

    private static IEnumerable<string> Data() 
    {
        var fileData = System.IO.File.ReadAllText("day2.txt");
        var data = fileData.Split("\r\n");

        return data.ToList();
    }

    private static int CalculateToolPoint(string tool)
    {
        return tool == "X" ? 1 
        : tool == "Y" ? 2
        : tool == "Z" ? 3 
        : 0;
    }

    private static int CalculateMatchPoint(string[] values) 
    {
        var elf = values[0];
        var player = values[1];

        if(player == "X")
        {
            return elf == "A" ? 3
                : elf == "C" ? 6
                : 0;
        }
        if(player == "Y") 
        {
            return elf == "B" ? 3
                : elf == "A" ? 6
                : 0; 
        }
        if(player == "Z")
        {
            return elf == "C" ? 3
                : elf == "B" ? 6
                : 0; 
        }

        return 0;
    }

    private static string GetToolForResult(string[] values)
    {
        var elf = values[0];
        var result = values[1];

        if(result == "X")
        {
            return elf == "A" ? "Z"
                : elf == "B" ? "X"
                : "Y";
        }
        if(result == "Y") 
        {
            return elf == "B" ? "Y"
                : elf == "A" ? "X"
                : "Z"; 
        }
        if(result == "Z")
        {
            return elf == "C" ? "X"
                : elf == "B" ? "Z"
                : "Y"; 
        }

        return "";
    }

    public static void A() 
    {
        var data = Data();
        var sumPoints = 0;

        foreach (var match in data) {
            var values = match.Split(' ');

            var toolPoint = CalculateToolPoint(values[1]);
            var matchPoint = CalculateMatchPoint(values);

            sumPoints+= toolPoint + matchPoint;
        }

        Console.WriteLine(sumPoints);
    }

    public static void B() {

        var data = Data();
        var sumPoints = 0;

        foreach (var match in data)
        {
            var values = match.Split(' ');

            var tool = GetToolForResult(values);

            var toolPoint = CalculateToolPoint(tool);
        
            var matchPoint = CalculateMatchPoint(new string[] {values[0], tool});

            sumPoints += toolPoint + matchPoint;
        }

        Console.WriteLine(sumPoints);
    }
}

/*
A = Rock
B = Paper
C = Scissor

X = Rock
Y = Paper
Z = Scissor

X = loose
Y = Draw
Z = Win
*/