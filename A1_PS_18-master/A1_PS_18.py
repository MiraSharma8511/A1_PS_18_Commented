# Input File to pass/insert data to system.
# Output File to display output in the file.
# Prompt Fie to read predefined command to be applied on the input data in the system.

in_file = 'inputPS18.txt'
out_file = 'outputPS18.txt'
prompt_file = 'promptsPS18.txt'


# This below class holds functions and objects related to student details
class Student:
    def __init__(self, student_id, cgpa):
        self.sID = student_id
        self.cgpa = cgpa

    def student_info(self):
        return (self.sID + " / " + self.cgpa) + "\n"


# This below class holds functions and objects related to hash table for mapping
class StudentHashTable:
    def __init__(self, size=300):  # This function creates an empty hash table and points to null.
        self.keys = []
        self.size = size
        self.map = [None] * size

    # Component sum hash code map + Compression by division function
    def nor_hash_id(self, key):
        h = 0
        for c in key:
            h = h + ord(c)
        return h % self.size

    # This is a function where student_id is passed as key and returns hash value
    def hash_id(self, key):
        h = self.nor_hash_id(key)
        return h

    # The usage of this function is to insert the student id and corresponding CPGA into the hash table.
    def insert_student_rec(self, student_id, cgpa):
        key_exists = False
        student = Student(student_id, cgpa)
        key = student.sID
        hash_key = self.hash_id(key)
        bucket = self.map[hash_key]
        if not bucket:
            self.map[hash_key] = []
            bucket = self.map[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:  # Check if encountered same key(student_id).
                key_exists = True  # Mark as key_exist true.
                break
        if key_exists:  # Check if encountered same key(student_id) then overwrite the existing key.
            bucket[i] = (key, student)  # At hash location, assign pair of key-value in hash table.
        else:
            bucket.append((key, student))  # To handle collision, separate chaining method applied for different key.
            self.keys.append(key)  # Here, linked list is created that returns same hash key value.

    # The usage of this function is to fetch the student details by passing student_id as key and returns values.
    def get_student_details(self, student_id):
        key = student_id
        hash_key = self.hash_id(key)
        bucket = self.map[hash_key]
        if bucket:
            for i, kv in enumerate(bucket):
                k, v = kv
                if key == k:
                    return v
        return None

    # The usage of this function is to clear hash table.
    def destroy_hash(self):
        self.map.clear()
        self.keys = []


# The UniversityReport class hold functions and objects related to reading input file and inserting data to hash table,
# reading prompt file and executing functions as per commands in prompt file,
# get list of students in hall of fame, get list of students for new course list,
# get all department max CGPA and average CGPA of all students of all department.

class UniversityReport:
    def __init__(self):
        self.studentMap = StudentHashTable()

    # The usage of this function is to read input file line by line and map key-value pair to hash table
    def read_input_file(self):
        input_file = open(in_file, "r")  # Open input_file to read the file data.
        count = 0
        for line in input_file:
            student_data_list = line.split("/")  # Read line to split record with '/' to get student_id & CGPA separate.
            count += 1
            self.studentMap.insert_student_rec(
                student_data_list[0].strip(),
                student_data_list[1].strip())  # Insert record in the hash table.
        input_file.close()  # Close the input file and free the file resource.

        output_file = open(out_file, "w")  # Open out_file to write the output data.
        output_file.write("Record added successfully %d.\n" % count)
        output_file.close()  # Close out_file after intimating the successful insertion of records.

    # The usage of this function is to reads prompts file and execute the respective function as per command detection.
    def read_prompts_file(self):
        prompts_file = open(prompt_file, "r")
        for line in prompts_file:
            if line.startswith(
                    "hallOfFame:"):  # Checks if prompt file has 'hallOfFame' command to execute hall_of_fame function.
                self.hall_of_fame()
            elif line.startswith("courseOffer:"):
                range_list = line.replace("courseOffer: ", "").split(" ")  # Extract range list from prompt command.
                range_list.pop(1)  # Extract range list from prompt command.
                self.new_course_list(range_list[0], range_list[1])  # Insert the range to get list of students.
            elif line.startswith("depAvg"):  # Checks if prompt file has 'depAvg' command to execute dep_avg function.
                self.dep_avg()  # Show list of all departments the maximum CGPA and average CGPA.
        prompts_file.close()  # Close prompt file after reading prompt command.

    # The usage of this function is to print the list of all students who have graduated and topped their department
    # in their year of graduation.
    def hall_of_fame(self):
        cse_graduated_list = []  # Creates the empty array for CSE graduated student list.
        ece_graduated_list = []  # Creates the empty array for ECE graduated student list.
        mec_graduated_list = []  # Creates the empty array for MEC graduated student list.
        arc_graduated_list = []  # Creates the empty array for ARC graduated student list.

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            course_code = key[4:7]
            if course_code == "CSE":  # Filter out the student record by extracting
                cse_cgpa = float(student.cgpa)  # and comparing the department code and adding
                cse_graduated_list.append(cse_cgpa)  # students to respective array list to
            elif course_code == "ECE":  # classify students based on department code.
                ece_cgpa = float(student.cgpa)
                ece_graduated_list.append(ece_cgpa)
            elif course_code == "MEC":
                mec_cgpa = float(student.cgpa)
                mec_graduated_list.append(mec_cgpa)
            elif course_code == "ARC":
                arc_cgpa = float(student.cgpa)
                arc_graduated_list.append(arc_cgpa)

        max_cse_cgpa = float(max(cse_graduated_list))  # store max of the CGPA of CSE department in variable.
        max_ece_cgpa = float(max(ece_graduated_list))  # store max of the CGPA of ECE department in variable.
        max_mec_cgpa = float(max(mec_graduated_list))  # store max of the CGPA of MEC department in variable.
        max_arc_cgpa = float(max(arc_graduated_list))  # store max of the CGPA of ARC department in variable.

        eligible_student_list = []  # create empty list of eligible students.

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            graduation_year = key[0:4]
            cgpa = float(student.cgpa)
            if cgpa == max_cse_cgpa and graduation_year == "2010":  # Filter out the student record by extracting
                eligible_student_list.append(student)  # and comparing the student code with year
            elif cgpa == max_ece_cgpa and graduation_year == "2010":  # '2010' and max CGPA of the students to
                eligible_student_list.append(student)  # add them in the list of eligible students.
            elif cgpa == max_mec_cgpa and graduation_year == "2010":
                eligible_student_list.append(student)
            elif cgpa == max_arc_cgpa and graduation_year == "2010":
                eligible_student_list.append(student)

        output_file = open(out_file, "a")  # Open output file to append the eligible students.
        output_file.write("---------- hall of fame ----------\n")
        output_file.write("Total eligible students: " + str(len(eligible_student_list)) + "\n")
        output_file.write("Qualified Students:\n")

        for student in eligible_student_list:
            output_file.write(student.student_info())  # Append students list to output file.
        output_file.close()  # Close output file.

    def new_course_list(self, cgpa_from, cgpa_to):
        min_cgpa = float(cgpa_from)
        max_cgpa = float(cgpa_to)
        student_list = []
        output_file = open(out_file, "a")  # Open output file to append details of students within min max CGPA range.
        output_file.write("-------------------------------------\n")
        output_file.write("---------- new course candidates ----------\n")
        output_file.write("Input: " + cgpa_from + " to " + cgpa_to)

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            cgpa = float(student.cgpa)
            if (cgpa >= min_cgpa) and (cgpa <= max_cgpa):  # Check student CGPA in min max range.
                student_list.append(student)  # Create a student list within the min max range.

        output_file.write("Total eligible students: " + str(len(student_list)) + "\n")
        output_file.write("Qualified Students:\n")

        for student in student_list:
            output_file.write(student.student_info())  # For the students within the range, append the student details.

        output_file.close()  # Close output file.

    # This function prints the list of all departments followed
    # by the maximum CGPA and average CGPA of all students in that department.
    # The output should be captured in outputPS18.txt following format.

    def dep_avg(self):
        cse_list = []  # Creates the empty array for CSE CGPA.
        ece_list = []  # Creates the empty array for ECE CGPA.
        mec_list = []  # Creates the empty array for MEC CGPA.
        arc_list = []  # Creates the empty array for ARC CGPA.

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            course_code = key[4:7]
            if course_code == "CSE":
                cse_cgpa = float(student.cgpa)  # Filter out the CGPA record by extracting
                cse_list.append(cse_cgpa)  # and comparing the department code and adding
            elif course_code == "ECE":  # CGPA record to respective array list.
                ece_cgpa = float(student.cgpa)
                ece_list.append(ece_cgpa)
            elif course_code == "MEC":
                mec_cgpa = float(student.cgpa)
                mec_list.append(mec_cgpa)
            elif course_code == "ARC":
                arc_cgpa = float(student.cgpa)
                arc_list.append(arc_cgpa)

        cse_set = set(cse_list)  # Get unique CGPA records by adding it to set.
        ece_set = set(ece_list)  # Get unique CGPA records by adding it to set.
        mec_set = set(mec_list)  # Get unique CGPA records by adding it to set.
        arc_set = set(arc_list)  # Get unique CGPA records by adding it to set.

        cse_max_cgpa = max(cse_set)  # Get Max number from the set.
        ece_max_cgpa = max(ece_set)  # Get Max number from the set.
        mec_max_cgpa = max(mec_set)  # Get Max number from the set.
        arc_max_cgpa = max(arc_set)  # Get Max number from the set.

        cse_average = sum(cse_list) / len(cse_list)  # Get average values.
        ece_average = sum(ece_list) / len(ece_list)  # Get average values.
        mec_average = sum(mec_list) / len(mec_list)  # Get average values.
        arc_average = sum(arc_list) / len(arc_list)  # Get average values.

        write_string_1 = "CSE: " + "max: " + str(cse_max_cgpa) + " avg: " + str(cse_average) + "\n"
        write_string_2 = "ECE: " + "max: " + str(ece_max_cgpa) + " avg: " + str(ece_average) + "\n"
        write_string_3 = "MEC: " + "max: " + str(mec_max_cgpa) + " avg: " + str(mec_average) + "\n"
        write_string_4 = "ARC: " + "max: " + str(arc_max_cgpa) + " avg: " + str(arc_average) + "\n"

        output_file = open(out_file, "a")  # Open output file to append maximum and average CGPA of each department.
        output_file.write("-------------------------------------\n")
        output_file.write("---------- department CGPA ----------\n")
        output_file.write(write_string_1)  # write to the output file.
        output_file.write(write_string_2)  # write to the output file.
        output_file.write(write_string_3)  # write to the output file.
        output_file.write(write_string_4)  # write to the output file.
        output_file.write("-------------------------------------\n")

        output_file.close()  # Close output file

    # Usage of this function is to destroy hash table.
    def destroy_hash(self):
        self.studentMap.destroy_hash()


universityReport = UniversityReport()  # Initiate the University Report Class.
universityReport.read_input_file()     # Read input file
universityReport.read_prompts_file()   # Read prompt file
universityReport.destroy_hash()        # Destroy the hash map and release the resource.
