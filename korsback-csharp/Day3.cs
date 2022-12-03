namespace adventofcode;

public class Day3 
{
    private static int GetPriority(char letter) 
    {
        var letterString = letter.ToString();
        var letterUpper = letterString.ToUpper();
        var isUpper = letterUpper == letterString;
        var value = char.ToUpper(letter) - 64;

        return isUpper ? value + 26 : value;
    }

    public static void A() 
    {
        var data = Utils.GetData(3, "\r\n");

        var sumOfPoints = 0;

        foreach(var rucksack in data) 
        {
            var middleIndex = rucksack.Count() / 2;
            var compartment1 = rucksack.Substring(0, middleIndex);
            var compartment2 = rucksack.Substring(middleIndex);

            foreach(var letter in compartment1) {
                if(compartment2.Contains(letter)) {
                    
                    sumOfPoints += GetPriority(letter);
                    break;
                }
            }
        }
        Console.WriteLine(sumOfPoints);
    }

    public static void B() 
    {
        var data = Utils.GetData(3, "\r\n");
        var sumOfPoints = 0;

        for(int i = 0; i < data.Count(); i+=3) {
            
            var rucksacks = data.Skip(i).Take(3).ToList();

            var rucksack1 = rucksacks[0];
            var rucksack2 = rucksacks[1];
            var rucksack3 = rucksacks[2];

            foreach(var letter in rucksack1) 
            {
                if(rucksack2.Contains(letter) && rucksack3.Contains(letter)) 
                {
                    sumOfPoints += GetPriority(letter);
                    break;
                }
            }
        }
        Console.WriteLine(sumOfPoints);
    }
}