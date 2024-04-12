#include "functions.h"

void trimLeadingWhitespaces(string& filename) {
    int firstNonSpace = filename.find_first_not_of(" \t");
    if (firstNonSpace != string::npos) {
        filename = filename.substr(firstNonSpace);
    } else {
        filename.clear();
    }
}

map<string, char> return_files_with_type(string curr_path) {
    string files_argument = "ls -l " + curr_path;

    FILE* files = popen(files_argument.c_str(), "r");
    if (!files) {
        return map<string, char>();
    }

    char buffer_reader[128];
    ostringstream ostream;
    while (fgets(buffer_reader, sizeof(buffer_reader), files) != nullptr) {
        ostream << buffer_reader;
    }

    map<std::string, char> files_and_type;

    istringstream lines_stream(ostream.str());
    string line;
    string temp_vars;

    getline(lines_stream, line); //to skip the first line
    while (getline(lines_stream, line)) {
        if (line.length() > 0) {
            istringstream perline_stream(line);
            for(int i = 0; i < 8; i++)      // skip all the info such as permissions, owners, size etc.
                perline_stream >> temp_vars;
            string filename;
            getline(perline_stream, filename);
            trimLeadingWhitespaces(filename);
            files_and_type[filename] = (line[0] == 'd') ? 'd' : 'f';
        }
    }

    pclose(files);
    return files_and_type;
}

int return_count_of_files_in_dir(string curr_path) {
    string arg_lines = "ls -l " + curr_path + " | wc -l";
    FILE *file_line_count = popen(arg_lines.c_str(), "r");
    if (!file_line_count)  { return -1; }
    int lines_count;
    int arg = fscanf(file_line_count, "%i", &lines_count);
    if (arg == EOF) { return -1; }
    pclose(file_line_count);
    return lines_count;
}

vector<string> FileMonitorThread::getLargeFiles() const {
    QMutexLocker s(&t);
    return largeFiles;
}

void FileMonitorThread::run() {
    vector<string> largeFiles;
    QMutexLocker s(&t);
    string arg_files = "find " + homePath + " -size +" + to_string(thresholdSize) + "M";
    FILE *abs_path_to_files = popen(arg_files.c_str(), "r");
    if (!abs_path_to_files) {
        cerr << "Error finding files!" << endl;
        return ;
    }

    char buffer_reader[128];
    ostringstream ostream;
    while (fgets(buffer_reader, sizeof(buffer_reader), abs_path_to_files) != nullptr) {
        ostream << buffer_reader;
    }

    istringstream lines_of_all_files(ostream.str());
    string line;

    while (getline(lines_of_all_files, line)) {
        if (line.length() > 0) {
            largeFiles.push_back(line);
        }
    }
    askUserforAction = !largeFiles.empty();
    if (askUserforAction)
        this->largeFiles = move(largeFiles);
    pclose(abs_path_to_files);
}
