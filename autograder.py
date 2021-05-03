"""This is the main program file for the auto grader program.
The auto grader assumes that the following files are in the same directory as the autograder:
  - autotraining.txt  --> file of tagged words used to train the HMM tagger
  - autotest.txt      --> file of untagged words to be tagged by the HMM
  - autosolution.txt  --> file with correct tags for autotest words
This auto grader generates a file called results.txt that records the test results.
"""
import os

if __name__ == '__main__':
    # Invoke the shell command to train and test the HMM tagger
    print("Training on autotraining.txt, running tests on autotest.txt. "
          "Output --> autooutput.txt")
    os.system("python tagger.py -d training5.txt training6.txt training7.txt -t test4.txt -o autooutput.txt")


    # Compare the contents of the HMM tagger output with the reference solution.
    # Store the missed cases and overall stats in results.txt
    with open("autooutput.txt", "r", encoding='utf-8') as output_file, \
         open("training4.txt", "r", encoding='utf-8') as solution_file, \
         open("results.txt", "w", encoding='utf-8') as results_file:
        # Each word is on a separate line in each file.
        output = output_file.readlines()
        solution = solution_file.readlines()
        total_matches = 0

        # generate the report
        for index in range(len(output)):
            if output[index] != solution[index]:
                results_file.write(f"Line {index + 1}: "
                                   f"expected <{output[index].strip()}> "
                                   f"but got <{solution[index].strip()}>\n")
            else:
                total_matches = total_matches + 1

        # Add stats at the end of the results file.
        results_file.write(f"Total words seen: {len(output)}.\n")
        results_file.write(f"Total matches: {total_matches}.\n")