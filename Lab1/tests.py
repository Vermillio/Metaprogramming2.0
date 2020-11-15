from CSharpFormatter import *

tests = [ ("""int[] numbers = { 4, 7, 10 };
int product = numbers.Aggregate(1, (int interim, int next) => interim * next);
Console.WriteLine(product);""",
"""int[] numbers = { 4, 7, 10 };
int product = numbers.Aggregate(1, (int interim, int next) => interim * next);
Console.WriteLine(product);""")]

def run_tests():
    print("Tests started")
    tests_failed = 0
    with open('errors.log', 'w+') as f:
        f.write("Running tests:\n")
        for i, test in zip(range(len(tests)), tests):
            result_str = CSharpFormatter().beautify(test[0], False)
            if result_str != test[1]:
                f.write("\nTEST " + str(i) + " FAILED:\n\n")
                f.write("expected:\n\n\"")
                f.write(test[1])
                f.write("\"\ngot:\n\n\"")
                f.write(result_str)
                f.write("\"\n")
                tests_failed+=1
            else:
                f.write("test " + str(i) + " completed.\n")
        f.write("Tests passed: "+str(len(tests)-tests_failed)+"/"+str(len(tests))+"")
    print("Tests finished")
    return (len(tests)-tests_failed)/len(tests)
